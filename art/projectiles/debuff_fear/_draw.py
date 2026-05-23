#!/usr/bin/env python3
"""
FEAR (retro) projectile — 30×30, 4 frames.
A dark-purple wisp with a ghostly recoiling shape. Smaller and quieter
than Confuse — fear is internal, not flashy. Two eye-pinprick dots
glow within the wisp for an unsettling face suggestion.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)

WISP_DEEP   = ( 30,  18,  44, 255)
WISP_BASE   = ( 70,  48,  96, 255)
WISP_MID    = (108,  78, 140, 255)
WISP_PALE   = (160, 132, 186, 255)
EYE_RED     = (220,  40,  40, 255)
EYE_DIM     = (140,  20,  20, 255)
TRAIL       = ( 60,  40,  82, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def stable_hash(x, y, salt=0):
    v = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    return (v & 0xFFFF) / 0xFFFF


def draw_wisp(px, frame, expand=1.0):
    """Amorphous purple wisp with ragged edges — uses noise for organic feel."""
    radius = 6 * expand
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            # Slight vertical elongation for a "wisp" feel
            d_ellip = math.sqrt((dx / 1.0) ** 2 + (dy / 1.3) ** 2)
            base = max(0, 1 - d_ellip / radius)
            noise = stable_hash(x + frame, y - frame, salt=frame * 5)
            density = base * (0.55 + 0.7 * noise)
            if density > 0.85:
                put(px, x, y, WISP_PALE)
            elif density > 0.6:
                put(px, x, y, WISP_MID)
            elif density > 0.35:
                put(px, x, y, WISP_BASE)
            elif density > 0.12:
                put(px, x, y, WISP_DEEP)


def draw_eyes(px, frame):
    """Two glowing red dots — the 'face' inside the wisp."""
    # Slight horizontal jitter per frame so they feel alive
    offset = [(0, 0), (1, 0), (0, 0), (-1, 0)][frame]
    bright = (frame == 2)
    for dx in (-2, 2):
        x = CX + dx + offset[0]
        y = CY - 1 + offset[1]
        put(px, x, y, EYE_RED if bright else EYE_DIM)


def draw_recoil_trail(px, frame):
    """Wisps trailing behind the head — suggests the spell is recoiling."""
    # Trail extends backward (down-left direction) as if pulling away
    trails = {
        0: [(8, 22), (6, 24)],
        1: [(9, 23), (7, 25), (10, 21)],
        2: [(7, 24), (5, 26), (9, 22), (11, 20)],
        3: [(8, 23), (10, 22)],
    }
    for x, y in trails[frame]:
        put(px, x, y, TRAIL)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    expand = [0.9, 1.0, 1.1, 1.0][frame]
    draw_wisp(px, frame, expand=expand)
    draw_recoil_trail(px, frame)
    draw_eyes(px, frame)
    return img


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/debuff_fear/frames"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print("done")
