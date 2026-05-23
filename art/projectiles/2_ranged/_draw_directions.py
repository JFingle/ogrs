#!/usr/bin/env python3
"""
RANGED arrow — 8 directional sprite variants for in-game flight rotation.
Each variant is the arrow rotated to point in one of 8 compass directions:
N, NE, E, SE, S, SW, W, NW. 30×30 canvas, transparent background.

Engine will pick the variant whose direction is closest to the projectile
flight angle (caster → target). That's engine work, not in scope here —
the art ships ready.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 15, 15
TRANS = (0, 0, 0, 0)

WOOD_HI    = (168, 114,  58, 255)
WOOD_BASE  = (139,  90,  43, 255)
WOOD_SHADE = ( 92,  58,  26, 255)
TIP_HI     = (220, 220, 230, 255)
TIP_SHADE  = ( 78,  82,  98, 255)
TIP_OUTLINE= ( 40,  44,  56, 255)
FLETCH_RED = (180,  55,  55, 255)
FLETCH_RED2= (120,  40,  40, 255)
GLINT      = (255, 255, 255, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


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


# Arrow length and orientation:
# tip is at +AXIS distance from center, tail at -AXIS distance.
ARROW_HALF = 11   # half-length of the arrow in pixels
TIP_INSET = 2     # how many pixels the iron head occupies from the tip


def arrow_geom(angle_deg):
    """Return (tail_x, tail_y, tip_x, tip_y) for an arrow pointing at angle_deg.
    0° = East (positive X), -90° = North (negative Y in screen coords)."""
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    tip_x  = CX + int(round(cos_a * ARROW_HALF))
    tip_y  = CY + int(round(sin_a * ARROW_HALF))
    tail_x = CX - int(round(cos_a * ARROW_HALF))
    tail_y = CY - int(round(sin_a * ARROW_HALF))
    return tail_x, tail_y, tip_x, tip_y


def draw_arrow(angle_deg, glint_t=None, tip_flash=False):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()

    tail_x, tail_y, tip_x, tip_y = arrow_geom(angle_deg)
    line = bresenham(tail_x, tail_y, tip_x, tip_y)

    # Body (skip first/last 2 cells — those are tail+tip drawn separately)
    body = line[2:-2]
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    # Perpendicular for highlight/shadow offsets
    perp_x = int(round(-sin_a))
    perp_y = int(round(cos_a))
    for (x, y) in body:
        put(px, x, y, WOOD_BASE)
        # Highlight on one side, shadow on the other
        put(px, x + perp_x, y + perp_y, WOOD_SHADE)
        put(px, x - perp_x, y - perp_y, WOOD_HI)

    # Tip — iron head as a small chunk at the tip, with outline cells perpendicular to flight
    # Step inward from the tip a bit to draw the head body
    head_cells = []
    for back_step in range(3):
        cx_h = tip_x - int(round(cos_a * back_step))
        cy_h = tip_y - int(round(sin_a * back_step))
        head_cells.append((cx_h, cy_h))
        # Side widening to form an arrow-head triangle
        if back_step >= 1:
            head_cells.append((cx_h + perp_x, cy_h + perp_y))
            head_cells.append((cx_h - perp_x, cy_h - perp_y))
    # Draw the head body
    for hx, hy in head_cells:
        put(px, hx, hy, TIP_HI)
    # Outline around the tip
    outline_offsets = [(perp_x * 2, perp_y * 2), (-perp_x * 2, -perp_y * 2),
                      (int(round(cos_a * 1)), int(round(sin_a * 1)))]
    for ox, oy in outline_offsets:
        put(px, tip_x + ox, tip_y + oy, TIP_OUTLINE)

    # Tail / fletching — red feather cluster behind the tail
    # Draw 2 rows of red pixels perpendicular to flight, just behind tail
    for back_step in range(0, 2):
        bx = tail_x + int(round(cos_a * back_step))
        by = tail_y + int(round(sin_a * back_step))
        for side in (-1, 0, 1):
            put(px, bx + perp_x * side, by + perp_y * side, FLETCH_RED if side != 1 else FLETCH_RED2)

    # Glint along shaft
    if glint_t is not None:
        idx = int(glint_t * (len(line) - 1))
        x, y = line[idx]
        put(px, x, y, GLINT)

    if tip_flash:
        put(px, tip_x, tip_y, GLINT)

    return img


DIRECTIONS = [
    ("N",  -90),
    ("NE", -45),
    ("E",   0),
    ("SE",  45),
    ("S",   90),
    ("SW", 135),
    ("W",  180),
    ("NW", 225),  # equivalent to -135
]


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/2_ranged/directions"
    os.makedirs(base, exist_ok=True)
    for name, angle in DIRECTIONS:
        img = draw_arrow(angle, glint_t=0.5, tip_flash=False)
        img.save(f"{base}/arrow_{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/arrow_{name}_x8.png")
        print(f"arrow_{name}: {angle}°")
    print("done")
