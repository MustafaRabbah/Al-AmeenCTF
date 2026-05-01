# طريقة الحل - الذيل المخفي

## الفكرة
الملف هو PNG صالح ينتهي بمقطع `IEND`، لكن بعد هذا المقطع تم إلصاق
أرشيف ZIP يحتوي على `flag.txt`. التقنية تُسمى *file appending /
container concatenation* وكاشفها الأساسي هو فحص التوقيعات (signatures).

## خطوات الحل

### الخيار 1 - binwalk

```bash
binwalk report_cover.png
```

ستجد إخراجًا مشابهًا:

```
DECIMAL  HEXADECIMAL  DESCRIPTION
0        0x0          PNG image, ...
24521    0x5FC9       Zip archive data, ...
```

### استخراج المحتوى

```bash
binwalk -e report_cover.png
cat _report_cover.png.extracted/*/flag.txt
```

### الخيار 2 - foremost

```bash
foremost -i report_cover.png -o out
ls out/zip/
```

### الخيار 3 - يدوي عبر unzip

```bash
unzip report_cover.png
cat flag.txt
```

> `unzip` يطبع تحذيرًا "extra bytes at beginning" لكنه ينجح.

## العلم
`AU-CS{easy_zip_appended_after_png}`
