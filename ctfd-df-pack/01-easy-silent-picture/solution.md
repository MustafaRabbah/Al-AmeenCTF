# طريقة الحل - الصورة الصامتة

## الفكرة
العلم مُخزّن داخل حقل **EXIF UserComment** الموجود في رأس الصورة.
المهارة المطلوبة: قراءة البيانات الوصفية بدل الاعتماد على المحتوى المرئي.

## خطوات الحل
1. شغّل `exiftool` على الملف:

   ```bash
   exiftool evidence_001.jpg
   ```
2. ابحث في الإخراج عن الحقول النصية وخاصة:
   - `User Comment`
   - `Image Description`
   - `XP Comment`
3. ستجد القيمة:
   ```
   User Comment : AU-CS{easy_exif_metadata_speaks}
   ```

## حل بديل (بدون exiftool)

```bash
strings evidence_001.jpg | grep -i 'AU-CS'
```

> النص محفوظ كـ ASCII داخل قطاع EXIF لذا `strings` كافية أيضًا.

## العلم
AU-CS{easy_exif_metadata_speaks}
