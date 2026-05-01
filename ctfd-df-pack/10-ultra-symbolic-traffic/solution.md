# الحل - المرور الرمزي المتشظي

1. احصر الطلبات على trace الحقيقي:
   - `trace=ZX-7741-ULTRA`

2. استخرج XOR key من endpoint:
   - `/api/diag/known?trace=...`
   - known = `alpha`, cipher_hex يعطينا key = `0x37`

3. استخرج symbol map من:
   - `/api/diag/map?trace=...`

4. اجمع fragments من:
   - `/api/secure/fragment?trace=ZX-7741-ULTRA&seq=...&blob=...`
   - رتبها حسب `seq`.

5. فك blob:
   - decode symbols -> bytes
   - XOR بكل بايت مع `0x37`
   - الناتج كلمات: `mustafa ultra symbolic cipher mesh 10`

6. تركيب العلم:
`AU-CS{mustafa_ultra_symbolic_cipher_mesh_10}`

