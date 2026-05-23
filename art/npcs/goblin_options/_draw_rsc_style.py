#!/usr/bin/env python3
"""
Goblin — proper RSC-aesthetic redraw.
Classic RSC pixel art is 3D-rendered look at ~32-40 px tall:
  - Big head proportionally
  - Hunched, forward-lean posture
  - 2-3 shading bands per body part (no anti-aliasing, no dither)
  - 1-px black outline around silhouette
  - Dim small eyes (NOT glowing red — looks too 'demonic')
  - Tattered cloth, usually red-brown or earth tones
  - Limited palette per part
"""
import os
from PIL import Image

W = H = 50
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def put_template(px, cells, ox, oy, color_map):
    th = len(cells)
    tw = max(len(r) for r in cells)
    for ty, row in enumerate(cells):
        for tx, ch in enumerate(row):
            if ch == '.':
                continue
            color = color_map.get(ch)
            put(px, ox + tx, oy + ty, color)


# RSC-leaning palette — slightly desaturated greens, warm browns
OUTLINE   = ( 22,  18,  10, 255)
DARK_SHAD = ( 38,  32,  20, 255)

SKIN_SHAD = ( 50,  86,  44, 255)
SKIN_BASE = ( 92, 138,  68, 255)
SKIN_HI   = (142, 188, 102, 255)

CLOTH_SHD = ( 86,  36,  24, 255)
CLOTH_B   = (146,  62,  36, 255)
CLOTH_HI  = (196, 110,  64, 255)

LOIN_SHD  = ( 60,  40,  20, 255)
LOIN_B    = (110,  78,  48, 255)
LOIN_HI   = (160, 124,  80, 255)

EYE       = ( 28,  20,  14, 255)
TOOTH     = (210, 190, 130, 255)
NAIL      = ( 60,  48,  30, 255)

WOOD_SHD  = ( 56,  38,  18, 255)
WOOD_B    = (104,  72,  38, 255)
WOOD_HI   = (158, 114,  64, 255)

IRON_SHD  = ( 60,  56,  64, 255)
IRON_B    = (118, 114, 130, 255)
IRON_HI   = (180, 180, 196, 255)


def draw_goblin(weapon='club', cloth_color='red'):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()

    # Cloth tone choice
    if cloth_color == 'red':
        c_shad, c_base, c_hi = CLOTH_SHD, CLOTH_B, CLOTH_HI
    else:
        c_shad, c_base, c_hi = LOIN_SHD, LOIN_B, LOIN_HI

    # ========= HEAD (proportionally big, slight forward lean) =========
    # Head occupies rows 6-21 (16 tall), centered around x=22
    HEAD = [
        "...OOOOOO...",
        "..OBBBBBBO..",
        ".OBHHHHHBBO.",
        "OBHHHHHHHBBO",
        "OBHHHHHHHHBO",
        "OBHHHHHHHHBO",
        "OBHHHHHHHBBO",
        "OBBHHHHHHBBO",
        ".OBBHHHHHBO.",
        "..OBBBBBBBO.",
        "...OBBBBBO..",
        "....OOOOO...",
    ]
    HEAD_COLORS = {'O': OUTLINE, 'B': SKIN_BASE, 'H': SKIN_HI, 'S': SKIN_SHAD}
    put_template(px, HEAD, 16, 6, HEAD_COLORS)

    # Pointed ears (sticking sideways from head, slightly slanted up)
    # Left ear (player's left, viewer's right? — actually mirror later. Just symmetric.)
    for dy in (0, 1, 2):
        put(px, 15 - dy, 11 + dy, OUTLINE)
        put(px, 16 - dy, 11 + dy, SKIN_BASE)
    put(px, 13, 13, OUTLINE)
    # Right ear
    for dy in (0, 1, 2):
        put(px, 28 + dy, 11 + dy, OUTLINE)
        put(px, 27 + dy, 11 + dy, SKIN_BASE)
    put(px, 30, 13, OUTLINE)

    # Eyes (small dim — 2 pixels each, dark, NOT red)
    put(px, 19, 13, EYE)
    put(px, 20, 13, EYE)
    put(px, 25, 13, EYE)
    put(px, 26, 13, EYE)
    # Eye shadow above for brow
    for x in (19, 20, 21, 22, 23, 24, 25, 26):
        put(px, x, 12, SKIN_SHAD)

    # Big nose — juts forward (right side from viewer), classic RSC big nose
    NOSE = [
        "OOO",
        "OBO",
        "OBO",
        "OOO",
    ]
    NC = {'O': OUTLINE, 'B': SKIN_HI}
    put_template(px, NOSE, 22, 14, NC)
    # Nose shadow underneath
    put(px, 22, 18, DARK_SHAD)
    put(px, 23, 18, DARK_SHAD)

    # Mouth area — small fang line
    for x in range(19, 27):
        put(px, x, 19, OUTLINE)
    # Fangs (lower)
    put(px, 21, 20, TOOTH)
    put(px, 24, 20, TOOTH)
    put(px, 20, 20, OUTLINE)
    put(px, 22, 20, OUTLINE)
    put(px, 23, 20, OUTLINE)
    put(px, 25, 20, OUTLINE)

    # Chin / jaw shadow
    for x in range(19, 27):
        put(px, x, 21, SKIN_SHAD)
    put(px, 23, 22, OUTLINE)
    put(px, 21, 22, OUTLINE)
    put(px, 22, 22, SKIN_SHAD)
    put(px, 24, 22, OUTLINE)

    # ========= NECK + TORSO (hunched) =========
    # Neck (short, thick)
    put(px, 20, 22, SKIN_BASE)
    put(px, 21, 22, SKIN_BASE)
    put(px, 22, 22, SKIN_BASE)
    put(px, 23, 22, SKIN_BASE)
    # Torso — broader than head at shoulders, narrows at waist
    # Shoulders at row 23 (wider)
    TORSO = [
        "OOOOOOOOOO",  # shoulders
        "OBBHHHBBSO",
        "OBHHHHHBSO",
        "OBHHHHBBSO",
        "OBHHBBBSOO",
        "OBBBBBSSOO",
        ".OBBBSSO..",   # waist narrowing
        ".OBBSSO...",
    ]
    TC = {'O': OUTLINE, 'B': SKIN_BASE, 'H': SKIN_HI, 'S': SKIN_SHAD}
    put_template(px, TORSO, 16, 23, TC)

    # ========= LOINCLOTH (red tattered cloth around hips) =========
    # Cloth row 31-36
    CLOTH = [
        ".OOOOOOOO..",
        "OBHHHBBBBO.",
        "OBHHBBBBBO.",
        "OBHBBBBSBO.",
        "OBBBSSBSBO.",
        ".OOOOOOOO..",
    ]
    CC = {'O': OUTLINE, 'B': c_base, 'H': c_hi, 'S': c_shad}
    put_template(px, CLOTH, 16, 31, CC)
    # Ragged hem
    for x in (16, 19, 22, 25):
        put(px, x, 37, c_shad)
        put(px, x + 1, 37, OUTLINE)

    # ========= LEGS (short, bent) =========
    # Left leg (viewer's left)
    for y in range(37, 44):
        put(px, 18, y, OUTLINE)
        put(px, 19, y, SKIN_BASE)
        put(px, 20, y, SKIN_HI)
        put(px, 21, y, OUTLINE)
    # Knee shadow
    put(px, 19, 41, SKIN_SHAD)
    # Right leg
    for y in range(37, 44):
        put(px, 23, y, OUTLINE)
        put(px, 24, y, SKIN_HI)
        put(px, 25, y, SKIN_BASE)
        put(px, 26, y, OUTLINE)
    put(px, 24, 41, SKIN_SHAD)

    # FEET (chunky, dark — bare feet with toes)
    # Left foot
    for x in range(17, 23):
        put(px, x, 44, OUTLINE)
        put(px, x, 45, LOIN_SHD)
    for x in (18, 20):
        put(px, x, 46, NAIL)  # toe nails
    # Right foot
    for x in range(22, 28):
        put(px, x, 44, OUTLINE)
        put(px, x, 45, LOIN_SHD)
    for x in (23, 25):
        put(px, x, 46, NAIL)

    # ========= ARMS =========
    # Left arm (hangs down, slightly forward)
    for y in range(26, 33):
        put(px, 14, y, OUTLINE)
        put(px, 15, y, SKIN_BASE)
        put(px, 16, y, OUTLINE)
    # Left hand (small fist)
    put(px, 14, 33, OUTLINE)
    put(px, 15, 33, SKIN_SHAD)
    put(px, 16, 33, OUTLINE)
    put(px, 14, 34, OUTLINE)
    put(px, 15, 34, SKIN_BASE)
    put(px, 16, 34, OUTLINE)
    put(px, 14, 35, OUTLINE)
    put(px, 15, 35, OUTLINE)
    put(px, 16, 35, OUTLINE)

    # Right arm — extends out to side, holds weapon
    for y in range(26, 31):
        put(px, 30, y, OUTLINE)
        put(px, 31, y, SKIN_BASE)
        put(px, 32, y, OUTLINE)
    # Forearm goes out to the right
    for x in range(32, 36):
        put(px, x, 28, OUTLINE)
        put(px, x, 29, SKIN_HI)
        put(px, x, 30, OUTLINE)
    # Right hand
    put(px, 36, 28, OUTLINE)
    put(px, 36, 29, OUTLINE)
    put(px, 36, 30, OUTLINE)
    put(px, 35, 27, OUTLINE)
    put(px, 35, 31, OUTLINE)

    # ========= WEAPON =========
    if weapon == 'club':
        # Wooden club extending upward from right hand
        # Shaft
        for y in range(15, 28):
            put(px, 36, y, OUTLINE)
            put(px, 37, y, WOOD_B)
            put(px, 38, y, WOOD_HI)
            put(px, 39, y, OUTLINE)
        # Club head (bulbous top)
        CLUB = [
            ".OOOOOO.",
            "OBBHHBO.",
            "OBHHHBBO",
            "OBHHBBBO",
            "OBBBBBSO",
            "OBBBBSSO",
            ".OOOOOO.",
        ]
        CLUBC = {'O': OUTLINE, 'B': WOOD_B, 'H': WOOD_HI, 'S': WOOD_SHD}
        put_template(px, CLUB, 35, 8, CLUBC)
    elif weapon == 'shortsword':
        # Iron blade
        for y in range(10, 28):
            put(px, 37, y, OUTLINE)
            put(px, 38, y, IRON_B)
            put(px, 39, y, IRON_HI)
            put(px, 40, y, OUTLINE)
        # Tip
        put(px, 38, 9, OUTLINE)
        put(px, 39, 9, OUTLINE)
        # Crossguard
        for x in range(35, 43):
            put(px, x, 28, WOOD_SHD)
            put(px, x, 29, OUTLINE)
        # Grip
        put(px, 37, 30, WOOD_B)
        put(px, 38, 30, WOOD_HI)
        put(px, 39, 30, WOOD_B)
        put(px, 40, 30, OUTLINE)

    return img


if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/npcs/goblin_options"
    img = draw_goblin(weapon='club', cloth_color='red')
    img.save(f"{out}/option_b_v2_rsc.png")
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"{out}/option_b_v2_rsc_x6.png")

    img2 = draw_goblin(weapon='shortsword', cloth_color='brown')
    img2.save(f"{out}/option_b_v2_rsc_warrior.png")
    img2.resize((W * 6, H * 6), Image.NEAREST).save(f"{out}/option_b_v2_rsc_warrior_x6.png")

    print("done")
