# Al-AmeenCTF

مجموعة تحديات CTF جاهزة للاستخدام التعليمي والتنظيمي، مع تركيز على رفعها بسهولة إلى منصة **CTFd**.

## محتوى المستودع

- `ctfd-crypto-pack`  
  حزمة تحديات تشفير (Crypto) متدرجة من السهل إلى الصعب.

- `ctfd-rev-pack`  
  حزمة تحديات هندسة عكسية (Reverse Engineering) تشمل تحديات C/C++/Rust.

- `ctfd-df-pack`  
  حزمة تحديات إضافية (Digital Forensics / DF).

## الهدف من المشروع

- توفير تحديات عربية منظمة وجاهزة للنشر.
- تسهيل عمل منظّمي المسابقات عبر ملفات وصف وحلول واضحة.
- دعم التدريب العملي للطلاب والمبتدئين في الأمن السيبراني.

## البنية العامة لكل حزمة

غالبًا ستجد داخل كل تحدي:

- `description.md` لوصف التحدي على المنصة
- `challenge-info.md` لبيانات الصعوبة والنقاط
- `solution.md` للحل (Organizer Only)
- `src/` للكود أو الملفات المصدر
- ملفات المرفقات/التنفيذ بحسب نوع التحدي

## طريقة الاستخدام السريعة (CTFd)

1. ادخل إلى الحزمة المطلوبة.
2. افتح `description.md` لكل تحدي.
3. أنشئ Challenge جديد في CTFd وأضف:
   - الاسم
   - التصنيف
   - النقاط
   - الوصف
4. ارفع ملف التحدي/المرفقات إن وجدت.
5. أضف العلم الصحيح من `answer-key.md` (إن كان موجودًا داخل الحزمة).

## ملاحظات مهمة

- صيغة الأعلام في التحديات غالبًا: `AU-CS{...}`.
- ملف `answer-key.md` مخصص للمنظّم فقط ويجب عدم نشره للمتسابقين.
- يفضّل اختبار كل تحدٍ قبل النشر النهائي على المنصة.

## Repository

رابط المشروع على GitHub:  
[https://github.com/MustafaRabbah/Al-AmeenCTF](https://github.com/MustafaRabbah/Al-AmeenCTF)

## Web Challenges

رابط تحديات الويب (Live):  
[https://github.com/MustafaRabbah/alameen-web-challs-live](https://github.com/MustafaRabbah/alameen-web-challs-live)

## Social

Instagram:  
[https://www.instagram.com/0x8.9/](https://www.instagram.com/0x8.9/)

---

**Maintainer:** Mustafa Rabbah
