#!/usr/bin/env python3
"""Builder for Challenge 07 - Thousand Requests (Hard DF).

Generates a large HTTP PCAP (>1000 requests) with heavy noise.
The flag is NOT present as a full string and must be assembled from
four words recovered from specific correlated requests.
"""
from scapy.all import Ether, IP, TCP, Raw, wrpcap
import random
import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(BASE, "evidence", "thousand_requests.pcap")

CLIENTS = [
    ("10.44.0.21", "08:00:27:aa:10:01"),
    ("10.44.0.22", "08:00:27:aa:10:02"),
    ("10.44.0.23", "08:00:27:aa:10:03"),
    ("10.44.0.24", "08:00:27:aa:10:04"),
    ("10.44.0.25", "08:00:27:aa:10:05"),
]
SERVER = ("10.44.0.10", "08:00:27:aa:20:99")


def mk_get(host: str, path: str, ua: str = "Mozilla/5.0", extra: str = "") -> str:
    return (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: {ua}\r\n"
        "Accept: */*\r\n"
        f"{extra}\r\n"
    )


def mk_resp(status: str, body: str, ctype: str = "application/json") -> str:
    return (
        f"HTTP/1.1 {status}\r\n"
        "Server: envoy/1.29\r\n"
        f"Content-Type: {ctype}\r\n"
        f"Content-Length: {len(body)}\r\n\r\n"
        f"{body}"
    )


def build_stream(client, server, sport: int, req: str, res: str, t0: float):
    pkts = []
    seq_c, seq_s = 1000, 5000
    eth_cs = Ether(src=client[1], dst=server[1])
    eth_sc = Ether(src=server[1], dst=client[1])
    ip_cs = IP(src=client[0], dst=server[0])
    ip_sc = IP(src=server[0], dst=client[0])

    syn = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="S", seq=seq_c)
    syn.time = t0
    pkts.append(syn)
    sa = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="SA", seq=seq_s, ack=seq_c + 1)
    sa.time = t0 + 0.001
    pkts.append(sa)
    ack = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c + 1, ack=seq_s + 1)
    ack.time = t0 + 0.002
    pkts.append(ack)
    seq_c += 1
    seq_s += 1

    req_b = req.encode()
    p_req = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="PA", seq=seq_c, ack=seq_s) / Raw(load=req_b)
    p_req.time = t0 + 0.003
    pkts.append(p_req)
    seq_c += len(req_b)

    a1 = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="A", seq=seq_s, ack=seq_c)
    a1.time = t0 + 0.004
    pkts.append(a1)

    res_b = res.encode()
    p_res = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="PA", seq=seq_s, ack=seq_c) / Raw(load=res_b)
    p_res.time = t0 + 0.005
    pkts.append(p_res)
    seq_s += len(res_b)

    a2 = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c, ack=seq_s)
    a2.time = t0 + 0.006
    pkts.append(a2)

    fin = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="FA", seq=seq_c, ack=seq_s)
    fin.time = t0 + 0.007
    pkts.append(fin)
    fin2 = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="FA", seq=seq_s, ack=seq_c + 1)
    fin2.time = t0 + 0.008
    pkts.append(fin2)
    last = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c + 1, ack=seq_s + 1)
    last.time = t0 + 0.009
    pkts.append(last)
    return pkts


def main() -> None:
    random.seed(0xA11DF00D)
    pkts = []
    t = 1716000000.0
    sport = 43000
    req_count = 0
    host = "core.lab.local"

    # 1200 noisy requests
    noise_paths = [
        "/api/ping", "/api/health", "/api/news?page=1", "/api/news?page=2",
        "/assets/main.js", "/assets/app.css", "/metrics", "/api/time",
        "/api/profile?id=41", "/api/profile?id=42", "/api/search?q=ops",
        "/api/search?q=hr", "/api/tasks?status=open", "/favicon.ico",
    ]
    for i in range(1200):
        c = CLIENTS[i % len(CLIENTS)]
        p = noise_paths[i % len(noise_paths)]
        req = mk_get(host, p, ua=f"Mozilla/5.0 (req-{i})")
        body = '{"ok":true,"id":%d}' % i
        if p.endswith(".js"):
            body = "console.log('ok-%d')" % i
            ctype = "application/javascript"
        elif p.endswith(".css"):
            body = "body{--v:%d}" % i
            ctype = "text/css"
        elif p == "/favicon.ico":
            body = "ICO"
            ctype = "application/octet-stream"
        else:
            ctype = "application/json"
        res = mk_resp("200 OK", body, ctype)
        pkts += build_stream(c, SERVER, sport, req, res, t)
        t += 0.02 + random.random() * 0.01
        sport += 1
        req_count += 1

    # Decoy clues
    decoys = [
        ("shadow", "route"), ("night", "signal"), ("fake", "token"), ("blue", "wire")
    ]
    for a, b in decoys:
        req = mk_get(host, f"/api/audit?word={a}&key={b}", ua="python-requests/2.31")
        res = mk_resp("200 OK", '{"status":"logged"}')
        pkts += build_stream(CLIENTS[1], SERVER, sport, req, res, t)
        t += 0.03
        sport += 1
        req_count += 1

    # Real clue chain: same endpoint, same client, increasing seq index
    words = ["mustafa", "rabbah", "deep", "traffic"]
    for idx, w in enumerate(words, start=1):
        req = mk_get(
            host,
            f"/api/intel/fragment?case=8841&seq={idx}&word={w}&trace=ops-77",
            ua="curl/8.5.0",
            extra="Cookie: session=sec8841\r\nX-Analyst: unit-3"
        )
        res = mk_resp("200 OK", '{"accepted":true}')
        pkts += build_stream(CLIENTS[3], SERVER, sport, req, res, t)
        t += 0.04
        sport += 1
        req_count += 1

    # More trailing noise (to hide clue location)
    for i in range(120):
        c = CLIENTS[(i + 2) % len(CLIENTS)]
        req = mk_get(host, f"/api/logs?offset={i}&limit=25", ua="Go-http-client/1.1")
        res = mk_resp("200 OK", '{"rows":25,"next":%d}' % (i + 25))
        pkts += build_stream(c, SERVER, sport, req, res, t)
        t += 0.02
        sport += 1
        req_count += 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wrpcap(OUT, pkts)
    print(f"[+] wrote {OUT}")
    print(f"[+] total requests: {req_count}")
    print("[*] expected flag: AU-CS{mustafa_rabbah_deep_traffic}")


if __name__ == "__main__":
    main()

