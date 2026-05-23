#!/usr/bin/env python3
"""
Armor v5 — Variant A scaled across all 7 platebody tiers.

Workflow per tier:
  1. Start with the untinted platebody template
  2. Add the mirrored yellow emblem to the LEFT shoulder (using template's exact yellow palette)
  3. Apply that tier's pictureMask — both emblems get the same tint

Result: 7 vanilla + 7 MW = 14 sprites at the template's native 39×29 size.
The MW variant is visually distinct via the doubled heraldic emblem;
the tier identity comes from the same color tint as vanilla.
"""
import struct, zipfile, os
from PIL import Image

ARCHIVE = "/home/sparky/ogrs/client/Cache/video/Authentic_Sprites.orsc"
OUT = "/home/sparky/ogrs/art/items/armor_v5"
os.makedirs(OUT, exist_ok=True)


def decode_sprite(data):
    if len(data) < 25: return None
    w, h = struct.unpack(">II", data[0:8])
    if w * h * 4 + 25 > len(data) + 100: return None
    expected = 25 + w * h * 4
    if len(data) < expected: return None
    pixels = struct.unpack(f">{w*h}I", data[25:expected])
    img = Image.new("RGBA", (w, h))
    for i, p in enumerate(pixels):
        if p == 0:
            img.putpixel((i % w, i // w), (0, 0, 0, 0))
        else:
            r = (p >> 16) & 0xFF; g = (p >> 8) & 0xFF; b = p & 0xFF
            img.putpixel((i % w, i // w), (r, g, b, 255))
    return img


with zipfile.ZipFile(ARCHIVE) as z:
    template = decode_sprite(z.read("2158"))


def apply_tint(img, mask_int):
    mr = (mask_int >> 16) & 0xFF; mg = (mask_int >> 8) & 0xFF; mb = mask_int & 0xFF
    out = img.copy()
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] == 0: continue
            px[x, y] = ((p[0] * mr) // 255, (p[1] * mg) // 255, (p[2] * mb) // 255, p[3])
    return out


# Existing emblem palette
YELLOW_HI  = (252, 192,   0, 255)
YELLOW_MID = (231, 214,  49, 255)

# Mirrored emblem (left shoulder) — same shape as right but x-mirrored around chest axis
MIRROR_PIXELS = [
    (5, 7, YELLOW_HI),  (6, 7, YELLOW_HI),  (7, 7, YELLOW_HI),  (8, 7, YELLOW_HI),
    (4, 8, YELLOW_HI),  (8, 8, YELLOW_HI),
    (4, 9, YELLOW_HI),  (5, 9, YELLOW_HI),  (7, 9, YELLOW_HI),
    (4, 10, YELLOW_MID), (7, 10, YELLOW_MID),
    (4, 11, YELLOW_MID), (5, 11, YELLOW_MID), (6, 11, YELLOW_MID), (7, 11, YELLOW_MID),
]


def add_mirrored_emblem(img):
    """Add the mirror emblem to a (untinted) template. Only paints on opaque template pixels."""
    px = img.load()
    w, h = img.size
    for x, y, c in MIRROR_PIXELS:
        if 0 <= x < w and 0 <= y < h and px[x, y][3] > 0:
            px[x, y] = c
    return img


# Real pictureMask values from EntityHandler.java
TIERS = [
    ('bronze',  0xFF7F19),
    ('iron',    0xEEDDDD),
    ('steel',   0xEEEEEE),
    ('black',   0x303030),
    ('mithril', 0x99AACC),
    ('adamant', 0xB2D499),
    ('rune',    0x00FFFF),
]


if __name__ == "__main__":
    # Build mirrored template ONCE, reuse for all tier tints
    mirrored_template = template.copy()
    add_mirrored_emblem(mirrored_template)

    w, h = template.size
    for tier_name, mask in TIERS:
        # Vanilla — just the tinted template
        vanilla = apply_tint(template, mask)
        vanilla.save(f"{OUT}/plate_{tier_name}.png")
        vanilla.resize((w * 8, h * 8), Image.NEAREST).save(f"{OUT}/plate_{tier_name}_x8.png")

        # Masterwork — mirrored template, then tinted
        mw = apply_tint(mirrored_template, mask)
        mw.save(f"{OUT}/plate_{tier_name}_mw.png")
        mw.resize((w * 8, h * 8), Image.NEAREST).save(f"{OUT}/plate_{tier_name}_mw_x8.png")
        print(f"done: plate_{tier_name} + _mw")

    print(f"\n=== Armor v5 platebody set complete: 14 sprites ===")
