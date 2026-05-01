# معلومات التحدي

- الاسم: استخبارات المرور (Traffic Intel)
- المستوى: صعب
- النقاط المقترحة: 300
- الفئة: Digital Forensics
- المهارة: Wireshark correlation / Network timeline analysis
- المصمم: Mustafa Rabbah
- الملف المُسلّم للاعب: `evidence/traffic_intel.pcap`

## كيف يُسلّم التحدي على CTFd

ارفع `evidence/traffic_intel.pcap` كمرفق للتحدي
ثم انسخ نص `description.md` في خانة الوصف.

## كيف يُعاد بناء الدليل

```bash
python3 solution_scripts/build.py
```

> يحتاج: `python3-scapy`, `wireshark`/`tshark` للتحقق.

