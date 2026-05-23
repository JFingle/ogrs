#!/usr/bin/env python3
"""
Armor v4 — hand-pixeled masterwork using the template's exact palette.

Approach: study the existing platebody template, find its natural ornament
slot (the small yellow shield emblem at upper-right), and EXTEND it the way
the original artist would. No floating 1-pixel lines on shaded surfaces.

Trying 3 variants of the rune platebody MW so we can pick the right level
of restraint:
  A — Mirror the existing yellow emblem on the opposite shoulder (heraldic pair)
  B — Mirror + small chest jewel (gem inset using template palette)
  C — Mirror + chest jewel + faint scrollwork connecting the two emblems
"""
import struct, zipfile, os
from PIL import Image

ARCHIVE = "/home/sparky/ogrs/client/Cache/video/Authentic_Sprites.orsc"
OUT = "/home/sparky/ogrs/art/items/armor_v4"
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
    template = decode_sprite(z.read("2158"))  # platebody


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


def put(px, w, h, x, y, c):
    if 0 <= x < w and 0 <= y < h:
        px[x, y] = c


# Existing template palette colors
YELLOW_HI  = (252, 192,   0, 255)   # FCC000 — bright emblem
YELLOW_MID = (231, 214,  49, 255)   # E7D631 — mid emblem (also slightly green-shifted)
OUTLINE    = (  1,   1,   1, 255)

# Existing emblem map (right shoulder) — exact pixel positions
ORIGINAL_EMBLEM_RIGHT = [
    (30, 7, YELLOW_HI),  (31, 7, YELLOW_HI),  (32, 7, YELLOW_HI),  (33, 7, YELLOW_HI),
    (30, 8, YELLOW_HI),  (34, 8, YELLOW_HI),
    (31, 9, YELLOW_HI),  (33, 9, YELLOW_HI),  (34, 9, YELLOW_HI),
    (31, 10, YELLOW_MID), (34, 10, YELLOW_MID),
    (31, 11, YELLOW_MID), (32, 11, YELLOW_MID), (33, 11, YELLOW_MID), (34, 11, YELLOW_MID),
]


def add_mirrored_emblem(px, w, h):
    """Place a mirror of the existing right-shoulder emblem on the LEFT shoulder.
    The original is at x=30-34. The chest center is around x=17. Mirror axis = 17.
    So x_left = 17*2 - x_right = 34-x for x in [30, 34] → [4, 0]. We use x=4-8."""
    # Mirrored emblem pixel positions
    MIRROR = [
        # Same y values, x mirrored. Original right emblem maps to x=4-8 on left.
        (5, 7, YELLOW_HI),  (6, 7, YELLOW_HI),  (7, 7, YELLOW_HI),  (8, 7, YELLOW_HI),
        (4, 8, YELLOW_HI),  (8, 8, YELLOW_HI),
        (4, 9, YELLOW_HI),  (5, 9, YELLOW_HI),  (7, 9, YELLOW_HI),
        (4, 10, YELLOW_MID),(7, 10, YELLOW_MID),
        (4, 11, YELLOW_MID),(5, 11, YELLOW_MID),(6, 11, YELLOW_MID),(7, 11, YELLOW_MID),
    ]
    for x, y, c in MIRROR:
        # Only paint if the underlying template pixel is opaque (we don't want to add pixels in empty space)
        if px[x, y][3] > 0:
            px[x, y] = c


def add_chest_jewel(px, w, h, gem_color):
    """Inset a small gem at chest center, using template shadow colors as the bezel."""
    # Center of chest is around (16, 15)
    cx, cy = 16, 15
    # The gem is a single pixel surrounded by darker bezel (using existing shadows)
    DARK = (49, 49, 49, 255)  # #313131 — existing shadow color from palette
    # Inset bezel (using a darker shade — fits because templates already have this color)
    bezel_cells = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for dx, dy in bezel_cells:
        x, y = cx + dx, cy + dy
        if 0 <= x < w and 0 <= y < h and px[x, y][3] > 0:
            px[x, y] = DARK
    # Gem pixel
    if 0 <= cx < w and 0 <= cy < h and px[cx, cy][3] > 0:
        px[cx, cy] = gem_color
    # Highlight pixel above gem
    if 0 <= cx-1 < w and 0 <= cy-1 < h and px[cx-1, cy-1][3] > 0:
        px[cx-1, cy-1] = YELLOW_HI


def add_scrollwork(px, w, h):
    """Subtle yellow dots in the chest center area connecting the two shoulder emblems.
    Uses YELLOW_MID dots only, sparingly, to suggest filigree without lines."""
    # 5 small yellow dots in a faint pattern
    dots = [(12, 9, YELLOW_MID), (16, 9, YELLOW_HI), (20, 9, YELLOW_MID),
            (14, 13, YELLOW_MID), (18, 13, YELLOW_MID)]
    for x, y, c in dots:
        if 0 <= x < w and 0 <= y < h and px[x, y][3] > 0:
            px[x, y] = c


# Correct workflow:
#   1. Add mirror emblem to UNTINTED template (so it gets tinted alongside the original)
#   2. Apply pictureMask tint
#   3. Add gem/accent AFTER tinting (accent colors aren't metal so they don't tint)

w, h = template.size
RUNE_MASK = 0x00FFFF

# Vanilla
vanilla_tinted = apply_tint(template, RUNE_MASK)
vanilla_tinted.save(f"{OUT}/00_vanilla_rune.png")
vanilla_tinted.resize((w * 8, h * 8), Image.NEAREST).save(f"{OUT}/00_vanilla_rune_x8.png")

# Variant A: Mirror emblem only
template_with_mirror = template.copy()
add_mirrored_emblem(template_with_mirror.load(), w, h)
a = apply_tint(template_with_mirror, RUNE_MASK)
a.save(f"{OUT}/A_mirror_only.png")
a.resize((w * 8, h * 8), Image.NEAREST).save(f"{OUT}/A_mirror_only_x8.png")

# Variant B: Mirror + chest jewel (jewel added AFTER tint, kept as pure amethyst)
b = a.copy()
add_chest_jewel(b.load(), w, h, (220, 60, 220, 255))
b.save(f"{OUT}/B_mirror_jewel.png")
b.resize((w * 8, h * 8), Image.NEAREST).save(f"{OUT}/B_mirror_jewel_x8.png")

# Variant C: Mirror + jewel + faint scrollwork (scrollwork added BEFORE tint so it matches the green)
template_with_full = template.copy()
add_mirrored_emblem(template_with_full.load(), w, h)
add_scrollwork(template_with_full.load(), w, h)
c = apply_tint(template_with_full, RUNE_MASK)
add_chest_jewel(c.load(), w, h, (220, 60, 220, 255))
c.save(f"{OUT}/C_full.png")
c.resize((w * 8, h * 8), Image.NEAREST).save(f"{OUT}/C_full_x8.png")

print("Wrote 4 sprites with correct tint workflow")
