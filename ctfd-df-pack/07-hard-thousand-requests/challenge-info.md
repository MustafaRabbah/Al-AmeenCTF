# معلومات التحدي

- الاسم: طوفان الطلبات
- المستوى: صعب جدًا
- النقاط المقترحة: 350
- الفئة: Digital Forensics
- المهارة: Network Forensics / Large PCAP Correlation
- المصمم: Mustafa Rabbah
- الملف المُسلّم للاعب: `evidence/thousand_requests.pcap`

## كيف يُسلّم التحدي على CTFd

ارفع `evidence/thousand_requests.pcap` كمرفق التحدي
ثم انسخ نص `description.md` في خانة الوصف.

## كيف يُعاد بناء الدليل

```bash
python3 solution_scripts/build.py
```

> يحتاج: `python3-scapy`, `tshark`.

