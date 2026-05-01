# طريقة الحل - طوفان الطلبات

## الفكرة
ملف الشبكة ضخم جدًا (1000+ طلب)، لذا الحل ليس بالتصفح اليدوي فقط.
المطلوب هو عزل endpoint الصحيح ثم جمع كلمات `word=` من تسلسل شرعي.

## خطوات التحليل

1. تأكيد حجم الحركة:
   ```bash
   tshark -r thousand_requests.pcap -Y 'http.request' | wc -l
   ```

2. البحث عن endpointات النادرة مقارنة بالضجيج:
   ```bash
   tshark -r thousand_requests.pcap -Y 'http.request' -T fields -e http.request.uri \
   | sort | uniq -c | sort -nr | head -40
   ```

3. ستركز على endpoint غير شائع:
   - `/api/intel/fragment`

4. استخراج السلسلة المرتبطة بنفس القضية:
   ```bash
   tshark -r thousand_requests.pcap \
     -Y 'http.request.uri contains "/api/intel/fragment?case=8841"' \
     -T fields -e ip.src -e http.request.uri
   ```

5. ستظهر طلبات متتالية تحتوي:
   - `seq=1&word=mustafa`
   - `seq=2&word=rabbah`
   - `seq=3&word=deep`
   - `seq=4&word=traffic`

6. ركب العلم حسب ترتيب `seq`.

## العلم النهائي
`AU-CS{mustafa_rabbah_deep_traffic}`

