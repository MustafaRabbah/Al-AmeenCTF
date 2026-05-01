# معلومات التحدي

- الاسم: الذيل المخفي (Hidden Tail)
- المستوى: سهل
- النقاط المقترحة: 125
- الفئة: Digital Forensics
- المهارة: File Carving / تحليل توقيعات الملفات
- المصمم: Mustafa Rabbah
- الملف المُسلّم للاعب: `evidence/report_cover.png`

## كيف يُسلّم التحدي على CTFd

ارفع `evidence/report_cover.png` كمرفق التحدي
ثم انسخ نص `description.md` في خانة الوصف.

## كيف يُعاد بناء الدليل

```bash
python3 solution_scripts/build.py
```

> يحتاج: `python3-pil`، مكتبة `zipfile` المضمنة في بايثون.
