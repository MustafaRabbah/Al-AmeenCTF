#!/usr/bin/env python3
"""Reference solver for Challenge 04 - Pixel Whisper.

Reads the LSB of the red channel (MSB-first), parses the 16-bit
length prefix and prints the recovered payload.
"""
from PIL import Image
import os, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(__file__), "..", "evidence", "whisper.png")


def main() -> None:
    img = Image.open(PATH).convert("RGB")
    w, h = img.size
    px  = img.load()
    bits = []
    for y in range(h):
        for x in range(w):
            bits.append(px[x, y][0] & 1)
    by = bytearray()
    for i in range(0, len(bits) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits[i + j]
        by.append(b)
    length = int.from_bytes(by[:2], "big")
    print(by[2:2 + length].decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
