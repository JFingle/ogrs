#!/usr/bin/env python3
"""
ENFEEBLE debuff projectile (v2 — larger + fancier).
Bigger amorphous yellow-green poison cloud filling more of the 30×30
canvas, with 3 wispy tendrils trailing outward and a glowing toxic
core at peak. Distinct from Weaken (droplet) and Confuse (purple swirl).
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)

SICK_DEEP    = ( 42,  46,  12, 255)
SICK_BASE    = ( 80,  78,  28, 255)
SICK_MID     = (140, 132,  64, 255)
SICK_PALE    = (188, 180,  96, 255)
SICK_HIGH    = (228, 220, 140, 255)
SICK_GLOW    = (255, 245, 180, 255)
SICK_WHITE   = (255, 255, 220, 255)
TOXIC_BRIGHT = (170, 200,  80, 255)
TOXIC_DIM    = ( 88, 112,  40, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def stable_hash(x, y, salt=0):
    v = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    return (v & 0xFFFF) / 0xFFFF


def cloud_density(x, y, frame, scale=1.0):
    """0..1 cloud thickness with per-frame noise drift."""
    dx, dy = x - CX, y - CY
    d_ellip = math.sqrt((dx / 1.15) ** 2 + (dy / 1.0) ** 2)
    base = max(0, 1 - d_ellip / (11.5 * scale))
    noise = stable_hash(x + frame * 2, y - frame, salt=frame * 7)
    density = base * (0.6 + 0.7 * noise)
    return density


def draw_cloud(px, frame, peak=False):
    """Layered cloud — bigger and richer than v1."""
    scale = 1.0
    bands = [
        (0.08, SICK_DEEP),
        (0.22, SICK_BASE),
        (0.40, SICK_MID),
        (0.60, SICK_PALE),
        (0.80, SICK_HIGH),
    ]
    if peak:
        bands.append((0.92, SICK_GLOW))
        bands.append((0.97, SICK_WHITE))
    for x in range(W):
        for y in range(H):
            d = cloud_density(x, y, frame, scale)
            for thresh, color in reversed(bands):
                if d > thresh:
                    put(px, x, y, color)
                    break


def draw_tendrils(px, frame):
    """3 wispy toxic tendrils trailing outward from the cloud."""
    # Each tendril is a curving line of pixels at a base angle, with frame-based wave.
    angles = [30, 150, 270]
    angle_offset = frame * 15
    for base in angles:
        ang = math.radians(base + angle_offset)
        for step in range(10, 16):
            # Curve the tendril by varying the angle slightly with step
            wave = math.sin(step / 2.0 + frame) * 0.3
            cos_a = math.cos(ang + wave)
            sin_a = math.sin(ang + wave)
            x = CX + int(round(cos_a * step))
            y = CY + int(round(sin_a * step))
            # Color by step depth
            if step <= 11:
                color = SICK_PALE
            elif step <= 13:
                color = SICK_BASE
            else:
                color = SICK_DEEP
            put(px, x, y, color)
        # Tip — a brighter toxic spec at the end of each tendril
        tip_step = 14
        x = CX + int(round(math.cos(ang) * tip_step))
        y = CY + int(round(math.sin(ang) * tip_step))
        put(px, x, y, TOXIC_DIM)


def draw_inner_specks(px, frame):
    """A few bright toxic-green specks inside the cloud — visual interest."""
    sets = {
        0: [(11, 12, TOXIC_BRIGHT), (17, 15, TOXIC_DIM)],
        1: [(13, 11, TOXIC_BRIGHT), (16, 16, TOXIC_BRIGHT)],
        2: [(11, 13, TOXIC_BRIGHT), (17, 12, TOXIC_BRIGHT),
            (14, 17, TOXIC_BRIGHT), (12, 16, TOXIC_DIM)],
        3: [(15, 14, TOXIC_DIM), (12, 15, TOXIC_DIM)],
    }
    for x, y, c in sets[frame]:
        put(px, x, y, c)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_cloud(px, frame, peak=(frame == 2))
    draw_tendrils(px, frame)
    draw_inner_specks(px, frame)
    return img


base = "/home/sparky/ogrs/art/projectiles/debuff_enfeeble/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
print("done")
