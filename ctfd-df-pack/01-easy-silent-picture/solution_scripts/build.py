#!/usr/bin/env python3
"""Builder for Challenge 01 - Silent Picture.

Generates a JPEG image with EXIF metadata. The flag is hidden in the
EXIF UserComment field. Other realistic metadata is added so the
analyst must look at metadata, not just run `strings`.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidence")
OUT = os.path.abspath(os.path.join(OUT_DIR, "evidence_001.jpg"))
FLAG = "AU-CS{easy_exif_metadata_speaks}"


def make_image(path: str) -> None:
    img = Image.new("RGB", (640, 360), (18, 22, 36))
    draw = ImageDraw.Draw(img)
    for y in range(360):
        c = int(40 + (y / 360) * 60)
        draw.line([(0, y), (640, y)], fill=(c, c // 2, c // 3))
    draw.rectangle([(20, 20), (620, 340)], outline=(220, 220, 220), width=2)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28
        )
        small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16
        )
    except Exception:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    draw.text((40, 60), "AL-AMEEN CTF", fill=(255, 215, 0), font=font)
    draw.text((40, 110), "CASE FILE - EVIDENCE 001", fill=(220, 220, 220), font=font)
    draw.text((40, 170), "Photographed by: Field Unit 3", fill=(180, 180, 180), font=small)
    draw.text((40, 200), "Source: confiscated mobile device", fill=(180, 180, 180), font=small)
    draw.text((40, 280), "Designed by Mustafa Rabbah", fill=(120, 200, 255), font=small)
    img.save(path, "JPEG", quality=88)


def add_metadata(path: str) -> None:
    cmds = [
        ["exiftool", "-overwrite_original",
         "-Make=Canon", "-Model=Canon EOS R7",
         "-Software=Adobe Photoshop 24.0",
         "-Artist=Field Unit 3",
         "-DateTimeOriginal=2025:09:14 22:18:03",
         "-CreateDate=2025:09:14 22:18:03",
         "-ImageDescription=Routine inspection photo - sector 7",
         "-Copyright=Al-Ameen Forensic Lab",
         "-GPSLatitude=33.3152",   "-GPSLatitudeRef=N",
         "-GPSLongitude=44.3661",  "-GPSLongitudeRef=E",
         "-GPSAltitude=42",
         f"-UserComment={FLAG}",
         "-XPComment=Internal note: see UserComment for case ID",
         path],
    ]
    for c in cmds:
        subprocess.run(c, check=True)


if __name__ == "__main__":
    make_image(OUT)
    add_metadata(OUT)
    print(f"[+] built {OUT}")
