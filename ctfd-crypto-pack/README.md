# Simple Crypto Pack for CTFd

This package contains 7 crypto challenges (beginner to ultra hard) ready for manual upload to CTFd.

## Package layout

- `01-caesar-shift/`
- `02-double-base64/`
- `03-single-byte-xor/`
- `04-vigenere-basic/`
- `05-rail-fence/`
- `06-hard-keystream-collapse/`
- `07-ultra-shattered-secret/`
- `answer-key.md` (organizer-only)
- `ctfd-upload-cheatsheet.md`

## Quick upload workflow (CTFd)

For each challenge directory:

1. Open `description.md`
2. Create a new challenge in CTFd:
   - Category: `Crypto`
   - Type: `Standard`
   - Name/Value from `description.md`
   - Paste description body
3. Add the attached file from the `files/` directory
4. Add the flag exactly as shown in `answer-key.md`
5. Optional: add the hint listed in `description.md`

## Recommended scoring

- 01: 100
- 02: 100
- 03: 150
- 04: 150
- 05: 200
- 06: 400
- 07: 500

## Notes

- All flags use format: `AU-CS{...}`
- Keep `answer-key.md` private and do not publish it to players.
