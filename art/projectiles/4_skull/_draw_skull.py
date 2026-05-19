#!/usr/bin/env python3
"""
Procedural SKULL projectile — curse spells + Flames of Zamorak + poison arrows.
Bottom-anchored skull silhouette + 3 cursed-flame wisps rising above.
Frames flicker the flames (heights + colors cycle).
"""
import os
from PIL import Image

W = H = 30
TRANS = (0, 0, 0, 0)

BONE_OUTLINE = ( 26,  16,  32, 255)  # 1A1020
BONE_SHADE   = ( 90,  72,  96, 255)  # 5A4860
BONE_BASE    = (144, 128, 160, 255)  # 9080A0
BONE_HI      = (200, 192, 208, 255)  # C8C0D0
CAVITY       = ( 10,   4,  16, 255)  # 0A0410

FL_DEEP      = ( 80,  16,  32, 255)
FL_OUTER     = (192,  48,  31, 255)
FL_MID       = (255, 128,  48, 255)
FL_CORE      = (255, 224, 160, 255)
EMBER        = (255, 255, 255, 255)


def in_bounds(x, y):
    return 0 <= x < W and 0 <= y < H


def put(px, x, y, c):
    if c is not None and in_bounds(x, y):
        px[x, y] = c


# Skull pixel map, anchored so the chin sits at (CX, 26).
# Each tuple is (x, y, color).
# Layout (cx = 14):
#   rows 16-18 = cranium
#   row 19      = brow ridge / eye sockets top
#   row 20      = eyes
#   row 21      = nose row / cheekbones
#   row 22      = upper jaw / teeth row
#   row 23-24   = lower jaw / chin
SKULL_CELLS = []
def _add(x, y, c):
    SKULL_CELLS.append((x, y, c))

# Cranium top (row 16-17): rounded dome
for x in range(11, 18):
    _add(x, 16, BONE_OUTLINE)
for (x, c) in [(10, BONE_OUTLINE), (11, BONE_BASE), (12, BONE_HI), (13, BONE_HI),
               (14, BONE_HI), (15, BONE_HI), (16, BONE_BASE), (17, BONE_BASE), (18, BONE_OUTLINE)]:
    _add(x, 17, c)
# Cranium full width row 18
for (x, c) in [(9, BONE_OUTLINE), (10, BONE_BASE), (11, BONE_HI), (12, BONE_BASE),
               (13, BONE_BASE), (14, BONE_BASE), (15, BONE_BASE), (16, BONE_BASE),
               (17, BONE_HI), (18, BONE_BASE), (19, BONE_OUTLINE)]:
    _add(x, 18, c)
# Eye sockets row 19 (sockets begin)
for (x, c) in [(9, BONE_OUTLINE), (10, BONE_SHADE), (11, CAVITY), (12, CAVITY),
               (13, BONE_BASE), (14, BONE_BASE), (15, CAVITY), (16, CAVITY),
               (17, BONE_SHADE), (18, BONE_SHADE), (19, BONE_OUTLINE)]:
    _add(x, 19, c)
# Eye sockets row 20 (full black holes)
for (x, c) in [(9, BONE_OUTLINE), (10, BONE_SHADE), (11, CAVITY), (12, CAVITY),
               (13, BONE_BASE), (14, BONE_BASE), (15, CAVITY), (16, CAVITY),
               (17, BONE_SHADE), (18, BONE_SHADE), (19, BONE_OUTLINE)]:
    _add(x, 20, c)
# Cheekbones + nose hole row 21
for (x, c) in [(10, BONE_OUTLINE), (11, BONE_SHADE), (12, BONE_BASE),
               (13, CAVITY), (14, CAVITY), (15, BONE_BASE), (16, BONE_BASE),
               (17, BONE_SHADE), (18, BONE_OUTLINE)]:
    _add(x, 21, c)
# Upper jaw row 22 — teeth gaps
for (x, c) in [(10, BONE_OUTLINE), (11, BONE_BASE), (12, CAVITY), (13, BONE_BASE),
               (14, CAVITY), (15, BONE_BASE), (16, CAVITY), (17, BONE_BASE),
               (18, BONE_OUTLINE)]:
    _add(x, 22, c)
# Lower jaw row 23
for (x, c) in [(11, BONE_OUTLINE), (12, BONE_BASE), (13, BONE_BASE),
               (14, BONE_SHADE), (15, BONE_BASE), (16, BONE_BASE), (17, BONE_OUTLINE)]:
    _add(x, 23, c)
# Chin row 24
for (x, c) in [(12, BONE_OUTLINE), (13, BONE_SHADE), (14, BONE_SHADE),
               (15, BONE_SHADE), (16, BONE_OUTLINE)]:
    _add(x, 24, c)


def draw_skull(px):
    for x, y, c in SKULL_CELLS:
        put(px, x, y, c)


def draw_flame(px, base_x, top_y, height_levels):
    """
    Flame wisp rising from (base_x, base_y=15) upward, with a per-frame height profile.
    height_levels is list of (relative_y_from_base, color) — drawn upward.
    """
    base_y = 15  # just above the cranium
    for dy, color in height_levels:
        put(px, base_x, base_y - dy, color)


def flame_profile(frame, side):
    """
    Return list of (dy, color) for a flame wisp. side -1/0/+1 = left/center/right wisp.
    Frame 0..3 controls flicker.
    """
    # Centered wisp is tallest; sides are shorter.
    if side == 0:
        if frame == 0:
            return [(0, FL_DEEP), (1, FL_OUTER), (2, FL_OUTER), (3, FL_MID), (4, FL_CORE)]
        if frame == 1:
            return [(0, FL_DEEP), (1, FL_OUTER), (2, FL_OUTER), (3, FL_MID), (4, FL_MID), (5, FL_CORE)]
        if frame == 2:
            return [(0, FL_DEEP), (1, FL_OUTER), (2, FL_MID), (3, FL_MID), (4, FL_CORE), (5, FL_CORE), (6, FL_CORE)]
        if frame == 3:
            return [(0, FL_DEEP), (1, FL_OUTER), (2, FL_MID), (3, FL_CORE)]
    else:
        if frame == 0:
            return [(0, FL_DEEP), (1, FL_OUTER), (2, FL_MID), (3, FL_CORE)]
        if frame == 1:
            return [(0, FL_DEEP), (1, FL_OUTER), (2, FL_OUTER), (3, FL_MID), (4, FL_CORE)]
        if frame == 2:
            return [(0, FL_DEEP), (1, FL_OUTER), (2, FL_OUTER), (3, FL_MID), (4, FL_MID), (5, FL_CORE)]
        if frame == 3:
            return [(0, FL_DEEP), (1, FL_MID), (2, FL_CORE)]


def draw_embers(px, frame):
    """Stray ember sparks above the flames on certain frames."""
    if frame == 3:
        for x, y in [(11, 4), (17, 5), (13, 2), (16, 3)]:
            put(px, x, y, EMBER)
        for x, y in [(10, 5), (18, 6), (14, 3)]:
            put(px, x, y, FL_OUTER)
    if frame == 2:
        # peak — additional ember at top of center wisp
        put(px, 14, 8, EMBER)
        put(px, 13, 9, FL_CORE)
        put(px, 15, 9, FL_CORE)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Flames first (so skull overlaps cleanly)
    for side, base_x in [(-1, 11), (0, 14), (1, 17)]:
        draw_flame(px, base_x, 0, flame_profile(frame, side))
    draw_skull(px)
    draw_embers(px, frame)
    return img


base = "/home/sparky/ogrs/art/projectiles/4_skull/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print(f"frame_{i:02d}")
print("done")
