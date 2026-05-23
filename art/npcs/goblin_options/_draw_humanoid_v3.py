#!/usr/bin/env python3
"""
Goblin humanoid v3 — careful hand-placement at exactly 30×50.

Matches existing OpenRSC goblin frame scale (idle was 59×53; this is roughly
half-width since it's bipedal vs 4-legged).

Classic-RSC proportions:
  rows  4-19  head (16 tall — large proportional head)
  rows 19-22  short neck
  rows 22-33  torso + arms
  rows 33-38  loincloth wrap
  rows 38-48  legs
  rows 48-49  feet

Palette: olive-green skin, deep red loincloth, brown wood club, ivory teeth.
"""
import os
from PIL import Image

W = 30
H = 50
TRANS = (0, 0, 0, 0)

# Palette — limited, slightly desaturated RSC-feel
OUTLINE   = ( 22,  20,  12, 255)
DARK_SHAD = ( 42,  42,  20, 255)
SKIN_DK   = ( 56,  78,  38, 255)
SKIN_B    = ( 96, 132,  62, 255)
SKIN_HI   = (148, 184, 102, 255)
SKIN_BRT  = (188, 218, 132, 255)
EYE       = ( 24,  18,  12, 255)
TOOTH     = (224, 208, 144, 255)
NAIL      = (134, 102,  60, 255)
CLOTH_DK  = ( 86,  28,  20, 255)
CLOTH_B   = (138,  54,  36, 255)
CLOTH_HI  = (192,  96,  64, 255)
WOOD_DK   = ( 72,  46,  20, 255)
WOOD_B    = (124,  84,  44, 255)
WOOD_HI   = (170, 124,  68, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def block(px, x, y, w, h, c):
    for dx in range(w):
        for dy in range(h):
            put(px, x + dx, y + dy, c)


# Center axis: x = 14 (canvas is 30 wide so center 14-15)
CX = 14


def draw_goblin():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()

    # ---- HEAD ---- rows 3-18, ~14 tall, slightly forward-leaning
    # Outline (large rounded square head)
    HEAD_ROWS = [
        # (y, x_left, x_right, fill_color)
        ( 3, 11, 16, OUTLINE),  # top arc
        ( 4, 10, 17, OUTLINE),
        ( 5,  9, 18, OUTLINE),
        ( 6,  9, 18, OUTLINE),
    ]
    # Top dome rows
    for y in (3,):
        for x in range(11, 17):
            put(px, x, y, OUTLINE)
    for y in (4,):
        put(px, 10, y, OUTLINE)
        for x in range(11, 17):
            put(px, x, y, SKIN_HI)
        put(px, 17, y, OUTLINE)
    for y in (5,):
        put(px, 9, y, OUTLINE)
        for x in range(10, 18):
            put(px, x, y, SKIN_HI)
        put(px, 18, y, OUTLINE)
    # Head main body
    for y in range(6, 17):
        put(px, 9, y, OUTLINE)
        put(px, 19, y, OUTLINE)
        for x in range(10, 19):
            put(px, x, y, SKIN_B)
    # Head bottom (chin)
    for y in (17,):
        put(px, 10, y, OUTLINE)
        for x in range(11, 18):
            put(px, x, y, SKIN_DK)
        put(px, 18, y, OUTLINE)
    for y in (18,):
        put(px, 11, y, OUTLINE)
        for x in range(12, 17):
            put(px, x, y, SKIN_DK)
        put(px, 17, y, OUTLINE)

    # Skin highlight on upper-left side (light source upper-left)
    for x, y in [(10, 6), (11, 6), (11, 7), (12, 7), (10, 7)]:
        put(px, x, y, SKIN_HI)
    put(px, 11, 8, SKIN_HI)

    # ---- EARS ---- pointed, sticking sideways from head (rows 8-11)
    # Left ear (viewer's left)
    put(px,  8,  9, OUTLINE)
    put(px,  7, 10, OUTLINE)
    put(px,  6, 11, OUTLINE)
    put(px,  8, 10, SKIN_B)
    put(px,  9, 10, SKIN_B)
    put(px,  8, 11, OUTLINE)
    # Right ear
    put(px, 20,  9, OUTLINE)
    put(px, 21, 10, OUTLINE)
    put(px, 22, 11, OUTLINE)
    put(px, 19, 10, SKIN_B)
    put(px, 20, 10, SKIN_B)
    put(px, 20, 11, OUTLINE)

    # ---- BIG NOSE ---- juts forward (down + right slightly in 3/4 view)
    # Nose body — small rounded knob protruding
    put_template_at(px, 13, 11, [
        ".OO.",
        "OBBO",
        "OBHO",
        "OBBO",
        ".OO.",
    ], {'O': OUTLINE, 'B': SKIN_DK, 'H': SKIN_B})

    # ---- EYES ---- small dim dots (classic RSC, not glowing red)
    # Left eye
    put(px, 11, 10, EYE)
    # Right eye
    put(px, 18, 10, EYE)
    # Brow shading just above eyes (slight squint)
    put(px, 10,  9, DARK_SHAD)
    put(px, 11,  9, DARK_SHAD)
    put(px, 17,  9, DARK_SHAD)
    put(px, 18,  9, DARK_SHAD)

    # ---- MOUTH + FANGS ---- below nose
    # Mouth line
    for x in range(11, 18):
        put(px, x, 15, OUTLINE)
    # Lower lip shade
    for x in range(12, 17):
        put(px, x, 16, DARK_SHAD)
    # 2 fangs visible
    put(px, 12, 16, TOOTH)
    put(px, 16, 16, TOOTH)

    # ---- NECK ---- short, thick
    block(px, 12, 19, 5, 2, SKIN_DK)
    put(px, 11, 19, OUTLINE)
    put(px, 17, 19, OUTLINE)
    put(px, 11, 20, OUTLINE)
    put(px, 17, 20, OUTLINE)

    # ---- TORSO ---- (rows 21-32, slightly hunched, wider at shoulders)
    # Shoulders row 21 (broadest)
    for x in range(9, 20):
        put(px, x, 21, OUTLINE)
    # Body sides
    for y in range(22, 33):
        put(px,  8, y, OUTLINE)
        put(px, 20, y, OUTLINE)
        for x in range(9, 20):
            put(px, x, y, SKIN_B)
    # Body shadow on right side (light from upper-left)
    for y in range(22, 33):
        for x in range(17, 20):
            put(px, x, y, SKIN_DK)
    # Belly highlight (left/center)
    for y in (24, 25, 26):
        for x in (10, 11, 12):
            put(px, x, y, SKIN_HI)

    # ---- ARMS ----
    # Left arm (viewer's left) — hangs down along body
    for y in range(22, 31):
        put(px, 6, y, OUTLINE)
        put(px, 7, y, SKIN_B)
        put(px, 8, y, SKIN_DK)  # arm inner side
    # Left hand at bottom
    for y in (31, 32):
        put(px, 6, y, OUTLINE)
        put(px, 7, y, SKIN_DK)
        put(px, 8, y, OUTLINE)
    put(px, 6, 33, OUTLINE)
    put(px, 7, 33, OUTLINE)
    put(px, 8, 33, OUTLINE)

    # Right arm — bent forward, holding a club at chest level
    # Shoulder to elbow (down and slightly forward)
    for y in range(22, 27):
        put(px, 20, y, OUTLINE)
        put(px, 21, y, SKIN_B)
        put(px, 22, y, OUTLINE)
    # Elbow turn — forearm goes inward toward club
    for x in range(20, 23):
        put(px, x, 27, OUTLINE)
    # Forearm rows 28-31
    for y in range(28, 31):
        for x in range(20, 24):
            put(px, x, y, SKIN_B)
        put(px, 19, y, OUTLINE)
        put(px, 24, y, OUTLINE)
    # Hand grasps the club around the wrist
    put(px, 22, 31, SKIN_B)
    put(px, 23, 31, SKIN_DK)

    # ---- CLUB ---- diagonal, going up-right from right hand (rests against shoulder)
    # Shaft from hand at (22, 30) up to (28, 19) -ish
    shaft = [
        (22, 30), (23, 29), (24, 28), (25, 27), (26, 26),
        (27, 25), (28, 24), (28, 23), (28, 22), (28, 21),
    ]
    for x, y in shaft:
        put(px, x, y, WOOD_B)
        put(px, x + 1, y - 1, WOOD_HI)
        put(px, x - 1, y + 1, OUTLINE)
    # Club head (knobby top)
    put_template_at(px, 26, 17, [
        "OOOO",
        "OHHO",
        "OBHO",
        "OBSO",
        "OOOO",
    ], {'O': OUTLINE, 'B': WOOD_B, 'H': WOOD_HI, 'S': WOOD_DK})

    # ---- LOINCLOTH ---- red tattered wrap rows 32-37
    # Cloth body
    for y in range(33, 38):
        put(px,  7, y, OUTLINE)
        put(px, 21, y, OUTLINE)
        for x in range(8, 21):
            put(px, x, y, CLOTH_B)
    # Top cinch
    for x in range(8, 21):
        put(px, x, 33, OUTLINE)
    # Highlight on left/center
    for x in (9, 10, 11, 12, 13):
        put(px, x, 34, CLOTH_HI)
    # Shadow on right
    for x in (17, 18, 19, 20):
        for y in (34, 35, 36):
            put(px, x, y, CLOTH_DK)
    # Ragged hem
    for x in (8, 10, 12, 14, 16, 18, 20):
        put(px, x, 38, OUTLINE)
    for x in (9, 11, 13, 15, 17, 19):
        put(px, x, 37, CLOTH_DK)

    # ---- LEGS ---- (rows 39-47, short bent legs)
    # Left leg
    for y in range(38, 47):
        put(px, 10, y, OUTLINE)
        put(px, 11, y, SKIN_B)
        put(px, 12, y, SKIN_HI)
        put(px, 13, y, OUTLINE)
    # Right leg
    for y in range(38, 47):
        put(px, 16, y, OUTLINE)
        put(px, 17, y, SKIN_HI)
        put(px, 18, y, SKIN_DK)
        put(px, 19, y, OUTLINE)

    # ---- FEET ---- bare with toe-claws
    for x in range(9, 15):
        put(px, x, 47, OUTLINE)
        put(px, x, 48, DARK_SHAD)
    for x in range(15, 21):
        put(px, x, 47, OUTLINE)
        put(px, x, 48, DARK_SHAD)
    # Toe-claws (small nails)
    for x in (10, 12):
        put(px, x, 49, NAIL)
    for x in (16, 18):
        put(px, x, 49, NAIL)

    return img


def put_template_at(px, x, y, rows, color_map):
    for ty, row in enumerate(rows):
        for tx, ch in enumerate(row):
            if ch == '.':
                continue
            put(px, x + tx, y + ty, color_map.get(ch))


if __name__ == "__main__":
    img = draw_goblin()
    out = "/home/sparky/ogrs/art/npcs/goblin_options"
    img.save(f"{out}/humanoid_v3.png")
    img.resize((W * 10, H * 10), Image.NEAREST).save(f"{out}/humanoid_v3_x10.png")
    print("done")
