#!/usr/bin/env python3
"""
OGRS — generate the in-game main-logo sprite (the wolf-replacement).

Sprite 2010 in Authentic_Sprites.orsc is the big banner shown on the
login screen + sleep + appearance views (drawn via GUIPARTS.MAINLOGO).
Original is 438x141 wolf art; we replace it with an OGRS-branded
banner: dark forest background, gold OGRS title, "Old Gielinor"
subtitle. Procedural PIL — keeps the art pipeline consistent.

The output PNG is packed into the archive by gen-mainlogo-pack
helper at the bottom of this script.
"""
import os
import struct
import shutil
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
ARCHIVE = REPO / "client" / "Cache" / "video" / "Authentic_Sprites.orsc"
BACKUP = ARCHIVE.with_suffix(ARCHIVE.suffix + ".bak")
SLOT = "2010"
W, H = 438, 141

BG_TOP        = (12, 24, 16)      # near-black forest at the top
BG_BOT        = (28, 56, 36)      # spruce green base
BORDER_OUTER  = (96, 64, 24)      # dark wood border
BORDER_INNER  = (212, 166, 74)    # gold accent
TITLE_GOLD    = (240, 196, 92)
TITLE_SHADOW  = (24, 16, 4)
SUBTITLE      = (220, 200, 168)


def find_font(size):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Vertical gradient background.
    for y in range(H):
        t = y / (H - 1)
        r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        d.line([(0, y), (W - 1, y)], fill=(r, g, b, 255))

    # Border frame.
    d.rectangle((0, 0, W - 1, H - 1), outline=BORDER_OUTER, width=3)
    d.rectangle((3, 3, W - 4, H - 4), outline=BORDER_INNER, width=1)

    # OGRS title — large.
    title = "OGRS"
    fsize = 72
    while fsize > 12:
        font = find_font(fsize)
        bbox = d.textbbox((0, 0), title, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if tw < W * 0.55 and th < H * 0.55:
            break
        fsize -= 2
    tx = (W - tw) // 2 - bbox[0]
    ty = 18
    # Drop shadow + main.
    d.text((tx + 3, ty + 3), title, font=font, fill=TITLE_SHADOW)
    d.text((tx, ty), title, font=font, fill=TITLE_GOLD)

    # Subtitle — "Old Gielinor"
    subtitle = "Old Gielinor"
    sfsize = 26
    sfont = find_font(sfsize)
    sbbox = d.textbbox((0, 0), subtitle, font=sfont)
    sw, sh = sbbox[2] - sbbox[0], sbbox[3] - sbbox[1]
    sx = (W - sw) // 2 - sbbox[0]
    sy = H - sh - 14
    d.text((sx + 2, sy + 2), subtitle, font=sfont, fill=TITLE_SHADOW)
    d.text((sx, sy), subtitle, font=sfont, fill=SUBTITLE)

    # Thin gold separator line between title + subtitle.
    sep_y = sy - 6
    d.line([(W // 4, sep_y), (3 * W // 4, sep_y)], fill=BORDER_INNER, width=1)

    return img


def encode_blob(img, header):
    """Encode in Sprite.unpack format. Header tuple from the original."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    w, h = img.size
    pixels = img.tobytes()
    out = bytearray()
    out += struct.pack(
        ">IIbIIII",
        w, h,
        header[2], header[3], header[4],
        header[5], header[6],
    )
    for i in range(0, len(pixels), 4):
        r, g, b, a = pixels[i], pixels[i + 1], pixels[i + 2], pixels[i + 3]
        out += bytes((a, r, g, b))
    return bytes(out)


def main():
    if not ARCHIVE.exists():
        raise SystemExit(f"missing archive: {ARCHIVE}")
    if not BACKUP.exists():
        shutil.copy2(ARCHIVE, BACKUP)

    # Read header from BACKUP (preserves original shift/something values
    # the engine expects for draw positioning), but READ ALL OTHER ENTRIES
    # FROM THE LIVE ARCHIVE so prior OGRS sprite patches (projectiles,
    # impacts, swirls, directionals) survive. Idempotent: re-running this
    # just overwrites slot SLOT with the same logo.
    with zipfile.ZipFile(BACKUP, "r") as zb:
        orig_header_bytes = zb.read(SLOT)[:25]
    header = struct.unpack(">IIbIIII", orig_header_bytes)
    print(f"Original header: w={header[0]} h={header[1]} "
          f"requires_shift={header[2]} xShift={header[3]} yShift={header[4]} "
          f"s1={header[5]} s2={header[6]}")

    img = render()
    print(f"Rendered logo: {img.size[0]}x{img.size[1]}")
    new_blob = encode_blob(img, header)

    with zipfile.ZipFile(ARCHIVE, "r") as zin:
        names = zin.namelist()
        entries = {n: zin.read(n) for n in names}
    entries[SLOT] = new_blob

    tmp = ARCHIVE.with_suffix(ARCHIVE.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, entries[n])
    tmp.replace(ARCHIVE)
    print(f"Wrote {ARCHIVE}: slot {SLOT} replaced "
          f"({len(new_blob)} bytes)")

    mirror = Path("/mnt/c/OGRS/Cache/video/Authentic_Sprites.orsc")
    if mirror.parent.exists():
        shutil.copy2(ARCHIVE, mirror)
        print(f"Mirrored to {mirror}")


if __name__ == "__main__":
    main()
