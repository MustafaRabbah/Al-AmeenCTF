# معلومات التحدي

- الاسم: همس البكسلات (Pixel Whisper)
- المستوى: متوسط
- النقاط المقترحة: 200
- الفئة: Digital Forensics
- المهارة: Steganography (LSB)
- المصمم: Mustafa Rabbah
- الملف المُسلّم للاعب: `evidence/whisper.png`

## كيف يُسلّم التحدي على CTFd

ارفع `evidence/whisper.png` كمرفق التحدي
ثم انسخ نص `description.md` في خانة الوصف.

## كيف يُعاد بناء الدليل

```bash
python3 solution_scripts/build.py    # يبني whisper.png
python3 solution_scripts/extract.py  # يستخرج العلم للتحقق
```

> يحتاج: `python3-pil`.
