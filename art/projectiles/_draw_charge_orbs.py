#!/usr/bin/env python3
"""
4 charge-orb spells — Air / Water / Earth / Fire orb charging.
Each shows an elemental swirl FLOWING INTO an empty orb shape (the
unfilled orb's silhouette is visible). Per-frame, the elemental energy
intensifies as the orb is "charged." Element-distinct hue per orb.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# Generic empty-orb silhouette — circular outline that the element fills into.
ORB_OUTLINE = ( 50,  50,  60, 255)
ORB_GLASS   = (120, 130, 150, 255)
ORB_DARK    = ( 20,  20,  30, 255)


def draw_orb_shell(px, fill_color, fill_intensity, ring_color=None):
    """Draw an empty glass orb with the element filling at fill_intensity (0..1)."""
    # Outer outline at radius ~7
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 49 and d2 > 36:
                # Glass outline ring
                put(px, x, y, ring_color or ORB_OUTLINE)
            elif d2 <= 36 and d2 > 25:
                # Inner glass ring (faint)
                put(px, x, y, ORB_GLASS)
    # Element filling — bottom-up fill
    fill_height = int(round(fill_intensity * 12))
    fill_top_y = CY + 6 - fill_height
    for x in range(W):
        for y in range(W):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 30 and y >= fill_top_y:
                # Inside orb + below fill line
                put(px, x, y, fill_color)


def swirl_streaks(px, element_color, frame, accent_color):
    """Element streaks swirling around / into the orb."""
    offset = frame * 35
    radii = [12, 11, 10, 11]
    r = radii[frame]
    for i in range(4):
        ang = math.radians(i * 90 + offset)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        for step in range(2, 5):
            x = CX + int(round(cos_a * r * (1 - step * 0.1)))
            y = CY + int(round(sin_a * r * (1 - step * 0.1)))
            color = element_color if step <= 2 else accent_color
            put(px, x, y, color)


# ===========================================================
# AIR ORB — pale gold + cream swirl
# ===========================================================
AIR_CORE  = (255, 247, 208, 255)
AIR_BASE  = (240, 220, 150, 255)
AIR_DIM   = (180, 160, 100, 255)


def air_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    fill = [0.2, 0.4, 0.7, 0.9][frame]
    draw_orb_shell(px, AIR_BASE, fill)
    swirl_streaks(px, AIR_CORE, frame, AIR_DIM)
    if frame == 2:
        # Bright center at peak charge
        put(px, CX, CY, (255, 255, 255, 255))
    return img


# ===========================================================
# WATER ORB — ice-blue swirl
# ===========================================================
WATER_CORE = (255, 255, 255, 255)
WATER_BASE = (168, 222, 255, 255)
WATER_DIM  = ( 91, 168, 229, 255)


def water_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    fill = [0.2, 0.4, 0.7, 0.9][frame]
    draw_orb_shell(px, WATER_BASE, fill)
    swirl_streaks(px, WATER_CORE, frame, WATER_DIM)
    if frame == 2:
        put(px, CX, CY, WATER_CORE)
    return img


# ===========================================================
# EARTH ORB — brown/green swirl
# ===========================================================
EARTH_CORE = (168, 208,  96, 255)
EARTH_BASE = (107,  69,  32, 255)
EARTH_DIM  = ( 58,  40,  24, 255)


def earth_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    fill = [0.2, 0.4, 0.7, 0.9][frame]
    draw_orb_shell(px, EARTH_BASE, fill)
    swirl_streaks(px, EARTH_CORE, frame, EARTH_DIM)
    if frame == 2:
        put(px, CX, CY, EARTH_CORE)
    return img


# ===========================================================
# FIRE ORB — red/orange swirl
# ===========================================================
FIRE_CORE = (255, 255, 220, 255)
FIRE_BASE = (255, 120,  40, 255)
FIRE_DIM  = (130,  20,  20, 255)


def fire_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    fill = [0.2, 0.4, 0.7, 0.9][frame]
    draw_orb_shell(px, FIRE_BASE, fill)
    swirl_streaks(px, FIRE_CORE, frame, FIRE_DIM)
    if frame == 2:
        put(px, CX, CY, FIRE_CORE)
    return img


SPELLS = [
    ("charge_air_orb",   air_frame),
    ("charge_water_orb", water_frame),
    ("charge_earth_orb", earth_frame),
    ("charge_fire_orb",  fire_frame),
]

if __name__ == "__main__":
    for folder, fn in SPELLS:
        out = f"/home/sparky/ogrs/art/projectiles/{folder}/frames"
        os.makedirs(out, exist_ok=True)
        for i in range(4):
            img = fn(i)
            img.save(f"{out}/frame_{i:02d}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/frame_{i:02d}_x8.png")
        print(f"done: {folder}")
