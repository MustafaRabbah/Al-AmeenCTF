#!/usr/bin/env python3
"""
Build hard crypto challenge: keystream reuse collapse.

Design:
- A custom stream cipher based on SHA-256(key || nonce || counter).
- Two plaintexts encrypted with the SAME key/nonce (fatal mistake).
- The first plaintext is fully known to the player.
- The second plaintext is the target encrypted file.
- A non-zero stream offset is used for the second file to increase complexity.
"""
import hashlib
import json
import os
from textwrap import dedent

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVID = os.path.join(BASE, "evidence")

FLAG = "AU-CS{hard_crypto_keystream_reuse_collapse}"

KEY = bytes.fromhex("f0a9c3d4117ee8ab5d9c02b4aa33219f")
NONCE = bytes.fromhex("52f42ab9e8019d7c")
OFFSET = 4096


def stream_bytes(length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        block = hashlib.sha256(KEY + NONCE + counter.to_bytes(8, "little")).digest()
        out.extend(block)
        counter += 1
    return bytes(out[:length])


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def main() -> None:
    os.makedirs(EVID, exist_ok=True)

    known_plain = dedent(
        """
        Al-Ameen Internal Security Memo
        =====================================
        This document is intentionally published as a known plaintext sample
        for interoperability tests between legacy and modern crypto pipelines.

        IMPORTANT:
        - Stream mode MUST use unique nonce per message.
        - Reusing the same key+nonce is catastrophic.
        - If two ciphertexts share keystream, one known plaintext can recover
          the stream and expose the second encrypted payload.

        Technical appendix:
        [A] stream chunking test vectors
        [B] deterministic parser baselines
        [C] migration notes for SOC archive

        End of published test memo.
        """
    ).strip().encode()

    # Make known plaintext very large so players can recover stream at high offsets
    known_plain = (known_plain + b"\n") * 300

    secret_plain = dedent(
        f"""
        {{
          "case_id": "CR-8841",
          "unit": "crypto-lab",
          "priority": "critical",
          "operator": "Mustafa Rabbah",
          "instruction": "assemble flag exactly",
          "flag": "{FLAG}"
        }}
        """
    ).strip().encode()

    ks = stream_bytes(OFFSET + max(len(known_plain), len(secret_plain)) + 64)
    known_enc = xor_bytes(known_plain, ks[: len(known_plain)])
    secret_enc = xor_bytes(secret_plain, ks[OFFSET : OFFSET + len(secret_plain)])

    with open(os.path.join(EVID, "known_plain.txt"), "wb") as f:
        f.write(known_plain)
    with open(os.path.join(EVID, "known_plain.enc"), "wb") as f:
        f.write(known_enc)
    with open(os.path.join(EVID, "vault.enc"), "wb") as f:
        f.write(secret_enc)

    meta = {
        "cipher": "custom-stream-v2",
        "hash_block": "sha256",
        "nonce": NONCE.hex(),
        "stream_offset_for_vault": OFFSET,
        "note": "legacy pipeline test export",
    }
    with open(os.path.join(EVID, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print("[+] built hard crypto challenge files")
    print(f"[+] flag: {FLAG}")


if __name__ == "__main__":
    main()

