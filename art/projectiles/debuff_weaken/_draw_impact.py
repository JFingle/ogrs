#!/usr/bin/env python3
"""
WEAKEN radial impact — 48×48, 4 frames.
Olive-green aura wraps the target with sap-drip trails running DOWNWARD
from the body. The "draining" theme: stuff is being pulled out of them.
Peak frame has the densest drips + olive haze around the silhouette.
"""
import os, math
from PIL import Image

W = H = 48
CX, CY = 24, 24
TRANS = (0, 0, 0, 0)

OUTLINE  = ( 42,  45,  20, 255)
DEEP     = ( 74,  80,  40, 255)
BASE     = (107, 116,  56, 255)
MID      = (139, 144,  80, 255)
PALE     = (168, 176, 112, 255)
HIGH     = (192, 196, 144, 255)
DRIP_HI  = (139, 144,  80, 255)
DRIP_LO  = ( 74,  80,  40, 255)
DRIP_DK  = ( 42,  45,  20, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def draw_aura(px, radius_sq):
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= radius_sq:
                if d2 <= radius_sq * 0.10:
                    put(px, x, y, HIGH)
                elif d2 <= radius_sq * 0.30:
                    put(px, x, y, PALE)
                elif d2 <= radius_sq * 0.60:
                    put(px, x, y, MID)
                elif d2 <= radius_sq * 0.85:
                    put(px, x, y, BASE)
                else:
                    if (x + y) % 2 == 0:
                        put(px, x, y, BASE)
                    else:
                        put(px, x, y, DEEP)


def draw_drips(px, count, max_length, x_radius=14):
    """Vertical drip trails running downward from the aura. Each drip
    occupies one column of pixels, brightest at the top fading to dark."""
    drip_offsets = []
    # Spread drips along x within +/- x_radius
    for i in range(count):
        x_off = -x_radius + int((2 * x_radius) * i / max(1, count - 1))
        # Slight vertical offset so they don't all start at the same y
        y_off = ((i * 7) % 5)
        drip_offsets.append((x_off, y_off))
    for x_off, y_off in drip_offsets:
        x = CX + x_off
        for step in range(max_length):
            y = CY + y_off + step
            if step < 1:
                color = DRIP_HI
            elif step < max_length - 2:
                color = DRIP_LO
            else:
                color = DRIP_DK
            put(px, x, y, color)


def draw_drop_specks(px, count, spread):
    """A few drip droplets that have separated from the trails."""
    angles = [(-12, 18), (10, 22), (-6, 28), (8, 32), (-14, 24), (4, 38)]
    for i in range(min(count, len(angles))):
        x_off, y_off = angles[i]
        put(px, CX + x_off, CY + y_off, DRIP_LO)
        put(px, CX + x_off, CY + y_off - 1, DRIP_HI)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        draw_aura(px, radius_sq=36)
        draw_drips(px, count=3, max_length=6, x_radius=4)
    elif frame == 1:
        draw_aura(px, radius_sq=140)
        draw_drips(px, count=5, max_length=10, x_radius=8)
        draw_drop_specks(px, count=2, spread=14)
    elif frame == 2:
        # PEAK — wide olive aura with many drip trails
        draw_aura(px, radius_sq=300)
        draw_drips(px, count=9, max_length=14, x_radius=12)
        draw_drop_specks(px, count=4, spread=18)
    elif frame == 3:
        # Dissipating — fewer drips, fading aura
        draw_aura(px, radius_sq=160)
        draw_drips(px, count=5, max_length=8, x_radius=10)
        draw_drop_specks(px, count=3, spread=18)
    return img


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/debuff_weaken/impact"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
