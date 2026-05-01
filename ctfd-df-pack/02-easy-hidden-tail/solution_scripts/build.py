#!/usr/bin/env python3
"""Builder for Challenge 02 - Hidden Tail.

Creates a normal-looking PNG image, then appends a ZIP archive at the
end of the file. The ZIP contains `flag.txt` and a small README. The
PNG still opens normally in any image viewer; players must spot the
appended archive (binwalk / foremost / hex inspection).
"""
from PIL import Image, ImageDraw, ImageFont
import os, io, zipfile, struct

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVID = os.path.join(BASE, "evidence")
OUT  = os.path.join(EVID, "report_cover.png")
FLAG = "AU-CS{easy_zip_appended_after_png}"


def make_png(path: str) -> None:
    img = Image.new("RGB", (700, 400), (245, 245, 230))
    d = ImageDraw.Draw(img)
    d.rectangle([(10, 10), (690, 390)], outline=(40, 40, 40), width=2)
    try:
        big = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        mid = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        sml = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        big = mid = sml = ImageFont.load_default()
    d.text((40, 50),  "AL-AMEEN FORENSIC LAB",       fill=(20, 60, 110), font=big)
    d.text((40, 110), "Case Report Cover - 0042",   fill=(60, 60, 60),  font=mid)
    d.text((40, 160), "Status: closed (preliminary)", fill=(120, 0, 0), font=mid)
    d.text((40, 230), "Notes:", fill=(0, 0, 0), font=mid)
    d.text((60, 270), "- evidence collected on site", fill=(40, 40, 40), font=sml)
    d.text((60, 295), "- chain of custody intact",     fill=(40, 40, 40), font=sml)
    d.text((60, 320), "- no further action required",  fill=(40, 40, 40), font=sml)
    d.text((40, 360), "Designed by Mustafa Rabbah",    fill=(0, 110, 90), font=sml)
    img.save(path, "PNG", optimize=True)


def append_zip(path: str) -> None:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("flag.txt", FLAG + "\n")
        z.writestr("README.txt",
                   "Recovered from PNG tail.\n"
                   "Skill: file carving - signatures matter.\n")
    payload = buf.getvalue()
    with open(path, "ab") as f:
        f.write(payload)


if __name__ == "__main__":
    make_png(OUT)
    append_zip(OUT)
    print(f"[+] built {OUT}, size={os.path.getsize(OUT)} bytes")
