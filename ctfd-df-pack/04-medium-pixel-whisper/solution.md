# طريقة الحل - همس البكسلات

## الفكرة
العلم مُخبّأ في **أصغر بت من قناة الأحمر** لكل بكسل، بترتيب القراءة
من اليسار لليمين، أعلى-لأسفل. أول 16 بت تُمثّل **طول** الحمولة بـ
`big-endian`، يليها بايتات النص بترتيب `MSB-first`.

## خطوات الحل

### الخيار 1 - zsteg (أسرع طريقة)

```bash
zsteg -a whisper.png | grep -i 'AU-CS'
```

ستجد سطرًا مشابهًا:

```
b1,r,msb,xy   text: "...AU-CS{medium_lsb_red_channel_msb}..."
```

### الخيار 2 - سكربت بايثون مخصص

```python
from PIL import Image
img = Image.open("whisper.png").convert("RGB")
w, h = img.size
bits = [img.getpixel((x, y))[0] & 1 for y in range(h) for x in range(w)]

def bits_to_bytes(bs):
    out = bytearray()
    for i in range(0, len(bs) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bs[i + j]
        out.append(b)
    return out

raw = bits_to_bytes(bits)
length = int.from_bytes(raw[:2], "big")
print(raw[2:2 + length].decode())
```

### الخيار 3 - StegSolve (واجهة رسومية)
استخدم `Image Combiner` و معاينة الـ Bit Plane = `Red 0`، ثم قم بفك
السلسلة الناتجة كنص.

## العلم
`AU-CS{medium_lsb_red_channel_msb}`
