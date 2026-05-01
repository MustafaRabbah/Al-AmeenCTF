# Al-AmeenCTF

[![CTF](https://img.shields.io/badge/Type-CTF%20Challenges-111827?style=for-the-badge)](https://github.com/MustafaRabbah/Al-AmeenCTF)
[![Language](https://img.shields.io/badge/Content-Arabic%20%2B%20English-16a34a?style=for-the-badge)](https://github.com/MustafaRabbah/Al-AmeenCTF)
[![Difficulty](https://img.shields.io/badge/Difficulty-Easy%20to%20Ultra%2B-f59e0b?style=for-the-badge)](https://github.com/MustafaRabbah/Al-AmeenCTF)
[![Maintained](https://img.shields.io/badge/Status-Actively%20Maintained-2563eb?style=for-the-badge)](https://github.com/MustafaRabbah/Al-AmeenCTF)

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

### الفئة المستهدفة

- نوادي الأمن السيبراني في الجامعات والمعاهد.
- المدربون الذين يبنون مسارات تدريب عملية.
- منظّمو مسابقات CTF التعليمية.
- المتعلمون ذاتيًا الراغبون بالتدرج من الأساسيات إلى التحديات المتقدمة.

### المهارات التي تغطيها التحديات

- **Crypto:** Caesar/Vigenere/XOR، تحليل أنماط التشفير، كسر مفاتيح بسيطة إلى متوسطة.
- **Reverse:** Static analysis، dynamic tracing، فهم الـ control flow، وفك منطق التحقق.
- **DF:** Metadata analysis، file carving، network forensics، وبناء timeline للتحقيق.

### المتطلبات العامة (حسب نوع التحدي)

- Linux environment (Kali/Ubuntu recommended).
- أدوات تحليل مثل: `gdb`, `strings`, `objdump`, `ghidra`, `wireshark`, `binwalk`.
- Python 3 للتشغيل المساعد والسكربتات.

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

### Target Audience

- University cybersecurity clubs and lab instructors.
- Trainers building structured hands-on tracks.
- Organizers running educational CTF events.
- Self-learners progressing from fundamentals to advanced challenge styles.

### Skills Covered

- **Crypto:** Caesar/Vigenere/XOR basics, cipher pattern analysis, practical key recovery workflows.
- **Reverse:** Static and dynamic analysis, control-flow reasoning, and validation bypass understanding.
- **DF:** Metadata extraction, file carving, network forensics, and incident timeline reconstruction.

### General Requirements (by challenge type)

- Linux environment (Kali/Ubuntu recommended).
- Common tools: `gdb`, `strings`, `objdump`, `ghidra`, `wireshark`, `binwalk`.
- Python 3 for helper scripts and reproducible challenge generation.

### Ethical Use

- This repository is intended for legal educational use only.
- Do not use techniques from these challenges against systems you do not own or have explicit permission to test.

## Links | الروابط

### العربية

- المستودع الرئيسي  
  [![GitHub Repo](https://img.shields.io/badge/GitHub-Al--AmeenCTF-181717?style=for-the-badge&logo=github)](https://github.com/MustafaRabbah/Al-AmeenCTF)

- تحديات الويب (Live)  
  [![Web Challenges](https://img.shields.io/badge/Web-Challenges%20Live-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white)](https://github.com/MustafaRabbah/alameen-web-challs-live)

- حسابي على Instagram  
  [![Instagram](https://img.shields.io/badge/Instagram-0x8.9-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/0x8.9/)

### English

- Main Repository  
  [![GitHub Repo](https://img.shields.io/badge/GitHub-Al--AmeenCTF-181717?style=for-the-badge&logo=github)](https://github.com/MustafaRabbah/Al-AmeenCTF)

- Web Challenges (Live)  
  [![Web Challenges](https://img.shields.io/badge/Web-Challenges%20Live-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white)](https://github.com/MustafaRabbah/alameen-web-challs-live)

- Instagram  
  [![Instagram](https://img.shields.io/badge/Instagram-0x8.9-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/0x8.9/)

---

**Maintainer:** Mustafa Rabbah
