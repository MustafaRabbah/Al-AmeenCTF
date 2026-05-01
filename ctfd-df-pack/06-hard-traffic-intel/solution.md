# طريقة الحل - استخبارات المرور

## الفكرة
العلم غير موجود صريحًا داخل الملف. المطلوب جمع 4 قيم من عدة طلبات HTTP ثم
تركيبها بالصيغة:

`AU-CS{actor_caseid_failedlogins_exfilbytes}`

---

## 1) استخراج `actor`

فلتر Wireshark:
```
http.request.uri == "/api/login"
```

ستجد عدة محاولات `401 Unauthorized` ثم طلب نجاح يحتوي:
- `Authorization: Basic ...`

فك ترميز Basic token يعطي:
`nour.ops:BlueFalcon!26`

إذًا:
- `actor = nour.ops`

---

## 2) استخراج `caseid`

فلتر:
```
http.request.uri contains "/api/v2/export"
```

ستجد عدة طلبات تصدير (منها decoy مثل `case=9191`).
المطلوب اختيار الطلب المرتبط بنفس جلسة المهاجم الناجحة:
- `Cookie: session=s-9981`
- ويرجع `200 OK` مع `job=j-447`

الطلب الصحيح:
`/api/v2/export?case=7419&fmt=csv`

إذًا:
- `caseid = 7419`

---

## 3) حساب `failedlogins`

لا تعد جميع محاولات الفشل عشوائيًا.
احسب فقط محاولات فشل نفس `actor` (`nour.ops`) قبل أول نجاح له (`200 OK`):
- عدّ طلبات `/api/login` التي رجعت `401 Unauthorized`.

النتيجة:
- `failedlogins = 3`

---

## 4) استخراج `exfilbytes`

فلتر:
```
http.request.uri == "/api/v2/upload"
```

ستجد أكثر من رفع (`/api/v2/upload`) ومن ضمنها Upload مزيف.
اختر فقط الطلب المرتبط بنفس السلسلة:
- نفس `session=s-9981`
- نفس `X-Job: j-447` القادم من export الصحيح

من هذا الطلب الصحيح:
- `Content-Length: 867`

إذًا:
- `exfilbytes = 867`

---

## تركيب العلم

```
AU-CS{nour.ops_7419_3_867}
```

## العلم النهائي
`AU-CS{nour.ops_7419_3_867}`

