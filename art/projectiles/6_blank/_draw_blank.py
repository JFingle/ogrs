#!/usr/bin/env python3
"""
Procedural BLANK projectile — tiny dart flicker.
Intentionally minimal: a 2-3 pixel silver streak that twinkles per frame.
"""
import os
from PIL import Image

W = H = 30
TRANS    = (0, 0, 0, 0)
TIP      = (255, 255, 255, 255)
BODY     = (216, 216, 216, 255)
TRAIL    = (128, 128, 136, 255)
DIM      = ( 74,  74,  82, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        # Two-pixel streak biased upper-right
        put(px, 15, 14, BODY)
        put(px, 14, 15, TRAIL)
    elif frame == 1:
        # Slight shift
        put(px, 16, 13, BODY)
        put(px, 15, 14, TRAIL)
        put(px, 14, 15, DIM)
    elif frame == 2:
        # PEAK — 3 pixel streak with white tip
        put(px, 17, 12, TIP)
        put(px, 16, 13, BODY)
        put(px, 15, 14, TRAIL)
        put(px, 14, 15, DIM)
    elif frame == 3:
        # Single faint dot
        put(px, 17, 12, TRAIL)
        put(px, 16, 13, DIM)
    return img


base = "/home/sparky/ogrs/art/projectiles/6_blank/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print(f"frame_{i:02d}")
print("done")
