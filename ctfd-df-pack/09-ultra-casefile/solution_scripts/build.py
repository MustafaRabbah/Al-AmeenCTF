#!/usr/bin/env python3
import os, json, sqlite3, hashlib, random
from datetime import datetime, timedelta

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVID = os.path.join(BASE, "evidence")
FLAG = "AU-CS{mustafa_casefile_ultra_chain_909}"

os.makedirs(EVID, exist_ok=True)

# 1) Build noisy timeline log
start = datetime(2026, 4, 7, 8, 0, 0)
lines = []
for i in range(5000):
    t = start + timedelta(seconds=i * 9)
    lines.append(f"{t} EVT src=agent-{i%9} op=heartbeat code={1000+i%37}")

incident_id = "CF-909"
lines += [
    "2026-04-07 19:21:03 EVT src=usbmon op=attach serial=KNG-909 evt=CF-909",
    "2026-04-07 19:21:41 EVT src=syncd op=copy path=/mnt/usb/.ops/.bundle evt=CF-909",
    "2026-04-07 19:22:10 EVT src=cron op=run tag=shadow-909 evt=CF-909",
]
with open(os.path.join(EVID, "timeline.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# 2) Build sqlite with decoys and true chain
dbp = os.path.join(EVID, "ops_cache.db")
con = sqlite3.connect(dbp)
cur = con.cursor()
cur.execute("create table notes(id integer primary key, case_id text, k text, v text, ts text)")
for i in range(2500):
    cur.execute("insert into notes(case_id,k,v,ts) values(?,?,?,?)",
                (f"CF-{100+i%40}", "noise", f"decoy_{i%17}", str(start + timedelta(seconds=i*13))))
rows = [
    (incident_id, "w1", "mustafa", "2026-04-07 19:23:01"),
    (incident_id, "w2", "casefile", "2026-04-07 19:23:07"),
    (incident_id, "w3", "ultra", "2026-04-07 19:23:19"),
    (incident_id, "w4", "chain", "2026-04-07 19:23:31"),
    (incident_id, "n", "909", "2026-04-07 19:23:42"),
]
cur.executemany("insert into notes(case_id,k,v,ts) values(?,?,?,?)", rows)
con.commit()
con.close()

# 3) Build hash clue file requiring ordering
clue = {
    "case_id": incident_id,
    "rule": "assemble w1_w2_w3_w4_n",
    "sha256_expected": hashlib.sha256("mustafa_casefile_ultra_chain_909".encode()).hexdigest(),
    "note": "decoys exist in DB and logs; use exact case_id correlation only",
}
with open(os.path.join(EVID, "clue.json"), "w", encoding="utf-8") as f:
    json.dump(clue, f, indent=2)

print("[+] built DF ultra evidence")
print(f"[+] flag: {FLAG}")

