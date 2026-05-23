#!/usr/bin/env python3
"""
CRUMBLE UNDEAD projectile — 30×30, 4 frames.
Holy white/gold orb with bone-shard wisps. Distinct from purple Curse
and the menacing Skull sprite: this one is the LIGHT crushing the dark.

Bones (small white shard fragments) orbit a holy core that brightens
to peak. Embedded story: holiness pulverizing undead.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)

CORE_WHITE  = (255, 255, 255, 255)
HOLY_HOT    = (255, 248, 220, 255)
HOLY_GOLD   = (240, 215, 130, 255)
HOLY_DIM    = (180, 150,  80, 255)
HOLY_EDGE   = (110,  90,  40, 255)
BONE_BRIGHT = (240, 232, 200, 255)
BONE_BASE   = (172, 158, 124, 255)
BONE_SHADOW = ( 80,  72,  48, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def draw_core(px, peak=False):
    """Holy orb with white-hot center."""
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                put(px, x, y, CORE_WHITE if peak else HOLY_HOT)
            elif d2 <= 4:
                put(px, x, y, HOLY_HOT)
            elif d2 <= 9:
                put(px, x, y, HOLY_GOLD)
            elif d2 <= 16:
                put(px, x, y, HOLY_DIM)
            elif d2 <= 25:
                put(px, x, y, HOLY_EDGE)


def draw_bone_shard(px, cx, cy, dx_dir, dy_dir):
    """Tiny bone shard — 3-pixel chunk with highlight."""
    put(px, cx, cy, BONE_BASE)
    put(px, cx + dx_dir, cy + dy_dir, BONE_BRIGHT)
    put(px, cx - dx_dir, cy - dy_dir, BONE_SHADOW)


def draw_orbiting_bones(px, frame):
    """5-7 bone shards orbiting at varying radius, rotating per frame."""
    counts = [5, 6, 7, 5]
    radii  = [8, 9, 10, 9]
    n = counts[frame]
    r = radii[frame]
    offset = frame * 25
    for i in range(n):
        ang = math.radians(i * (360 / n) + offset)
        cx = CX + int(round(math.cos(ang) * r))
        cy = CY + int(round(math.sin(ang) * r))
        dx_dir = int(round(-math.sin(ang)))  # tangent direction
        dy_dir = int(round(math.cos(ang)))
        if dx_dir == 0 and dy_dir == 0:
            dx_dir = 1
        draw_bone_shard(px, cx, cy, dx_dir, dy_dir)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_core(px, peak=(frame == 2))
    draw_orbiting_bones(px, frame)
    return img


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/debuff_crumble_undead/frames"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print("done")
