#!/usr/bin/env bash
# Builder for Challenge 05 - Disk Ghost.
# Creates a small FAT12 image, writes several decoy files plus a
# `flag.txt` containing the real flag, then deletes flag.txt so its
# data still lingers in unallocated space. Players use TSK
# (`fls -r -d`, `icat`), photorec, foremost, or a hex viewer.

set -euo pipefail
BASE="$(cd "$(dirname "$0")"/.. && pwd)"
EV="$BASE/evidence"
IMG="$EV/case_drive.img"
MNT="$(mktemp -d)"
FLAG='AU-CS{medium_deleted_but_recoverable}'

mkdir -p "$EV"
rm -f "$IMG"
dd if=/dev/zero of="$IMG" bs=1024 count=2048 status=none
mkfs.fat -F 12 -n "EVIDENCE" "$IMG" >/dev/null

sudo -n true 2>/dev/null && SUDO=sudo || SUDO=

if command -v mtools >/dev/null 2>&1 || command -v mcopy >/dev/null 2>&1; then
  TMPDIR_FILES="$(mktemp -d)"
  printf 'CASE 0042\nUNIT: Field 3\nDATE: 2025-09-14\nSTATUS: closed\n' \
    > "$TMPDIR_FILES/notes.txt"
  printf 'name,value\nuser,admin\nrole,viewer\n' > "$TMPDIR_FILES/users.csv"
  printf 'Lab inventory\n- camera\n- laptop\n- USB stick\n' \
    > "$TMPDIR_FILES/inventory.txt"
  printf '%s\n' "$FLAG" > "$TMPDIR_FILES/flag.txt"
  printf '\xFF\xD8\xFF\xE0THIS_IS_A_DECOY_BLOCK_FOR_FORENSICS_TRAINING' \
    > "$TMPDIR_FILES/photo.bin"

  mcopy -i "$IMG" "$TMPDIR_FILES/notes.txt"     ::/notes.txt
  mcopy -i "$IMG" "$TMPDIR_FILES/users.csv"     ::/users.csv
  mcopy -i "$IMG" "$TMPDIR_FILES/inventory.txt" ::/inventory.txt
  mcopy -i "$IMG" "$TMPDIR_FILES/flag.txt"      ::/flag.txt
  mcopy -i "$IMG" "$TMPDIR_FILES/photo.bin"     ::/photo.bin
  mdel  -i "$IMG" ::/flag.txt
  rm -rf "$TMPDIR_FILES"
  echo "[+] populated and deleted flag via mtools"
else
  echo "[!] mtools not present, falling back to loop-mount (needs sudo)" >&2
  $SUDO mount -o loop "$IMG" "$MNT"
  echo 'CASE 0042'           | $SUDO tee "$MNT/notes.txt"     >/dev/null
  echo 'name,value'          | $SUDO tee "$MNT/users.csv"     >/dev/null
  echo 'Lab inventory'       | $SUDO tee "$MNT/inventory.txt" >/dev/null
  echo "$FLAG"               | $SUDO tee "$MNT/flag.txt"      >/dev/null
  $SUDO sync
  $SUDO rm "$MNT/flag.txt"
  $SUDO sync
  $SUDO umount "$MNT"
fi
rmdir "$MNT" 2>/dev/null || true

echo "[+] built $IMG"
ls -la "$IMG"
