#!/usr/bin/env python3
"""Builder for Challenge 04 - Pixel Whisper.

Embeds the flag inside the least-significant bit of a PNG image's
red-channel pixels, MSB-first, prefixed with a 16-bit big-endian
length. The format is intentionally simple so a smart analyst can
either:
  - Spot a `zsteg` finding (b1,r,msb), or
  - Write a tiny Python script using PIL to extract.

The cover image is a synthetic noisy gradient so the LSB pattern
isn't trivially visible to the naked eye but extraction is reliable.
"""
from PIL import Image
import os, random

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT  = os.path.join(BASE, "evidence", "whisper.png")
FLAG = "AU-CS{medium_lsb_red_channel_msb}"
SIZE = (480, 320)


def build_cover() -> Image.Image:
    random.seed(0xA1A2)
    img = Image.new("RGB", SIZE)
    px = img.load()
    w, h = SIZE
    for y in range(h):
        for x in range(w):
            r = (x * 255 // w + random.randint(0, 12)) & 0xFF
            g = ((x + y) * 255 // (w + h) + random.randint(0, 12)) & 0xFF
            b = (y * 255 // h + random.randint(0, 12)) & 0xFF
            px[x, y] = (r, g, b)
    return img


def embed(img: Image.Image, payload: bytes) -> Image.Image:
    head = len(payload).to_bytes(2, "big")
    blob = head + payload
    bits = []
    for byte in blob:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    px = img.load()
    w, h = img.size
    if len(bits) > w * h:
        raise ValueError("payload too large")
    it = iter(bits)
    done = False
    for y in range(h):
        if done: break
        for x in range(w):
            try:
                bit = next(it)
            except StopIteration:
                done = True
                break
            r, g, b = px[x, y]
            r = (r & 0xFE) | bit
            px[x, y] = (r, g, b)
    return img


if __name__ == "__main__":
    cover = build_cover()
    stego = embed(cover, FLAG.encode())
    stego.save(OUT, "PNG", optimize=True)
    print(f"[+] wrote {OUT}")
