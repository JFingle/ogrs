#!/usr/bin/env python3
"""
FIRE flame — 8 directional sprite variants.
Flame teardrop is rotated so its hot tip leads in the direction of flight
(N, NE, E, SE, S, SW, W, NW). Defined in 'local' frame with tip on +X axis,
then rotated per direction. 30×30 canvas, transparent background.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)

CORE_WHITE  = (255, 255, 255, 255)
CORE_HOT    = (255, 240, 180, 255)
CORE_YELLOW = (255, 200,  80, 255)
CORE_ORANGE = (255, 120,  40, 255)
CORE_RED    = (210,  50,  30, 255)
CORE_DEEP   = (130,  20,  20, 255)
SMOKE       = (110,  60,  50, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def teardrop_cell(lx, ly):
    """Return color for a local-frame coord, or None if outside the teardrop.
    Tip at (+8, 0), wide base around (-6, 0). +X axis is the leading direction."""
    # Allowed half-width per longitudinal position lx
    if lx > 7:
        return None
    if lx >= 5:
        # Hot bright tip
        max_half = max(0, 2 - (lx - 5) * 0.7)
    elif lx >= -2:
        # Body — widest in middle
        max_half = 3 + (0.5 if -1 <= lx <= 2 else 0)
    elif lx >= -6:
        # Tail / base — slightly narrower
        max_half = 3 - (abs(lx + 4) * 0.4)
    else:
        return None
    if abs(ly) > max_half:
        return None

    # Distance from the brightest center (around lx=2..5, ly=0)
    bright_x = 3
    d_bright = math.sqrt((lx - bright_x) ** 2 + (ly * 1.2) ** 2)

    if d_bright < 1.0:
        return CORE_WHITE
    if d_bright < 2.0:
        return CORE_HOT
    if d_bright < 3.5:
        return CORE_YELLOW
    if d_bright < 5.0:
        return CORE_ORANGE
    if d_bright < 6.5:
        return CORE_RED
    if d_bright < 7.5:
        return CORE_DEEP
    return SMOKE


def draw_flame(angle_deg, ember_count=3):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    # Sample local-frame pixels and rotate to screen
    for lx in range(-7, 9):
        for ly in range(-5, 6):
            color = teardrop_cell(lx, ly)
            if color is None:
                continue
            # Rotate to screen
            sx = CX + int(round(cos_a * lx - sin_a * ly))
            sy = CY + int(round(sin_a * lx + cos_a * ly))
            put(px, sx, sy, color)

    # Embers ahead of the tip — ember_count specks at +X positions
    for i in range(ember_count):
        local_x = 9 + i
        local_y = (-1) ** i
        sx = CX + int(round(cos_a * local_x - sin_a * local_y))
        sy = CY + int(round(sin_a * local_x + cos_a * local_y))
        color = CORE_HOT if i == 0 else CORE_ORANGE
        put(px, sx, sy, color)

    return img


DIRECTIONS = [
    ("N",  -90),
    ("NE", -45),
    ("E",   0),
    ("SE",  45),
    ("S",   90),
    ("SW", 135),
    ("W",  180),
    ("NW", -135),
]


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/element_fire/directions"
    os.makedirs(base, exist_ok=True)
    for name, angle in DIRECTIONS:
        img = draw_flame(angle)
        img.save(f"{base}/flame_{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/flame_{name}_x8.png")
        print(f"flame_{name}: {angle}°")
    print("done")
