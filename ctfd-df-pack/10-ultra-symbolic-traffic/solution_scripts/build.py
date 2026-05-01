#!/usr/bin/env python3
"""
Challenge 10 - Ultra Symbolic Traffic (Hard DF)

Large HTTP PCAP with:
- heavy noise (2000+ requests)
- multi-stage clue chain
- XOR + symbolic substitution decoding
"""
from scapy.all import Ether, IP, TCP, Raw, wrpcap
import os
import random

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(BASE, "evidence", "ultra_symbolic_traffic.pcap")

CLIENTS = [
    ("10.66.0.21", "08:00:27:ab:10:01"),
    ("10.66.0.22", "08:00:27:ab:10:02"),
    ("10.66.0.23", "08:00:27:ab:10:03"),
    ("10.66.0.24", "08:00:27:ab:10:04"),
    ("10.66.0.25", "08:00:27:ab:10:05"),
]
SERVER = ("10.66.0.10", "08:00:27:ab:20:99")
HOST = "pipeline.lab.local"

FLAG = "AU-CS{mustafa_ultra_symbolic_cipher_mesh_10}"
WORDS = ["mustafa", "ultra", "symbolic", "cipher", "mesh", "10"]
TRACE = "ZX-7741-ULTRA"
XOR_KEY = 0x37

# Two-char symbol alphabet (printable ascii only)
SYM = [
    "~!", "~@", "~#", "~$", "~%", "~^", "~&", "~*", "~(", "~)",
    "_!", "_@", "_#", "_$", "_%", "_^", "_&", "_*", "_(", "_)",
    "+!", "+@", "+#", "+$", "+%", "+^",
]
ALPHA = "abcdefghijklmnopqrstuvwxyz"
MAP = {ALPHA[i]: SYM[i] for i in range(26)}
REV = {v: k for k, v in MAP.items()}


def mk_get(path: str, ua: str = "Mozilla/5.0", extra: str = "") -> str:
    return (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        f"User-Agent: {ua}\r\n"
        "Accept: */*\r\n"
        f"{extra}\r\n"
    )


def mk_resp(status: str, body: str, ctype: str = "application/json") -> str:
    return (
        f"HTTP/1.1 {status}\r\n"
        "Server: envoy/1.30\r\n"
        f"Content-Type: {ctype}\r\n"
        f"Content-Length: {len(body)}\r\n\r\n"
        f"{body}"
    )


def stream(client, sport: int, req: str, res: str, t0: float):
    pkts = []
    seq_c, seq_s = 1000, 5000
    eth_cs = Ether(src=client[1], dst=SERVER[1])
    eth_sc = Ether(src=SERVER[1], dst=client[1])
    ip_cs = IP(src=client[0], dst=SERVER[0])
    ip_sc = IP(src=SERVER[0], dst=client[0])

    syn = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="S", seq=seq_c); syn.time = t0; pkts.append(syn)
    sa = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="SA", seq=seq_s, ack=seq_c + 1); sa.time = t0 + 0.001; pkts.append(sa)
    ack = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c + 1, ack=seq_s + 1); ack.time = t0 + 0.002; pkts.append(ack)
    seq_c += 1; seq_s += 1

    rb = req.encode()
    rr = res.encode()
    p1 = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="PA", seq=seq_c, ack=seq_s) / Raw(load=rb); p1.time = t0 + 0.003; pkts.append(p1)
    seq_c += len(rb)
    a1 = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="A", seq=seq_s, ack=seq_c); a1.time = t0 + 0.004; pkts.append(a1)
    p2 = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="PA", seq=seq_s, ack=seq_c) / Raw(load=rr); p2.time = t0 + 0.005; pkts.append(p2)
    seq_s += len(rr)
    a2 = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c, ack=seq_s); a2.time = t0 + 0.006; pkts.append(a2)
    f1 = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="FA", seq=seq_c, ack=seq_s); f1.time = t0 + 0.007; pkts.append(f1)
    f2 = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="FA", seq=seq_s, ack=seq_c + 1); f2.time = t0 + 0.008; pkts.append(f2)
    la = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c + 1, ack=seq_s + 1); la.time = t0 + 0.009; pkts.append(la)
    return pkts


def xor_hex(s: str) -> str:
    return "".join(f"{(ord(ch) ^ XOR_KEY):02x}" for ch in s)


def sym_encode(s: str) -> str:
    out = []
    for ch in s:
        if ch in MAP:
            out.append(MAP[ch])
        elif ch.isdigit():
            out.append(f"={ch}")
        elif ch == "_":
            out.append("--")
        else:
            out.append("??")
    return "".join(out)


def main():
    random.seed(7741)
    pkts = []
    t = 1717000000.0
    sport = 46000
    req_count = 0

    noise_paths = [
        "/api/ping", "/api/time", "/api/assets?v=1", "/api/news?p=1", "/api/news?p=2",
        "/api/profile?id=40", "/api/profile?id=41", "/api/tasks?state=open",
        "/metrics", "/favicon.ico", "/healthz"
    ]

    # 2300 noisy requests
    for i in range(2300):
        c = CLIENTS[i % len(CLIENTS)]
        p = noise_paths[i % len(noise_paths)]
        req = mk_get(p, ua=f"Mozilla/5.0 (n{i})")
        if p == "/favicon.ico":
            res = mk_resp("200 OK", "ICO", "application/octet-stream")
        elif p == "/metrics":
            res = mk_resp("200 OK", f"ok {i}", "text/plain")
        else:
            res = mk_resp("200 OK", '{"ok":true,"id":%d}' % i)
        pkts += stream(c, sport, req, res, t)
        t += 0.012 + random.random() * 0.008
        sport += 1
        req_count += 1

    # Stage 1: known plaintext xor leak (derive XOR key)
    req = mk_get(f"/api/diag/known?trace={TRACE}&p=alpha")
    res = mk_resp("200 OK", '{"known":"alpha","cipher_hex":"%s"}' % xor_hex("alpha"))
    pkts += stream(CLIENTS[2], sport, req, res, t); t += 0.03; sport += 1; req_count += 1

    # Stage 2: symbolic map availability
    map_payload = ",".join(f"{a}:{MAP[a]}" for a in ALPHA)
    req = mk_get(f"/api/diag/map?trace={TRACE}")
    res = mk_resp("200 OK", '{"symbol_map":"%s"}' % map_payload)
    pkts += stream(CLIENTS[2], sport, req, res, t); t += 0.03; sport += 1; req_count += 1

    # Stage 3: real fragments (each request holds xor+symbolic encoded word)
    for i, w in enumerate(WORDS, 1):
        mixed = sym_encode("".join(chr((ord(c) ^ XOR_KEY)) for c in w))
        req = mk_get(
            f"/api/secure/fragment?trace={TRACE}&seq={i}&blob={mixed}",
            ua="curl/8.7.1",
            extra="Cookie: session=ultra7741\r\nX-Req-Chain: core"
        )
        res = mk_resp("200 OK", '{"accepted":true,"seq":%d}' % i)
        pkts += stream(CLIENTS[2], sport, req, res, t)
        t += 0.04
        sport += 1
        req_count += 1

    # Add decoy fragments with different trace
    decoy_words = ["ghost", "token", "wrong", "route"]
    for i, w in enumerate(decoy_words, 1):
        mixed = sym_encode("".join(chr((ord(c) ^ XOR_KEY)) for c in w))
        req = mk_get(f"/api/secure/fragment?trace=ZX-0000-FAKE&seq={i}&blob={mixed}", ua="curl/8.7.1")
        res = mk_resp("200 OK", '{"accepted":true,"seq":%d}' % i)
        pkts += stream(CLIENTS[4], sport, req, res, t)
        t += 0.02
        sport += 1
        req_count += 1

    wrpcap(OUT, pkts)
    print(f"[+] wrote {OUT}")
    print(f"[+] total requests: {req_count}")
    print(f"[+] expected flag: {FLAG}")


if __name__ == "__main__":
    main()

