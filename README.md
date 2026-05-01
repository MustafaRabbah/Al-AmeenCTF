# Al-AmeenCTF

## العربية

مشروع **Al-AmeenCTF** هو مجموعة حزم تحديات أمن سيبراني تعليمية، مصممة لتخدم التدريب العملي وتنظيم المسابقات.

### نظرة عامة

- إجمالي الحزم الحالية: **3**
- إجمالي التحديات التقريبي: **26+ تحديًا**
- التخصصات: **Crypto / Reverse Engineering / Digital Forensics**
- مستويات الصعوبة: من **Easy** إلى **Ultra+**
- صيغة الأعلام المعتمدة: `AU-CS{...}`

### محتوى المستودع

- `ctfd-crypto-pack`  
  حزمة تشفير تحتوي **7 تحديات** من الأساسيات حتى المستوى المتقدم جدًا.

- `ctfd-rev-pack`  
  حزمة هندسة عكسية تحتوي **9 تحديات** تشمل ملفات وكود من C/C++/Rust، مع حالات anti-debug وتحديات تحليل ديناميكي في المستويات العليا.

- `ctfd-df-pack`  
  حزمة تحقيق جنائي رقمي تحتوي **10 تحديات** تشمل EXIF، carving، PCAP analysis، timeline correlation، وتحليل أدلة متعددة المصادر.

### بنية التحديات داخل الحزم

غالبًا ستجد في كل تحدٍ:

- `description.md` وصف التحدي
- `challenge-info.md` معلومات الفئة والصعوبة والنقاط
- `solution.md` حل تفصيلي (للمنظّم فقط)
- `src/` أو `evidence/` حسب نوع التحدي
- `answer-key.md` على مستوى الحزمة (للمنظّم فقط)

### ملاحظات مهمة

- بعض تحديات المستوى العالي تحتوي تشويشًا مقصودًا (Obfuscation) أو آليات مقاومة تحليل.
- تحديات DF مبنية بطريقة قابلة لإعادة التوليد (reproducible) عبر سكربتات.
- يجب إبقاء ملفات الحلول ومفاتيح الإجابات خاصة بالمنظّم.

---

## English

**Al-AmeenCTF** is a curated collection of cybersecurity CTF challenge packs built for learning, hands-on practice, and competition organization.

### Overview

- Current packs: **3**
- Approximate total challenges: **26+**
- Categories: **Crypto / Reverse Engineering / Digital Forensics**
- Difficulty range: **Easy** to **Ultra+**
- Standard flag format: `AU-CS{...}`

### Repository Contents

- `ctfd-crypto-pack`  
  A crypto pack with **7 challenges**, from beginner-level concepts to advanced scenarios.

- `ctfd-rev-pack`  
  A reverse engineering pack with **9 challenges** across C/C++/Rust, including anti-debug logic and advanced dynamic analysis styles.

- `ctfd-df-pack`  
  A digital forensics pack with **10 challenges**, covering EXIF, file carving, PCAP analysis, timeline reconstruction, and multi-source correlation.

### Challenge Structure

Most challenges include:

- `description.md` challenge description
- `challenge-info.md` category, difficulty, and scoring info
- `solution.md` organizer-only walkthrough
- `src/` or `evidence/` depending on challenge type
- `answer-key.md` at pack level (organizer-only)

### Notes

- High-difficulty challenges may include intentional obfuscation and anti-analysis behavior.
- DF challenge evidence is generally generated in a reproducible way using scripts.
- Keep all solution and answer-key files private from players.

## Links

- Main Repository: [https://github.com/MustafaRabbah/Al-AmeenCTF](https://github.com/MustafaRabbah/Al-AmeenCTF)
- Web Challenges (Live): [https://github.com/MustafaRabbah/alameen-web-challs-live](https://github.com/MustafaRabbah/alameen-web-challs-live)
- Instagram: [https://www.instagram.com/0x8.9/](https://www.instagram.com/0x8.9/)

---

**Maintainer:** Mustafa Rabbah
