#!/usr/bin/env python3
"""OGRS — pack the 34 wearable inventory icons into Authentic_Sprites.orsc.

Reads the mapping from gen-wearables-batch.py so the sprite IDs stay
in lockstep with the YAMLs. Same blob format as
scripts/art/pack-router-sprites.py and pack-ui-sprites.py — a 25-byte
sprite header followed by ARGB pixel data.

Run AFTER scripts/art/gen-wearables-batch.py has generated the YAMLs;
that script is the single source of truth for which PNG goes at which
sprite ID.
"""
from __future__ import annotations
import shutil
import struct
import sys
import zipfile
from pathlib import Path
from PIL import Image

# Reuse the mapping defined in the generator (avoid drift).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module
gen = import_module("gen-wearables-batch")

REPO = Path(__file__).resolve().parents[2]
ARCHIVE = REPO / "client" / "Cache" / "video" / "Authentic_Sprites.orsc"
BACKUP = ARCHIVE.with_suffix(ARCHIVE.suffix + ".bak")
ART_ROOT = REPO / "art" / "items"
MIRROR = Path("/mnt/c/OGRS/Cache/video/Authentic_Sprites.orsc")

HEADER_FMT = ">IIbIIII"
HEADER_LEN = struct.calcsize(HEADER_FMT)


def slot_for(sprite_id: int) -> int:
    """Items live at cache slot 2150 + sprite_id."""
    return 2150 + sprite_id


def encode_blob(img: Image.Image) -> bytes:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    w, h = img.size
    pixels = img.tobytes()
    out = bytearray()
    # 32x32 icons. requiresShift=1, shifts=0, anchor=center (16,16).
    out += struct.pack(HEADER_FMT, w, h, 1, 0, 0, w // 2, h // 2)
    for i in range(0, len(pixels), 4):
        r, g, b, a = pixels[i], pixels[i + 1], pixels[i + 2], pixels[i + 3]
        out += bytes((a, r, g, b))
    return bytes(out)


def main() -> int:
    if not ARCHIVE.exists():
        print(f"FATAL: {ARCHIVE} not found", file=sys.stderr)
        return 1
    if not BACKUP.exists():
        shutil.copy2(ARCHIVE, BACKUP)
        print(f"Backed up archive -> {BACKUP}")

    with zipfile.ZipFile(BACKUP, "r") as zin:
        names = zin.namelist()
        entries = {n: zin.read(n) for n in names}

    added = 0
    skipped = 0
    for idx, w in enumerate(gen.ALL):
        sprite_id = gen.SPRITE_ID_BASE + idx
        slot = slot_for(sprite_id)
        png_path = ART_ROOT / w.sprite_dir / w.sprite_file
        if not png_path.exists():
            print(f"  WARN: missing {png_path}")
            skipped += 1
            continue
        img = Image.open(png_path)
        if img.size != (32, 32):
            # Resize if the source isn't already 32x32 — most inventory
            # icons render best at this size in the bag panel.
            img = img.resize((32, 32), Image.LANCZOS)
        blob = encode_blob(img)
        entries[str(slot)] = blob
        if str(slot) not in names:
            names.append(str(slot))
        added += 1
        print(f"  slot {slot} <- sprite.id={sprite_id}  {w.sprite_dir}/{w.sprite_file}")

    tmp = ARCHIVE.with_suffix(ARCHIVE.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, entries[n])
    tmp.replace(ARCHIVE)

    print(f"\nPacked {added} wearable icons into {ARCHIVE.name}.")
    if skipped:
        print(f"  ({skipped} skipped — check art/items/{w.sprite_dir}/ for the listed files)")

    if MIRROR.parent.exists():
        shutil.copy2(ARCHIVE, MIRROR)
        print(f"Mirrored to {MIRROR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
