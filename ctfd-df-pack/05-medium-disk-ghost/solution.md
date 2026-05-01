# طريقة الحل - شبح القرص

## الفكرة
عند حذف ملف في FAT12/16/32 يتم وضع البايت الأول من اسمه في خانة
الفهرس بقيمة `0xE5`، ولكن **محتوى الكتل في منطقة البيانات يبقى كما هو**
حتى يُكتب فوقه. هذا يسمح باستراجاع الملف بسهولة طالما لم تُعَد الكتابة.

## خطوات الحل

### الخيار 1 - The Sleuth Kit (الأنظف)

```bash
fls -r -d case_drive.img         # يعرض كل الإدخالات المحذوفة
# مثال على الإخراج:
# r/r * 13:  flag.txt

icat case_drive.img 13           # يستخرج محتوى الـ inode
```

> الإشارة `*` تعني محذوف. الرقم بعدها هو رقم الإدخال.

### الخيار 2 - PhotoRec / foremost

```bash
mkdir out && photorec /d out/ case_drive.img
# أو
foremost -i case_drive.img -o out
```

### الخيار 3 - بحث خام في القرص

```bash
strings case_drive.img | grep -i 'AU-CS'
```

> العلم نص ASCII لذا يُلتقط مباشرة من الكتلة المحذوفة.

### الخيار 4 - تركيب القرص للقراءة فقط (يحتاج root)

```bash
sudo mount -o loop,ro case_drive.img /mnt/img
ls -la /mnt/img      # لن ترى flag.txt - تم حذفه على مستوى الفهرس
sudo umount /mnt/img
```

> هذا الخيار للتأكد فقط من أنه لا يوجد ملف ظاهر، ثم يجب اللجوء لأحد
> الخيارات السابقة.

## العلم
`AU-CS{medium_deleted_but_recoverable}`
