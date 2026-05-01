# معلومات التحدي

- الاسم: شبح القرص (Disk Ghost)
- المستوى: متوسط
- النقاط المقترحة: 225
- الفئة: Digital Forensics
- المهارة: Filesystem Forensics / استرجاع ملفات محذوفة من FAT
- المصمم: Mustafa Rabbah
- الملف المُسلّم للاعب: `evidence/case_drive.img`

## كيف يُسلّم التحدي على CTFd

ارفع `evidence/case_drive.img` كمرفق التحدي
ثم انسخ نص `description.md` في خانة الوصف.

## كيف يُعاد بناء الدليل

```bash
python3 solution_scripts/build.py
```

> يحتاج: `mkfs.fat` (`dosfstools`) + `pip install pyfatfs`.
