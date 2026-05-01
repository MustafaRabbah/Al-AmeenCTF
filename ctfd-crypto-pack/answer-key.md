# Organizer Answer Key (Private)

Do not share this file with players.

## 01) Caesar Starter

- Flag: `AU-CS{caesar_shift_seven_for_security_keyword}`
- Method: Caesar decrypt with shift `7`
- Cipher text: `HB-JZ{jhlzhy_zopma_zlclu_mvy_zljbypaf_rlfdvyk}`
- Note: Decryption output is the full flag directly

## 02) Base64 on Base64

- Flag: `AU-CS{double_base64_reveals_real_flag_text}`
- Method: Decode Base64 twice
- Encoded string: `UVZVdFExTjdaRzkxWW14bFgySmhjMlUyTkY5eVpYWmxZV3h6WDNKbFlXeGZabXhoWjE5MFpYaDBmUT09`

## 03) Tiny XOR

- Flag: `AU-CS{single_byte_xor_reveals_true_flag}`
- Method: Single-byte XOR brute force
- Key byte: `0x13`
- Cipher hex: `52463e504068607a7d747f764c716a67764c6b7c614c61766576727f604c676166764c757f72746e`

## 04) Vigenere Basic

- Flag: `AU-CS{vigenere_classic_key_reveals_flag_text}`
- Method: Vigenere decrypt
- Key: `KEY`
- Cipher text: `KY-AC{zgqilovc_mpycwgm_oci_vcfiyvw_dvee_divd}`
- Note: Decryption output is the full flag directly

## 05) Rail Fence Warmup

- Flag: `AU-CS{rail_fence_cipher_three_rails_full_flag}`
- Method: Rail Fence cipher decrypt with rails `3`
- Cipher text: `ASie_hteif_gUC{alfnecpe_he_al_ulfa}-r_cirrrsll`
- Note: Decryption output is the full flag directly

## 06) انهيار تيار المفتاح (Hard)

- Flag: `AU-CS{hard_crypto_keystream_reuse_collapse}`
- Method: Recover keystream from known plaintext pair, then decrypt `vault.enc` at provided offset.
- Files:
  - `known_plain.txt`
  - `known_plain.enc`
  - `vault.enc`
  - `meta.json` (contains `stream_offset_for_vault`)

## 07) السر المتشظي (Ultra)

- Flag: `AU-CS{mustafa_ultra_crypto_shattered_707}`
- Method: de-XOR each block with PRNG keystream, invert permutation, remove `#` padding.
- Files:
  - `cipher.bin`
  - `meta.json`
  - `perm.txt`
  - `note.txt`
