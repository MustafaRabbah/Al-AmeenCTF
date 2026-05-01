#!/usr/bin/env python3
"""Builder for Challenge 05 - Disk Ghost.

Builds a FAT12 disk image, writes some legitimate-looking case files
plus `flag.txt`, then deletes flag.txt so its data still lingers in
the data area while the directory entry is marked deleted (0xE5).

Recovery techniques (any of these works):
  - The Sleuth Kit:   `fls -r -d image`  then  `icat image <inode>`
  - PhotoRec:         `photorec image`
  - Foremost:         `foremost -i image -o out`
  - Hex viewer:       `xxd image | grep AU-CS`
"""
import os
import struct
import subprocess
import tempfile

from pyfatfs.PyFatFS import PyFatFS

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EV   = os.path.join(BASE, "evidence")
IMG  = os.path.join(EV, "case_drive.img")
FLAG = "AU-CS{medium_deleted_but_recoverable}"


def make_blank(path: str, kib: int = 1440) -> None:
    with open(path, "wb") as f:
        f.truncate(kib * 1024)
    subprocess.run(
        ["mkfs.fat", "-F", "12", "-n", "EVIDENCE", path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def populate(path: str) -> None:
    fs = PyFatFS(path)
    fs.writebytes(
        "/notes.txt",
        b"CASE 0042\r\nUNIT: Field 3\r\nDATE: 2025-09-14\r\n"
        b"STATUS: closed (preliminary)\r\n"
        b"NOTE: chain of custody intact.\r\n",
    )
    fs.writebytes(
        "/users.csv",
        b"name,role,department\r\n"
        b"admin,operator,lab\r\n"
        b"viewer,read-only,front-desk\r\n"
        b"auditor,review,external\r\n",
    )
    fs.writebytes(
        "/inventory.txt",
        b"Lab inventory snapshot:\r\n"
        b"  - 1x DSLR camera\r\n"
        b"  - 1x analyst laptop\r\n"
        b"  - 3x USB sticks\r\n"
        b"  - 1x faraday bag\r\n",
    )
    fs.writebytes(
        "/photo.bin",
        b"\xff\xd8\xff\xe0DECOY_PHOTO_HEADER_FOR_TRAINING_ONLY\x00",
    )
    fs.writebytes("/flag.txt", (FLAG + "\n").encode())
    fs.close()


def soft_delete_flag(path: str) -> None:
    """Mark `flag.txt` directory entry as deleted (0xE5) without
    wiping the data clusters or zero-ing the FAT chain. This is the
    canonical 'recoverable delete' state for forensic exercises."""
    with open(path, "r+b") as f:
        bpb = f.read(36)
        bytes_per_sec = struct.unpack_from("<H", bpb, 11)[0]
        sec_per_clus  = struct.unpack_from("<B", bpb, 13)[0]
        rsvd_sec      = struct.unpack_from("<H", bpb, 14)[0]
        n_fats        = struct.unpack_from("<B", bpb, 16)[0]
        root_entries  = struct.unpack_from("<H", bpb, 17)[0]
        fat_size      = struct.unpack_from("<H", bpb, 22)[0]
        root_dir_off  = (rsvd_sec + n_fats * fat_size) * bytes_per_sec
        root_dir_sz   = root_entries * 32

        f.seek(root_dir_off)
        root = bytearray(f.read(root_dir_sz))

        for i in range(0, root_dir_sz, 32):
            entry = root[i:i + 32]
            if not entry or entry[0] in (0x00, 0xE5):
                continue
            attr = entry[11]
            if attr & 0x0F == 0x0F:
                continue
            name = bytes(entry[0:8]).rstrip(b" ")
            ext  = bytes(entry[8:11]).rstrip(b" ")
            full = name + (b"." + ext if ext else b"")
            if full.upper() == b"FLAG.TXT":
                root[i] = 0xE5
                f.seek(root_dir_off + i)
                f.write(bytes([0xE5]))
                print(f"[+] marked dir entry @0x{root_dir_off + i:x} as deleted")
                break
        else:
            raise RuntimeError("flag.txt directory entry not found")


if __name__ == "__main__":
    os.makedirs(EV, exist_ok=True)
    if os.path.exists(IMG):
        os.remove(IMG)
    make_blank(IMG)
    populate(IMG)
    soft_delete_flag(IMG)
    print(f"[+] built {IMG} ({os.path.getsize(IMG)} bytes)")
