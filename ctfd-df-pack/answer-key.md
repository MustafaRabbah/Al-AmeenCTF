# Organizer Answer Key (Digital Forensics)

Do not share this file with players.

## 01) الصورة الصامتة (Silent Picture)
- Difficulty: Easy
- Points: 100
- Skill: EXIF metadata
- Flag: `AU-CS{easy_exif_metadata_speaks}`
- One-liner solver:
  ```bash
  exiftool evidence_001.jpg | awk -F': ' '/User Comment/ {print $2}'
  ```

## 02) الذيل المخفي (Hidden Tail)
- Difficulty: Easy
- Points: 125
- Skill: File carving
- Flag: `AU-CS{easy_zip_appended_after_png}`
- One-liner solver:
  ```bash
  unzip -p report_cover.png flag.txt
  ```

## 03) أثر الحزم (Packet Trail)
- Difficulty: Easy
- Points: 150
- Skill: PCAP / HTTP analysis
- Flag: `AU-CS{easy_http_post_in_pcap}`
- One-liner solver:
  ```bash
  tshark -r capture.pcap -Y 'http.request.uri == "/comment"' -T fields -e http.file_data \
    | xxd -r -p | sed -n 's/.*note_b64=\([^&]*\).*/\1/p' \
    | python3 -c 'import sys,base64;print(base64.b64decode(sys.stdin.read().strip()).decode())'
  ```

## 04) همس البكسلات (Pixel Whisper)
- Difficulty: Medium
- Points: 200
- Skill: LSB steganography
- Flag: `AU-CS{medium_lsb_red_channel_msb}`
- Reference solver: `solution_scripts/extract.py`
  ```bash
  python3 04-medium-pixel-whisper/solution_scripts/extract.py
  ```

## 05) شبح القرص (Disk Ghost)
- Difficulty: Medium
- Points: 225
- Skill: FAT deleted-file recovery
- Flag: `AU-CS{medium_deleted_but_recoverable}`
- One-liner solver (requires sleuthkit):
  ```bash
  fls -r -d case_drive.img | awk '/flag.txt/ {print $3}' | tr -d ':' \
    | xargs -I{} icat case_drive.img {}
  ```

## 06) استخبارات المرور (Traffic Intel)
- Difficulty: Hard
- Points: 300
- Skill: Multi-request Wireshark correlation
- Flag: `AU-CS{nour.ops_7419_3_867}`
- How derived:
  - `actor` from successful Basic auth login user
  - `caseid` from `/api/v2/export?case=...`
  - `failedlogins` count of prior `401` on `/api/login`
  - `exfilbytes` from `/api/v2/upload` `Content-Length`

## 07) طوفان الطلبات (Thousand Requests)
- Difficulty: Very Hard
- Points: 350
- Skill: High-volume PCAP correlation
- Flag: `AU-CS{mustafa_rabbah_deep_traffic}`
- How derived:
  - Filter requests to `/api/intel/fragment?case=8841`
  - Collect ordered words by `seq=1..4`
  - Assemble: `mustafa` + `rabbah` + `deep` + `traffic`

## 08) أثر الحادثة (Incident Trace)
- Difficulty: Very Hard
- Points: 375
- Skill: Multi-source forensic timeline correlation (non-PCAP)
- Flag: `AU-CS{mustafa_forensic_shadow_trail}`
- How derived:
  - `mustafa` from `auth.log` (evt `IR-7741`)
  - `forensic` from USB label in `usb-events.log`
  - `shadow` from cron `--tag=shadow`
  - `trail` from bash history file move `.shadow.trail`

## 09) ملف القضية 909 (Ultra Casefile)
- Difficulty: Ultra
- Points: 450
- Skill: Multi-artifact correlation with DB + timeline + hash validation
- Flag: `AU-CS{mustafa_casefile_ultra_chain_909}`

## 10) المرور الرمزي المتشظي (Ultra Symbolic Traffic)
- Difficulty: Ultra+
- Points: 500
- Skill: High-volume HTTP correlation + XOR + symbolic decoding
- Flag: `AU-CS{mustafa_ultra_symbolic_cipher_mesh_10}`
