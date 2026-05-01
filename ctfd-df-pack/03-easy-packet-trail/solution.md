# طريقة الحل - أثر الحزم

## الفكرة
الـ PCAP يحتوي عدة جلسات HTTP (decoys كثيرة) لجعل التحليل أقرب للواقع.
الجلسة المهمة هي `POST /comment`، لكن العلم ليس نصًا صريحًا؛ تم وضعه
داخل الحقل `note_b64` بعد ترميزه Base64، لذلك لن يظهر مباشرة مع `strings`.

## خطوات الحل

### في Wireshark
1. افتح `capture.pcap`.
2. ضع الفلتر:
   ```
   http.request.method == "POST"
   ```
3. كليك يمين على الحزمة → `Follow → HTTP Stream`.
4. ستظهر بيانات النموذج:
   ```
   user=field_unit_3&case=0042&note_b64=QV...=&submit=send
   ```
5. انسخ قيمة `note_b64` وفكّها Base64:
   ```bash
   echo 'QVUtQ1N7ZWFzeV9odHRwX3Bvc3RfaW5fcGNhcH0=' | base64 -d
   ```

### عبر tshark (سطر أوامر)

```bash
tshark -r capture.pcap -Y 'http.request.method == "POST"' \
       -T fields -e http.file_data | xxd -r -p
```

ثم فك قيمة `note_b64`:

```bash
tshark -r capture.pcap -Y 'http.request.uri == "/comment"' \
  -T fields -e http.file_data \
| xxd -r -p \
| sed -n 's/.*note_b64=\([^&]*\).*/\1/p' \
| python3 -c 'import sys,base64;print(base64.b64decode(sys.stdin.read().strip()).decode())'
```

## العلم
`AU-CS{easy_http_post_in_pcap}`
