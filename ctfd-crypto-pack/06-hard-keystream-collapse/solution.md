# طريقة الحل - انهيار تيار المفتاح

## الفكرة
التحدي مبني على **إعادة استخدام نفس تيار التشفير** (same keystream reuse)
مع ملف معروف المحتوى وملف حساس.

لدينا:
- `known_plain.txt` (نص معروف)
- `known_plain.enc` (تشفيره بنفس التيار)
- `vault.enc` (هدفنا)
- `meta.json` يحتوي `stream_offset_for_vault`

## المبدأ
في التشفير التياري:
`C = P XOR K`
إذًا:
`K = P XOR C`

من الملف المعروف نستخرج `K`، ثم نأخذ الجزء المناسب حسب `offset` ونفك:
`vault_plain = vault_enc XOR K[offset:offset+len(vault_enc)]`

## سكربت حل سريع (Python)

```python
import json

with open("known_plain.txt","rb") as f:
    p = f.read()
with open("known_plain.enc","rb") as f:
    c = f.read()
with open("vault.enc","rb") as f:
    v = f.read()
with open("meta.json","r",encoding="utf-8") as f:
    m = json.load(f)

offset = m["stream_offset_for_vault"]
ks = bytes([a ^ b for a,b in zip(p,c)])
out = bytes([v[i] ^ ks[offset+i] for i in range(len(v))])
print(out.decode())
```

## العلم
`AU-CS{hard_crypto_keystream_reuse_collapse}`

