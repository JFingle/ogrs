#!/usr/bin/env python3
"""
CRUMBLE UNDEAD impact — 48×48, 4 frames.
Holy white/gold burst with literal bone fragments breaking apart and
falling outward. Peak frame: bones crumbling around the target silhouette.

This is the impact that engine should play centered on an undead NPC's
position when Crumble Undead fatally damages them (see ROUTER_NOTES.md
'bones-crumble death animation' engine prereq).
"""
import os, math
from PIL import Image

W = H = 48
CX, CY = 24, 24
TRANS = (0, 0, 0, 0)

CORE_WHITE  = (255, 255, 255, 255)
HOLY_HOT    = (255, 248, 220, 255)
HOLY_GOLD   = (240, 215, 130, 255)
HOLY_DIM    = (180, 150,  80, 255)
HOLY_EDGE   = (110,  90,  40, 255)
BONE_BRIGHT = (240, 232, 200, 255)
BONE_BASE   = (172, 158, 124, 255)
BONE_SHADOW = ( 80,  72,  48, 255)
DUST        = (140, 124,  90, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def in_silhouette(x, y):
    dx, dy = x - CX, y - CY
    if abs(dx) <= 3 and -14 <= dy <= -9: return True
    if abs(dx) <= 4 and -8 <= dy <= 2: return True
    if abs(dx) <= 2 and 3 <= dy <= 12: return True
    if -7 <= dx <= -5 and -6 <= dy <= 2: return True
    if 5 <= dx <= 7 and -6 <= dy <= 2: return True
    return False


def draw_holy_burst(px, radius, peak=False, dim_silhouette=False):
    r2 = radius * radius
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 > r2:
                continue
            t = d2 / r2
            if dim_silhouette and in_silhouette(x, y):
                t = min(1.0, t * 1.8)
            if t < 0.05:
                color = CORE_WHITE if peak else HOLY_HOT
            elif t < 0.25:
                color = HOLY_HOT
            elif t < 0.55:
                color = HOLY_GOLD
            elif t < 0.85:
                color = HOLY_DIM
            else:
                color = HOLY_EDGE
            # Outer dither for soft falloff
            if t > 0.85 and (x + y) % 2 == 1:
                continue
            put(px, x, y, color)


def bone_fragment(px, cx, cy, length, angle_deg):
    """A short straight bone fragment — 3-4 pixels long."""
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    for step in range(length):
        x = cx + int(round(cos_a * step))
        y = cy + int(round(sin_a * step))
        if step == 0:
            put(px, x, y, BONE_BRIGHT)
        elif step == length - 1:
            put(px, x, y, BONE_SHADOW)
        else:
            put(px, x, y, BONE_BASE)


def crumbling_bones(px, frame):
    """Bone fragments flying outward at varying angles and lengths per frame."""
    sets = {
        0: [(20, 22, 3, 200), (30, 26, 3, 20)],
        1: [(14, 18, 3, 210), (34, 22, 3, 30), (24, 12, 3, 270),
            (24, 36, 3, 90), (18, 32, 3, 220)],
        2: [(10, 14, 4, 200), (38, 16, 4, 20),  (12, 36, 4, 220),
            (38, 36, 4, 30),  (24, 6, 4, 270),  (24, 42, 4, 90),
            (8, 24, 4, 180),  (40, 24, 4, 0),
            (16, 8, 3, 250),  (34, 8, 3, 290),  (16, 40, 3, 230),  (34, 40, 3, 310)],
        3: [(4, 12, 4, 200), (44, 14, 4, 20),
            (8, 40, 3, 220), (42, 38, 3, 30), (24, 4, 3, 270), (24, 46, 3, 90)],
    }
    for cx, cy, length, ang_deg in sets[frame]:
        bone_fragment(px, cx, cy, length, ang_deg)


def dust_specks(px, frame):
    """Faint dust specks lingering in the air after the burst."""
    if frame == 3:
        for x, y in [(12, 12), (36, 12), (8, 30), (40, 30), (24, 8), (24, 40),
                     (16, 22), (32, 22)]:
            put(px, x, y, DUST)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        draw_holy_burst(px, radius=6)
        crumbling_bones(px, frame)
    elif frame == 1:
        draw_holy_burst(px, radius=14)
        crumbling_bones(px, frame)
    elif frame == 2:
        draw_holy_burst(px, radius=22, peak=True, dim_silhouette=True)
        crumbling_bones(px, frame)
    elif frame == 3:
        draw_holy_burst(px, radius=10)
        crumbling_bones(px, frame)
        dust_specks(px, frame)
    return img


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/debuff_crumble_undead/impact"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
