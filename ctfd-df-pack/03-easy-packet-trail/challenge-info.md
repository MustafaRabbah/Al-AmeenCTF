# معلومات التحدي

- الاسم: أثر الحزم (Packet Trail)
- المستوى: سهل
- النقاط المقترحة: 150
- الفئة: Digital Forensics
- المهارة: تحليل PCAP وحركة HTTP
- المصمم: Mustafa Rabbah
- الملف المُسلّم للاعب: `evidence/capture.pcap`

## كيف يُسلّم التحدي على CTFd

ارفع `evidence/capture.pcap` كمرفق التحدي
ثم انسخ نص `description.md` في خانة الوصف.

## كيف يُعاد بناء الدليل

```bash
python3 solution_scripts/build.py
```

> يحتاج: `python3-scapy` (مثبتة بالفعل على Kali).
