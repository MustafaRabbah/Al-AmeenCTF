#!/usr/bin/env python3
"""Builder for Challenge 03 - Packet Trail.

Creates a synthetic PCAP file containing a small HTTP exchange:
  - GET /          -> 200 OK (welcome page, decoy)
  - POST /comment  -> 200 OK (form data carries the flag)
  - GET /healthz   -> 200 OK (decoy)
The flag is embedded inside the POST body. Players use Wireshark or
tshark to follow the HTTP stream and recover the value.
"""
from scapy.all import (
    Ether, IP, TCP, Raw, wrpcap,
)
import base64
import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT  = os.path.join(BASE, "evidence", "capture.pcap")
FLAG = "AU-CS{easy_http_post_in_pcap}"

CLIENT = ("10.0.42.7",  "08:00:27:aa:bb:01")
SERVER = ("10.0.42.10", "08:00:27:aa:bb:02")


def build_stream(sport: int, payloads_c2s, payloads_s2c, t0: float):
    pkts = []
    seq_c, seq_s = 1000, 5000
    eth_cs = Ether(src=CLIENT[1], dst=SERVER[1])
    eth_sc = Ether(src=SERVER[1], dst=CLIENT[1])
    ip_cs  = IP(src=CLIENT[0], dst=SERVER[0])
    ip_sc  = IP(src=SERVER[0], dst=CLIENT[0])

    syn = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="S",  seq=seq_c)
    syn.time = t0
    pkts.append(syn)
    sa  = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="SA", seq=seq_s, ack=seq_c + 1)
    sa.time = t0 + 0.001
    pkts.append(sa)
    ack = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A",  seq=seq_c + 1, ack=seq_s + 1)
    ack.time = t0 + 0.002
    pkts.append(ack)
    seq_c += 1; seq_s += 1
    t = t0 + 0.003

    for body in payloads_c2s:
        data = body.encode()
        p = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="PA",
                                  seq=seq_c, ack=seq_s) / Raw(load=data)
        p.time = t; pkts.append(p); t += 0.005
        seq_c += len(data)
        a = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="A",
                                  seq=seq_s, ack=seq_c)
        a.time = t; pkts.append(a); t += 0.001

    for body in payloads_s2c:
        data = body.encode()
        p = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="PA",
                                  seq=seq_s, ack=seq_c) / Raw(load=data)
        p.time = t; pkts.append(p); t += 0.005
        seq_s += len(data)
        a = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A",
                                  seq=seq_c, ack=seq_s)
        a.time = t; pkts.append(a); t += 0.001

    fin = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="FA",
                                 seq=seq_c, ack=seq_s)
    fin.time = t; pkts.append(fin); t += 0.001
    fina = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="FA",
                                 seq=seq_s, ack=seq_c + 1)
    fina.time = t; pkts.append(fina); t += 0.001
    last_ack = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A",
                                 seq=seq_c + 1, ack=seq_s + 1)
    last_ack.time = t; pkts.append(last_ack)
    return pkts


def main() -> None:
    all_pkts = []
    encoded_flag = base64.b64encode(FLAG.encode()).decode()

    body1_req = (
        "GET / HTTP/1.1\r\n"
        "Host: portal.al-ameen.local\r\n"
        "User-Agent: Mozilla/5.0\r\n"
        "Accept: text/html\r\n\r\n"
    )
    body1_res = (
        "HTTP/1.1 200 OK\r\n"
        "Server: nginx/1.24\r\n"
        "Content-Type: text/html\r\n"
        "Content-Length: 51\r\n\r\n"
        "<html><body><h1>AL-AMEEN PORTAL</h1></body></html>\n"
    )
    all_pkts += build_stream(40012, [body1_req], [body1_res], t0=1715000000.0)

    form = (
        f"user=field_unit_3&"
        f"case=0042&"
        f"note_b64={encoded_flag}&"
        f"submit=send"
    )
    body2_req = (
        "POST /comment HTTP/1.1\r\n"
        "Host: portal.al-ameen.local\r\n"
        "User-Agent: Mozilla/5.0\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(form)}\r\n"
        "Cookie: session=8c3a1f2e\r\n\r\n"
        f"{form}"
    )
    body2_res = (
        "HTTP/1.1 200 OK\r\n"
        "Server: nginx/1.24\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 21\r\n\r\n"
        '{"status":"received"}'
    )
    all_pkts += build_stream(40015, [body2_req], [body2_res], t0=1715000010.0)

    body4_req = (
        "GET /api/news?page=1 HTTP/1.1\r\n"
        "Host: portal.al-ameen.local\r\n"
        "User-Agent: Mozilla/5.0\r\n"
        "Accept: application/json\r\n\r\n"
    )
    body4_res = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 95\r\n\r\n"
        '{"items":[{"id":1,"title":"Lab update"},{"id":2,"title":"Case tracker maintenance"}]}'
    )
    all_pkts += build_stream(40016, [body4_req], [body4_res], t0=1715000013.0)

    body5_req = (
        "POST /api/login HTTP/1.1\r\n"
        "Host: portal.al-ameen.local\r\n"
        "User-Agent: Mozilla/5.0\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 43\r\n\r\n"
        '{"username":"auditor","password":"wrongpass"}'
    )
    body5_res = (
        "HTTP/1.1 401 Unauthorized\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 27\r\n\r\n"
        '{"error":"invalid credentials"}'
    )
    all_pkts += build_stream(40017, [body5_req], [body5_res], t0=1715000016.0)

    body3_req = (
        "GET /healthz HTTP/1.1\r\n"
        "Host: portal.al-ameen.local\r\n"
        "User-Agent: curl/8.5.0\r\n\r\n"
    )
    body3_res = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 3\r\n\r\n"
        "OK\n"
    )
    all_pkts += build_stream(40018, [body3_req], [body3_res], t0=1715000020.0)

    body6_req = (
        "GET /assets/app.js HTTP/1.1\r\n"
        "Host: portal.al-ameen.local\r\n"
        "User-Agent: Mozilla/5.0\r\n\r\n"
    )
    body6_res = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/javascript\r\n"
        "Content-Length: 58\r\n\r\n"
        "console.log('portal loaded');const API='/api';void(API);\n"
    )
    all_pkts += build_stream(40021, [body6_req], [body6_res], t0=1715000023.0)

    body7_req = (
        "GET /api/time HTTP/1.1\r\n"
        "Host: portal.al-ameen.local\r\n"
        "User-Agent: python-requests/2.31\r\n"
        "Accept: application/json\r\n\r\n"
    )
    body7_res = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 42\r\n\r\n"
        '{"server_time":"2025-09-14T22:18:44+03:00"}'
    )
    all_pkts += build_stream(40025, [body7_req], [body7_res], t0=1715000026.0)

    wrpcap(OUT, all_pkts)
    print(f"[+] wrote {OUT} ({len(all_pkts)} packets)")


if __name__ == "__main__":
    main()
