#!/usr/bin/env python3
"""
Procedural RANGED projectile — actual arrow silhouette.
Iron arrowhead (triangle) + wood shaft + V-fletching at tail.
Glint cycle frame-by-frame so it reads as in-flight.
"""
import os
from PIL import Image

W = H = 30
TRANSPARENT = (0, 0, 0, 0)

WOOD_HI     = (168, 114,  58, 255)
WOOD_BASE   = (139,  90,  43, 255)
WOOD_SHADE  = ( 92,  58,  26, 255)

TIP_HI      = (220, 220, 230, 255)
TIP_BASE    = (160, 165, 180, 255)
TIP_SHADE   = ( 78,  82,  98, 255)
TIP_OUTLINE = ( 40,  44,  56, 255)

FLETCH_HI   = (240, 240, 240, 255)
FLETCH_BASE = (190, 190, 200, 255)
FLETCH_SH   = (110, 115, 130, 255)
FLETCH_RED  = (180,  55,  55, 255)  # tier accent — red fletching for the basic arrow look
FLETCH_RED2 = (120,  40,  40, 255)

GLINT       = (255, 255, 255, 255)
TRAIL       = (200, 200, 210, 255)


def in_bounds(x, y):
    return 0 <= x < W and 0 <= y < H


def put(px, x, y, c):
    if c is not None and in_bounds(x, y):
        px[x, y] = c


# Diagonal arrow, tail lower-left to tip upper-right.
TAIL_X, TAIL_Y = 5, 24
TIP_X,  TIP_Y  = 24, 5


def bresenham(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    x, y = x0, y0
    while True:
        pts.append((x, y))
        if x == x1 and y == y1: break
        e2 = 2 * err
        if e2 > -dy: err -= dy; x += sx
        if e2 <  dx: err += dx; y += sy
    return pts


def draw_shaft(px):
    """Draws shaft from after the fletching to before the tip. Returns full line for glint indexing."""
    line = bresenham(TAIL_X, TAIL_Y, TIP_X, TIP_Y)
    # Body indices: skip a few cells at each end (tip + fletching draw there separately)
    body = line[4:-4]
    for (x, y) in body:
        put(px, x, y, WOOD_BASE)
        # 1-px highlight on upper-right side of shaft
        put(px, x + 1, y - 1, WOOD_HI)
        # 1-px shadow on lower-left side of shaft
        put(px, x - 1, y + 1, WOOD_SHADE)
    return line


def draw_tip(px, flash=False):
    """Triangular iron arrowhead at upper-right."""
    # Outline of the head (a 3-row triangle, tip at TIP_X+1, TIP_Y-1)
    tip_cells = {
        # row offsets from TIP, building a chunky triangle
        ( 0,  0): TIP_BASE,
        (-1,  0): TIP_BASE,
        ( 0, -1): TIP_HI,
        ( 1, -1): TIP_HI,
        (-1,  1): TIP_BASE,
        (-2,  1): TIP_SHADE,
        (-2,  2): TIP_OUTLINE,
        (-1, -1): TIP_HI,
        ( 1,  0): TIP_HI,    # extends right
        ( 2, -1): TIP_HI,    # very tip
    }
    for (ox, oy), c in tip_cells.items():
        put(px, TIP_X + ox, TIP_Y + oy, c)
    # Outline (dark) around the head for readability against light bg
    outline = [(-3, 2), (-2, 3), (-1, 2), (0, 1), (-3, 1), (1, 1), (2, 0), (3, -1)]
    for ox, oy in outline:
        put(px, TIP_X + ox, TIP_Y + oy, TIP_OUTLINE)
    if flash:
        put(px, TIP_X + 2, TIP_Y - 1, GLINT)
        put(px, TIP_X + 1, TIP_Y - 1, GLINT)
        put(px, TIP_X + 1, TIP_Y - 2, GLINT)


def draw_fletching(px):
    """V-shaped fletching at the tail. Red-feather tier-1 look."""
    # Three "feathers" extending back from tail along the up and side directions
    cells = {
        # spine
        ( 0,  0): WOOD_SHADE,
        ( 1, -1): WOOD_SHADE,
        # red feather body (two angled lobes)
        ( 0,  1): FLETCH_RED,
        (-1,  1): FLETCH_RED,
        (-1,  0): FLETCH_RED,
        (-2,  0): FLETCH_RED,
        (-2, -1): FLETCH_RED2,
        (-1, -1): FLETCH_RED2,
        ( 0, -1): FLETCH_RED2,
        # right-lower lobe
        ( 1,  1): FLETCH_RED,
        ( 1,  2): FLETCH_RED2,
        ( 0,  2): FLETCH_RED2,
        (-1,  2): FLETCH_RED2,
        # spine highlights
        ( 0,  0): WOOD_BASE,
    }
    for (ox, oy), c in cells.items():
        put(px, TAIL_X + ox, TAIL_Y + oy, c)


def draw_glint(px, line, t):
    idx = int(t * (len(line) - 1))
    x, y = line[idx]
    put(px, x, y, GLINT)
    put(px, x + 1, y - 1, FLETCH_HI)


def draw_trail(px):
    """Speed lines behind the fletching, going lower-left."""
    for i, (ox, oy, c) in enumerate([
        (-3,  2, TRAIL),
        (-4,  3, TRAIL),
        (-5,  4, FLETCH_SH),
        (-2,  4, TRAIL),
        (-3,  5, FLETCH_SH),
    ]):
        put(px, TAIL_X + ox, TAIL_Y + oy, c)


def draw_frame(glint_t=None, tip_flash=False, trail=False):
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    px = img.load()
    line = draw_shaft(px)
    draw_fletching(px)
    draw_tip(px, flash=tip_flash)
    if glint_t is not None:
        draw_glint(px, line, glint_t)
    if trail:
        draw_trail(px)
    return img


frames = [
    dict(),                                # frame_00 — plain
    dict(glint_t=0.45),                    # frame_01 — glint midway
    dict(glint_t=0.85, tip_flash=True),    # frame_02 — PEAK at tip
    dict(trail=True),                      # frame_03 — speed lines
]

base = "/home/sparky/ogrs/art/projectiles/2_ranged/frames"
os.makedirs(base, exist_ok=True)
for i, kw in enumerate(frames):
    img = draw_frame(**kw)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print(f"frame_{i:02d}: {kw}")
print("done")
