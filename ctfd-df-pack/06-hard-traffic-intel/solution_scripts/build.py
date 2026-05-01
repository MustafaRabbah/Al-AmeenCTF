#!/usr/bin/env python3
"""Builder for Challenge 06 - Traffic Intel (Hard).

Hard DF/Wireshark challenge where the flag is NOT present directly.
Players must correlate several HTTP requests and infer multiple values.

Flag formula:
  AU-CS{<actor>_<caseid>_<failed_logins>_<exfil_bytes>}
"""
from scapy.all import Ether, IP, TCP, Raw, wrpcap
import base64
import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(BASE, "evidence", "traffic_intel.pcap")


def build_stream(client, server, sport: int, payloads_c2s, payloads_s2c, t0: float):
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
    t = t0 + 0.003

    for body in payloads_c2s:
        data = body.encode()
        p = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="PA", seq=seq_c, ack=seq_s) / Raw(load=data)
        p.time = t
        pkts.append(p)
        t += 0.004
        seq_c += len(data)
        a = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="A", seq=seq_s, ack=seq_c)
        a.time = t
        pkts.append(a)
        t += 0.001

    for body in payloads_s2c:
        data = body.encode()
        p = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="PA", seq=seq_s, ack=seq_c) / Raw(load=data)
        p.time = t
        pkts.append(p)
        t += 0.004
        seq_s += len(data)
        a = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c, ack=seq_s)
        a.time = t
        pkts.append(a)
        t += 0.001

    fin = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="FA", seq=seq_c, ack=seq_s)
    fin.time = t
    pkts.append(fin)
    t += 0.001
    fina = eth_sc / ip_sc / TCP(sport=80, dport=sport, flags="FA", seq=seq_s, ack=seq_c + 1)
    fina.time = t
    pkts.append(fina)
    t += 0.001
    last = eth_cs / ip_cs / TCP(sport=sport, dport=80, flags="A", seq=seq_c + 1, ack=seq_s + 1)
    last.time = t
    pkts.append(last)
    return pkts


def mk_get(host: str, path: str, ua="Mozilla/5.0", extra=""):
    return (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: {ua}\r\n"
        "Accept: */*\r\n"
        f"{extra}\r\n"
    )


def mk_post(host: str, path: str, body: str, content_type="application/json", extra=""):
    return (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: Mozilla/5.0\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"{extra}\r\n"
        f"{body}"
    )


def mk_resp(status: str, body: str, ctype="application/json"):
    return (
        f"HTTP/1.1 {status}\r\n"
        "Server: nginx/1.24\r\n"
        f"Content-Type: {ctype}\r\n"
        f"Content-Length: {len(body)}\r\n\r\n"
        f"{body}"
    )


def main() -> None:
    client_a = ("10.10.14.23", "08:00:27:aa:bb:10")
    client_b = ("10.10.14.31", "08:00:27:aa:bb:11")
    server = ("10.10.14.5", "08:00:27:aa:bb:99")
    host = "api.lab.local"
    cdn_host = "cdn.lab.local"
    files_host = "files.lab.local"
    pkts = []
    t = 1715001000.0

    # Decoys - normal traffic from two clients.
    pkts += build_stream(client_a, server, 41001, [mk_get(host, "/"), mk_get(host, "/favicon.ico")], [
        mk_resp("200 OK", "<html>dashboard</html>", "text/html"),
        mk_resp("404 Not Found", "{}", "application/json"),
    ], t)
    t += 2
    pkts += build_stream(client_b, server, 41002, [mk_get(host, "/api/time")], [
        mk_resp("200 OK", '{"ts":"2025-09-14T19:13:00Z"}')
    ], t)
    t += 2

    # CDN/static noise.
    pkts += build_stream(client_b, server, 41003, [mk_get(cdn_host, "/assets/main.js"), mk_get(cdn_host, "/assets/app.css")], [
        mk_resp("200 OK", "console.log('ok')", "application/javascript"),
        mk_resp("200 OK", "body{margin:0}", "text/css"),
    ], t)
    t += 2
    pkts += build_stream(client_a, server, 41004, [mk_get(files_host, "/public/readme.txt")], [
        mk_resp("200 OK", "training portal", "text/plain")
    ], t)
    t += 2

    # Three failed logins for same actor (clue #3).
    for sp in (41010, 41011, 41012):
        bad = mk_post(host, "/api/login", '{"username":"nour.ops","password":"BadPass!"}')
        pkts += build_stream(client_a, server, sp, [bad], [mk_resp("401 Unauthorized", '{"error":"bad creds"}')], t)
        t += 2

    # Extra failed logins for another user (noise that should be ignored).
    for sp in (41020, 41021):
        bad_other = mk_post(host, "/api/login", '{"username":"fadi.dev","password":"Winter!2025"}')
        pkts += build_stream(client_b, server, sp, [bad_other], [mk_resp("401 Unauthorized", '{"error":"bad creds"}')], t)
        t += 2

    # Successful login with Basic token (clue #1 actor).
    auth_token = base64.b64encode(b"nour.ops:BlueFalcon!26").decode()
    good = mk_post(
        host,
        "/api/login",
        '{"mode":"token-auth"}',
        extra=f"Authorization: Basic {auth_token}\r\nX-Trace: 74f2-c1"
    )
    pkts += build_stream(client_a, server, 41013, [good], [mk_resp("200 OK", '{"session":"s-9981","role":"analyst"}')], t)
    t += 2

    # More decoys.
    pkts += build_stream(client_a, server, 41014, [mk_get(host, "/api/profile?id=41")], [mk_resp("200 OK", '{"name":"Nour","tz":"UTC+3"}')], t)
    t += 2
    pkts += build_stream(client_b, server, 41015, [mk_post(host, "/api/search", '{"q":"training docs"}')], [mk_resp("200 OK", '{"hits":12}')], t)
    t += 2
    pkts += build_stream(client_a, server, 41022, [mk_get(host, "/api/events?limit=20", extra="Cookie: session=s-9981\r\n")], [
        mk_resp("200 OK", '{"events":[{"id":51},{"id":52},{"id":53}]}')
    ], t)
    t += 2
    pkts += build_stream(client_b, server, 41023, [mk_get(host, "/api/v2/export?case=9191&fmt=json", extra="Cookie: session=s-1000\r\n")], [
        mk_resp("403 Forbidden", '{"error":"forbidden"}')
    ], t)
    t += 2

    # Case export request (clue #2 case id).
    ex1 = mk_get(host, "/api/v2/export?case=7419&fmt=csv", extra="Cookie: session=s-9981\r\n")
    ex1r = mk_resp("200 OK", '{"job":"j-447","status":"queued","size":867}')
    pkts += build_stream(client_a, server, 41016, [ex1], [ex1r], t)
    t += 2

    # Fake upload noise (different session and job).
    fake_upload = mk_post(
        host,
        "/api/v2/upload",
        "Y" * 412,
        content_type="application/octet-stream",
        extra="Cookie: session=s-1000\r\nX-Job: j-201"
    )
    pkts += build_stream(client_b, server, 41024, [fake_upload], [mk_resp("401 Unauthorized", '{"error":"expired session"}')], t)
    t += 2

    # Exfil upload (real clue #4 bytes from Content-Length).
    # Body length intentionally 867 and tied to j-447 + s-9981 chain.
    exfil_body = "X" * 867
    ex2 = mk_post(host, "/api/v2/upload", exfil_body, content_type="application/octet-stream",
                  extra="Cookie: session=s-9981\r\nX-Job: j-447")
    ex2r = mk_resp("202 Accepted", '{"status":"stored"}')
    pkts += build_stream(client_a, server, 41017, [ex2], [ex2r], t)
    t += 2

    # Additional API noise after exfil.
    pkts += build_stream(client_a, server, 41025, [mk_get(host, "/api/audit?job=j-447", extra="Cookie: session=s-9981\r\n")], [
        mk_resp("200 OK", '{"audit":"queued","priority":"low"}')
    ], t)
    t += 2
    pkts += build_stream(client_b, server, 41026, [mk_get(files_host, "/public/logo.png")], [
        mk_resp("200 OK", "PNGDATA", "application/octet-stream")
    ], t)
    t += 2

    # Tail decoys.
    pkts += build_stream(client_b, server, 41018, [mk_get(host, "/api/metrics")], [mk_resp("403 Forbidden", '{"error":"denied"}')], t)
    t += 2
    pkts += build_stream(client_a, server, 41019, [mk_get(host, "/healthz", "curl/8.5.0")], [mk_resp("200 OK", "OK", "text/plain")], t)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wrpcap(OUT, pkts)
    print(f"[+] wrote {OUT} ({len(pkts)} packets)")
    print("[*] expected flag: AU-CS{nour.ops_7419_3_867}")


if __name__ == "__main__":
    main()

