#!/usr/bin/env python3
"""
Build Challenge 08 - Incident Trace (Hard DF, non-PCAP).

Scenario:
- SOC suspects insider activity on workstation `ops-ws-07`.
- Evidence is a mixed incident bundle (logs, history, cron, USB events).
- Players must correlate one incident id across sources and extract four words.
"""
import csv
import os
import random
import zipfile
from datetime import datetime, timedelta

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVID = os.path.join(BASE, "evidence")
FLAG = "AU-CS{mustafa_forensic_shadow_trail}"


def write_text(path: str, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_auth_log(path: str):
    random.seed(8841)
    start = datetime(2026, 3, 11, 8, 0, 0)
    lines = []
    users = ["ops", "backup", "dev", "monitor", "guest", "auditor", "svc-sync"]
    hosts = ["10.50.0.10", "10.50.0.11", "10.50.0.12", "10.50.0.13"]
    for i in range(3200):
        t = start + timedelta(seconds=i * 17)
        u = users[i % len(users)]
        h = hosts[i % len(hosts)]
        if i % 19 == 0:
            lines.append(f"{t} AUTH fail user={u} src={h} reason=bad_password")
        else:
            lines.append(f"{t} AUTH ok user={u} src={h} session=s{i:05d}")

    # Real incident chain
    lines += [
        "2026-03-12 21:13:44 AUTH fail user=mustafa src=10.50.0.77 reason=bad_password evt=IR-7741",
        "2026-03-12 21:13:52 AUTH fail user=mustafa src=10.50.0.77 reason=bad_password evt=IR-7741",
        "2026-03-12 21:14:08 AUTH ok user=mustafa src=10.50.0.77 session=s77410 evt=IR-7741",
    ]
    write_text(path, lines)


def build_sudo_log(path: str):
    lines = []
    start = datetime(2026, 3, 11, 8, 10, 0)
    cmds = ["apt update", "systemctl restart nginx", "journalctl -u ssh", "ls -la /opt", "id"]
    for i in range(1400):
        t = start + timedelta(seconds=i * 23)
        c = cmds[i % len(cmds)]
        lines.append(f"{t} sudo user=ops tty=pts/{i%4} cmd=\"{c}\" result=ok")

    lines += [
        "2026-03-12 21:14:19 sudo user=mustafa tty=pts/7 cmd=\"sudo -l\" result=ok evt=IR-7741",
        "2026-03-12 21:14:24 sudo user=mustafa tty=pts/7 cmd=\"sudo /usr/bin/rsync -a /srv/reports /mnt/usb\" result=ok evt=IR-7741",
    ]
    write_text(path, lines)


def build_usb_log(path: str):
    lines = []
    start = datetime(2026, 3, 11, 8, 30, 0)
    for i in range(900):
        t = start + timedelta(seconds=i * 45)
        lines.append(
            f"{t} USB attach vendor=Generic model=FlashDisk serial=SN{i:06d} mount=/media/usb{i%5}"
        )
        if i % 7 == 0:
            lines.append(f"{t} USB detach serial=SN{i:06d}")

    lines += [
        "2026-03-12 21:14:30 USB attach vendor=Kingston model=DataTraveler serial=IR7741 label=forensic mount=/mnt/usb evt=IR-7741",
        "2026-03-12 21:20:02 USB detach serial=IR7741 evt=IR-7741",
    ]
    write_text(path, lines)


def build_cron(path: str):
    lines = [
        "# m h dom mon dow user command",
        "*/5 * * * * root /usr/local/bin/cleanup-temp --keep=12h",
        "0 * * * * root /usr/local/bin/archive-metrics --dst=/var/archive",
        "15 2 * * * root /usr/local/bin/rotate-keys --mode=safe",
        "# --- injected job ---",
        "17 21 12 3 * root /usr/local/bin/shadow_copy --src=/srv/reports --dst=/mnt/usb/.cache --tag=shadow --evt=IR-7741",
    ]
    write_text(path, lines)


def build_history(path: str):
    lines = []
    for i in range(2600):
        lines.append(f"echo heartbeat_{i}")
        if i % 3 == 0:
            lines.append("ls -la /var/log")
    lines += [
        "whoami",
        "cat /etc/hosts",
        "cd /srv/reports",
        "tar -czf /tmp/q1_reports.tar.gz .",
        "mv /tmp/q1_reports.tar.gz /mnt/usb/.cache/.shadow.trail",
        "history -c",
    ]
    write_text(path, lines)


def build_browser_csv(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "url", "title", "user"])
        base = datetime(2026, 3, 11, 9, 0, 0)
        for i in range(1600):
            ts = (base + timedelta(seconds=i * 11)).isoformat(sep=" ")
            w.writerow([ts, f"https://intra.local/news/{i%40}", "Portal", "ops"])
        w.writerow(["2026-03-12 21:12:58", "https://wiki.local/ir/7741", "IR Runbook", "mustafa"])
        w.writerow(["2026-03-12 21:13:31", "https://wiki.local/storage/usb-labels", "USB Label Policy", "mustafa"])


def build_readme(path: str):
    text = [
        "Incident Bundle - ops-ws-07",
        "Collected by: AL-AMN SOC",
        "Bundle contains logs from multiple subsystems.",
        "Some entries are noisy or irrelevant.",
        "Primary lead: correlate evt=IR-7741 across all artifacts.",
        "Build flag as four words in timeline order.",
    ]
    write_text(path, text)


def main():
    bundle_root = os.path.join(EVID, "incident_bundle")
    os.makedirs(bundle_root, exist_ok=True)

    build_auth_log(os.path.join(bundle_root, "logs", "auth.log"))
    build_sudo_log(os.path.join(bundle_root, "logs", "sudo.log"))
    build_usb_log(os.path.join(bundle_root, "logs", "usb-events.log"))
    build_cron(os.path.join(bundle_root, "system", "cron.txt"))
    build_history(os.path.join(bundle_root, "system", "bash_history.txt"))
    build_browser_csv(os.path.join(bundle_root, "workstation", "browser_history.csv"))
    build_readme(os.path.join(bundle_root, "README.txt"))

    zip_path = os.path.join(EVID, "incident_bundle.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(bundle_root):
            for fn in files:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, EVID)
                z.write(full, rel)

    print(f"[+] wrote {zip_path}")
    print(f"[+] expected flag: {FLAG}")


if __name__ == "__main__":
    main()

