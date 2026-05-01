# طريقة الحل - أثر الحادثة

## الفكرة
التحدي يعتمد على correlation زمني بين عدة مصادر غير شبكية.
الدليل الأساسي هو تتبع `evt=IR-7741` ثم استخراج الكلمات من نقاط مفصلية.

## خطوات التحليل

1. فك الضغط:
   ```bash
   unzip incident_bundle.zip
   cd incident_bundle
   ```

2. تتبع الحدث:
   ```bash
   rg "IR-7741" .
   ```

3. النتائج المهمة:
   - من `logs/auth.log`:
     - المستخدم المرتبط بالحدث = `mustafa`
   - من `logs/usb-events.log`:
     - USB label = `forensic`
   - من `system/cron.txt`:
     - `--tag=shadow`  -> الكلمة الثالثة `shadow`
   - من `system/bash_history.txt`:
     - اسم الملف النهائي `.shadow.trail` -> الكلمة الرابعة `trail`

4. تركيب العلم بالترتيب الزمني:
   - `mustafa`
   - `forensic`
   - `shadow`
   - `trail`

## العلم النهائي
`AU-CS{mustafa_forensic_shadow_trail}`

