# معلومات التحدي

- الاسم: الصورة الصامتة (Silent Picture)
- المستوى: سهل
- النقاط المقترحة: 100
- الفئة: Digital Forensics
- المهارة: تحليل البيانات الوصفية (EXIF / Metadata)
- المصمم: Mustafa Rabbah
- الملف المُسلّم للاعب: `evidence/evidence_001.jpg`

## كيف يُسلّم التحدي على CTFd

ارفع الملف `evidence/evidence_001.jpg` كـ **مرفق** للتحدي،
ثم انسخ نص `description.md` في خانة الوصف.

## كيف يُعاد بناء الدليل

```bash
python3 solution_scripts/build.py
```

> يحتاج: `python3-pil`, `exiftool`.
