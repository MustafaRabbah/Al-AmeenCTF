#!/usr/bin/env python3
import os, random, json, hashlib, base64

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVID = os.path.join(BASE, "evidence")
FLAG = "AU-CS{mustafa_ultra_crypto_shattered_707}"
os.makedirs(EVID, exist_ok=True)

secret = FLAG.encode()
perm = [7, 2, 11, 0, 15, 4, 9, 1, 13, 6, 3, 14, 5, 10, 8, 12]
while len(secret) % 16:
    secret += b"#"
blocks = [secret[i:i+16] for i in range(0, len(secret), 16)]

def prng(seed, n):
    x = seed & 0xffffffff
    out = []
    for _ in range(n):
        x = (1103515245 * x + 12345) & 0xffffffff
        out.append((x >> 16) & 0xff)
    return bytes(out)

seed = 0x707A11
cipher_blocks = []
for bi, b in enumerate(blocks):
    p = bytes([b[perm[i]] for i in range(16)])
    ks = prng(seed ^ bi ^ 0xA5A5, 16)
    c = bytes([p[i] ^ ks[i] for i in range(16)])
    cipher_blocks.append(c)

blob = b"".join(cipher_blocks)
with open(os.path.join(EVID, "cipher.bin"), "wb") as f:
    f.write(blob)

decoy = base64.b64encode(hashlib.sha256(b"wrong_chain").digest()).decode()
with open(os.path.join(EVID, "note.txt"), "w") as f:
    f.write("Use seed from meta, invert permutation, then unpad #.\n")
    f.write("decoy=" + decoy + "\n")

meta = {
    "seed_hint": "0x707A11",
    "perm_hash": hashlib.md5(bytes(perm)).hexdigest(),
    "block_size": 16,
    "padding": "#",
}
with open(os.path.join(EVID, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

with open(os.path.join(EVID, "perm.txt"), "w") as f:
    f.write("7,2,11,0,15,4,9,1,13,6,3,14,5,10,8,12\n")

print("[+] built crypto ultra evidence")
print("[+] flag:", FLAG)

