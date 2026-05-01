# الحل
- block size = 16.
- لكل block: استخرج keystream من PRNG(seed ^ block_index ^ 0xA5A5).
- XOR لفك البلوك.
- اعكس permutation المعطاة في `perm.txt`.
- اجمع البلوكات ثم أزل padding `#`.
- العلم: `AU-CS{mustafa_ultra_crypto_shattered_707}`
