#!/usr/bin/env python3
"""
Procedural SPIKEBALL projectile — Earth spells + Snare/Bind + adamant arrows.
Asymmetric tumbling boulder with mossy patches. 4 frames rotate the boulder
(via flip/rotate) so it reads as actively spinning through the air.
"""
import os
from PIL import Image

W = H = 30
TRANS = (0, 0, 0, 0)

OUTLINE   = ( 26,  20,  12, 255)  # 1A140C
DEEP      = ( 58,  40,  24, 255)  # 3A2818
BASE      = (107,  69,  32, 255)  # 6B4520
HIGH      = (160, 112,  80, 255)  # A07050
PEAK_LIT  = (212, 152, 112, 255)  # D49870
MOSS_HI   = (104, 128,  48, 255)  # 688030
MOSS_SH   = ( 58,  74,  24, 255)  # 3A4A18
DUST_HI   = (139, 106,  69, 255)  # 8B6A45
DUST_LO   = ( 74,  53,  32, 255)  # 4A3520


def in_bounds(x, y):
    return 0 <= x < W and 0 <= y < H


def put(px, x, y, c):
    if c is not None and in_bounds(x, y):
        px[x, y] = c


# Canonical boulder shape drawn into a 14×14 sub-grid, centered roughly at (7, 7).
# Each character maps to a color:
#   '.' = transparent  'O' = outline  'D' = deep  'B' = base
#   'H' = highlight    'P' = peak_lit  'm' = moss_shade  'M' = moss_highlight
BOULDER_TEMPLATE = [
    "...OOOO....OO.",
    "..OBBBHO..OPPO",
    ".OBBBHHHOOPHHO",
    "OBmmBHHHHHHHHO",
    "OBmMmBBBHHPHHO",
    "OBmMBBBBBBHHHO",
    "OBmBBBBBBBBHHO",
    "OBBBBBDDBBBBHO",
    "OBBBBBDDBBBmHO",
    "OBBBBBDDBBmMmO",
    "OBBBBBBBDBmMmO",
    ".OBBBDBBBBBmO.",
    "..OBBBBDDBBO..",
    "...OOOOOOOO...",
]

COLOR_MAP = {
    'O': OUTLINE,
    'D': DEEP,
    'B': BASE,
    'H': HIGH,
    'P': PEAK_LIT,
    'm': MOSS_SH,
    'M': MOSS_HI,
    '.': None,
}


def render_template(template, transpose=False, flip_h=False, flip_v=False):
    """Returns a list of (dx, dy, color) for the boulder, with optional flip/transpose."""
    h = len(template)
    w = len(template[0])
    cells = []
    for ty in range(h):
        for tx in range(w):
            ch = template[ty][tx]
            color = COLOR_MAP.get(ch)
            if color is None:
                continue
            x, y = tx, ty
            if transpose:
                x, y = y, x
            if flip_h:
                x = (w - 1) - x if not transpose else (h - 1) - x
            if flip_v:
                y = (h - 1) - y if not transpose else (w - 1) - y
            cells.append((x, y, color))
    return cells


def draw_boulder(px, cells, offset_x, offset_y, lit_extra=False):
    for dx, dy, c in cells:
        put(px, offset_x + dx, offset_y + dy, c)
    if lit_extra:
        # Brighten the top-most pixels (sun-lit edge effect)
        # Find topmost non-transparent cells per column
        from collections import defaultdict
        cols = defaultdict(list)
        for dx, dy, _ in cells:
            cols[dx].append(dy)
        for dx, ys in cols.items():
            top = min(ys)
            put(px, offset_x + dx, offset_y + top, PEAK_LIT)


def draw_dust(px, frame):
    """Small dust trail particles behind the boulder."""
    # Place a few specks in the lower-left area (assuming boulder moves to upper-right)
    if frame == 2:
        # peak — punchy dust kick
        specs = [(8, 23, DUST_HI), (7, 24, DUST_HI), (9, 22, DUST_HI),
                 (6, 25, DUST_LO), (10, 24, DUST_LO), (5, 26, DUST_LO)]
    elif frame == 3:
        specs = [(7, 24, DUST_HI), (5, 25, DUST_LO), (8, 23, DUST_LO),
                 (3, 27, DUST_LO), (10, 24, DUST_LO)]
    elif frame == 1:
        specs = [(8, 23, DUST_LO), (6, 25, DUST_LO)]
    else:
        specs = [(7, 24, DUST_LO)]
    for x, y, c in specs:
        put(px, x, y, c)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # 4 rotations via flip combos
    flips = [
        dict(transpose=False, flip_h=False, flip_v=False),
        dict(transpose=True,  flip_h=False, flip_v=True),
        dict(transpose=False, flip_h=True,  flip_v=True),
        dict(transpose=True,  flip_h=True,  flip_v=False),
    ]
    cells = render_template(BOULDER_TEMPLATE, **flips[frame])
    # Boulder occupies ~14×14; center near (14, 14) → offset (7, 7)
    draw_boulder(px, cells, offset_x=7, offset_y=7, lit_extra=(frame == 2))
    draw_dust(px, frame)
    return img


base = "/home/sparky/ogrs/art/projectiles/5_spikeball/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print(f"frame_{i:02d}")
print("done")
