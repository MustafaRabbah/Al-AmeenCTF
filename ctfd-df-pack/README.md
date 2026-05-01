# Al-Ameen CTF - Digital Forensics Pack

حزمة فيها 10 تحديات تحقيق جنائي رقمي حقيقية، كل واحد يعلّم مهارة
مختلفة عن الآخر:

| #  | الاسم               | المستوى | المهارة                          | الملف المُسلّم للاعب          |
|----|---------------------|---------|----------------------------------|-------------------------------|
| 01 | الصورة الصامتة     | سهل     | EXIF / Metadata                  | `evidence_001.jpg`            |
| 02 | الذيل المخفي       | سهل     | File Carving                     | `report_cover.png`            |
| 03 | أثر الحزم          | سهل     | تحليل PCAP / HTTP                | `capture.pcap`                |
| 04 | همس البكسلات       | متوسط   | Steganography (LSB)              | `whisper.png`                 |
| 05 | شبح القرص          | متوسط   | استرجاع ملفات محذوفة من FAT      | `case_drive.img`              |
| 06 | استخبارات المرور   | صعب     | Wireshark correlation analysis   | `traffic_intel.pcap`          |
| 07 | طوفان الطلبات      | صعب جدًا| Large PCAP correlation           | `thousand_requests.pcap`      |
| 08 | أثر الحادثة        | صعب جدًا| Multi-source incident timeline   | `incident_bundle.zip`         |
| 09 | ملف القضية 909     | Ultra   | DB+Logs correlation & validation | `timeline.log / ops_cache.db` |
| 10 | المرور الرمزي      | Ultra+  | HTTP correlation + XOR + symbols | `ultra_symbolic_traffic.pcap` |

كل تحدي داخل مجلد مستقل ويحتوي على:

- `description.md` — وصف عربي جاهز للنسخ على منصة CTFd
- `challenge-info.md` — معلومات التحدي والنقاط وطريقة التسليم
- `solution.md` — طريقة الحل التفصيلية (للمنظّم فقط)
- `evidence/` — الملف الفعلي الذي يُسلَّم للاعبين
- `solution_scripts/` — السكربتات التي تبني (وتحلّ) الدليل

## ملاحظات عامة

- صيغة جميع الأعلام: `AU-CS{...}`
- نطاق النقاط: من `100` إلى `500`
- جميع الأدلة مولّدة عبر سكربتات قابلة لإعادة التشغيل (reproducible).
- لا يوجد تحدي يعتمد على CTF خارجي أو خدمة عبر الإنترنت — كل التحديات
  تُحل على ملف ثابت.

## كيف تُعيد بناء كل التحديات دفعة واحدة

```bash
for d in 01-*/ 02-*/ 03-*/ 04-*/ 05-*/ 06-*/ 07-*/ 08-*/ 09-*/ 10-*/; do
  echo "==> $d"
  if [ -f "$d/solution_scripts/build.py" ]; then
    python3 "$d/solution_scripts/build.py"
  elif [ -f "$d/solution_scripts/build.sh" ]; then
    bash "$d/solution_scripts/build.sh"
  fi
done
```

## المتطلبات

```bash
sudo apt install -y exiftool dosfstools sleuthkit binwalk foremost \
                    photorec wireshark-common
pip3 install --user --break-system-packages pyfatfs
# scapy و Pillow مثبتتان مسبقًا في Kali
```
