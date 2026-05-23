#!/usr/bin/env python3
"""
Retexture the existing OpenRSC goblin sprite (slot 837).

Approach: per-pixel color remap. Preserves the EXACT silhouette and pose,
just swaps the palette. The original uses 10 distinct colors — we remap
those 10 to new palettes that re-theme the creature.

Variants:
  A — cleaned + sharpened (same palette, edge cleanup)
  B — green skin (goblin-themed)
  C — brown bark (forest spirit)
  D — red devil (small imp)
"""
import os
from PIL import Image

SRC = "/home/sparky/ogrs/art/reference/goblin_extracted/sprite_0837.png"
OUT = "/home/sparky/ogrs/art/npcs/goblin_options"
os.makedirs(OUT, exist_ok=True)


# Original palette indexed by intent — each role mapped to multiple swap targets.
# Color roles in the original:
#   FUR_BASE    : C9C9C9 (light grey)   — main mane fur
#   FUR_SHAD    : 8C8C8C (mid grey)     — fur shading
#   OUTLINE     : 182131 (near-black)   — silhouette outline
#   OUTLINE_2   : 2A3255 (dark blue)    — secondary outline / deeper shade
#   FLESH_HI    : F7AD9C (pink)         — exposed flesh: ears, tail tip
#   FLESH_MID   : D5846B (pink-brown)   — flesh mid-shade
#   FLESH_SHAD  : 8C4A39 (dark brown)   — flesh deep shade / feet detail
#   TEETH       : C6F700 (yellow-green) — fangs / teeth
#   EYE         : CE2129 (red)          — eye whites/iris
#   EYE_HI      : E7737B (pink-red)     — eye highlight

ORIG = {
    'FUR_BASE':   (201, 201, 201),
    'FUR_SHAD':   (140, 140, 140),
    'OUTLINE':    ( 24,  33,  49),
    'OUTLINE_2':  ( 42,  50,  85),
    'FLESH_HI':   (247, 173, 156),
    'FLESH_MID':  (213, 132, 107),
    'FLESH_SHAD': (140,  74,  57),
    'TEETH':      (198, 247,   0),
    'EYE':        (206,  33,  41),
    'EYE_HI':     (231, 115, 123),
}


# Helper: build a color-remap from a target dict (role → new RGB)
def remap(img, target_palette):
    """Returns a new image with colors swapped per target_palette."""
    src_to_dst = {}
    for role, rgb in ORIG.items():
        new = target_palette.get(role, rgb)
        src_to_dst[rgb + (255,)] = new + (255,)
    out = img.copy()
    w, h = out.size
    px = out.load()
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] == 0:
                continue
            px[x, y] = src_to_dst.get(p, p)
    return out


# ---- Variants ----

# A — cleaned + sharpened (same palette, minor edge fixes)
def variant_clean(orig):
    """For now just a copy; real cleanup pass would remove stray dark-outline
    pixels inside the silhouette body. (Done procedurally below.)"""
    img = orig.copy()
    px = img.load()
    w, h = img.size
    OUTLINE_RGBA = ORIG['OUTLINE'] + (255,)
    FUR = ORIG['FUR_BASE'] + (255,)
    FUR_S = ORIG['FUR_SHAD'] + (255,)

    # Walk through; any OUTLINE pixel whose 4 neighbors are all FUR_BASE or FUR_SHAD
    # is a stray "noise" outline pixel inside the body. Soften it to FUR_SHAD.
    cleaned = img.copy()
    cpx = cleaned.load()
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if px[x, y] != OUTLINE_RGBA:
                continue
            neighbors = [px[x - 1, y], px[x + 1, y], px[x, y - 1], px[x, y + 1]]
            non_outline = sum(1 for n in neighbors if n[3] > 0 and n != OUTLINE_RGBA)
            if non_outline == 4:
                cpx[x, y] = FUR_S   # interior stray → soften
    return cleaned


# B — green-skin goblin retexture (grey fur becomes green skin)
PAL_GREEN = {
    'FUR_BASE':   ( 90, 140,  60),   # goblin green
    'FUR_SHAD':   ( 50,  86,  44),   # deeper green
    'OUTLINE':    ( 18,  26,  14),
    'OUTLINE_2':  ( 34,  46,  24),
    'FLESH_HI':   (160, 200,  90),   # belly highlight
    'FLESH_MID':  (130, 170,  80),
    'FLESH_SHAD': ( 70, 100,  40),
    'TEETH':      (240, 220, 120),
    'EYE':        ( 30,  20,  14),   # dim black eyes (classic RSC)
    'EYE_HI':     ( 60,  50,  40),
}

# C — bark / forest spirit retexture
PAL_BARK = {
    'FUR_BASE':   (138, 105,  68),   # bark brown
    'FUR_SHAD':   ( 92,  68,  40),   # deeper bark
    'OUTLINE':    ( 30,  20,  12),
    'OUTLINE_2':  ( 50,  36,  20),
    'FLESH_HI':   (212, 168,  90),   # warm wood
    'FLESH_MID':  (164, 124,  60),
    'FLESH_SHAD': ( 90,  60,  28),
    'TEETH':      (240, 230, 180),   # ivory
    'EYE':        (220, 200,  80),   # amber eyes
    'EYE_HI':     (250, 230, 140),
}

# D — red devilkin retexture
PAL_DEVIL = {
    'FUR_BASE':   (180,  60,  50),   # red flesh
    'FUR_SHAD':   (120,  30,  30),
    'OUTLINE':    ( 30,  10,  10),
    'OUTLINE_2':  ( 60,  20,  20),
    'FLESH_HI':   (255, 150, 120),   # exposed skin lighter
    'FLESH_MID':  (220, 110,  90),
    'FLESH_SHAD': (140,  50,  40),
    'TEETH':      (255, 240, 200),   # ivory fangs
    'EYE':        (255, 220,  60),   # glowing yellow
    'EYE_HI':     (255, 255, 200),
}


def main():
    orig = Image.open(SRC).convert("RGBA")

    a = variant_clean(orig)
    a.save(f"{OUT}/retex_A_cleaned.png")
    a.resize((a.size[0] * 8, a.size[1] * 8), Image.NEAREST).save(f"{OUT}/retex_A_cleaned_x8.png")

    b = remap(orig, PAL_GREEN)
    b = variant_clean(b)   # same cleanup pass on the recolored version
    b.save(f"{OUT}/retex_B_green.png")
    b.resize((b.size[0] * 8, b.size[1] * 8), Image.NEAREST).save(f"{OUT}/retex_B_green_x8.png")

    c = remap(orig, PAL_BARK)
    c.save(f"{OUT}/retex_C_bark.png")
    c.resize((c.size[0] * 8, c.size[1] * 8), Image.NEAREST).save(f"{OUT}/retex_C_bark_x8.png")

    d = remap(orig, PAL_DEVIL)
    d.save(f"{OUT}/retex_D_devil.png")
    d.resize((d.size[0] * 8, d.size[1] * 8), Image.NEAREST).save(f"{OUT}/retex_D_devil_x8.png")

    print("done — wrote 4 retextures")


if __name__ == "__main__":
    main()
