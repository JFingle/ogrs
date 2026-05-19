#!/usr/bin/env python3
"""
Procedural ORB projectile — Wind / Air spells + Saradomin Strike + mithril arrows.
Reads as 'blessed gust': pale gold core, white halo, 3 radial wind streaks that rotate.
4-frame breathing animation, frame 02 = peak brightness.
"""
import math
from PIL import Image

W = H = 30
CX, CY = 14, 14   # bias slightly upper-left for a "leading edge" feel

TRANSPARENT     = (0, 0, 0, 0)
CORE_PEAK       = (255, 255, 255, 255)  # frame 02 only
CORE_HIGHLIGHT  = (255, 247, 208, 255)  # FFF7D0
CORE_BASE       = (245, 230, 160, 255)  # F5E6A0
CORE_SHADE      = (217, 194, 104, 255)  # D9C268
HALO_BRIGHT     = (232, 237, 245, 255)  # E8EDF5
HALO_DIM        = (185, 196, 212, 255)  # B9C4D4
STREAK_BRIGHT   = (255, 255, 255, 255)
STREAK_MID      = (210, 220, 240, 255)
STREAK_DIM      = (122, 143, 173, 255)


def in_bounds(x, y):
    return 0 <= x < W and 0 <= y < H


def put(px, x, y, color):
    if in_bounds(x, y):
        px[x, y] = color


def draw_core(px, peak=False, halo_intensity=1.0):
    """Filled circle with 3 value bands + 1-px halo ring."""
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                px[x, y] = CORE_PEAK if peak else CORE_HIGHLIGHT
            elif d2 <= 4:
                px[x, y] = CORE_HIGHLIGHT
            elif d2 <= 10:
                px[x, y] = CORE_BASE
            elif d2 <= 16:
                px[x, y] = CORE_SHADE
            elif d2 <= 25:
                # Halo ring — skip random cells for soft edge
                if halo_intensity >= 1.0:
                    px[x, y] = HALO_BRIGHT
                elif halo_intensity >= 0.5:
                    if (x + y) % 2 == 0:
                        px[x, y] = HALO_BRIGHT
                    else:
                        px[x, y] = HALO_DIM
                else:
                    if (x + y) % 2 == 0:
                        px[x, y] = HALO_DIM


def draw_streak(px, angle_deg, start_r, end_r):
    """Radial streak from (CX, CY) along angle, between radii."""
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    # Walk along the ray with sub-pixel steps so the line is continuous.
    plotted = set()
    for step in range(start_r * 4, end_r * 4 + 1):
        r = step / 4.0
        x = int(round(CX + cos_a * r))
        y = int(round(CY + sin_a * r))
        if (x, y) in plotted:
            continue
        plotted.add((x, y))
        # Color by position along streak.
        if r <= start_r + 1.5:
            color = STREAK_BRIGHT
        elif r <= start_r + 3.5:
            color = STREAK_MID
        else:
            color = STREAK_DIM
        put(px, x, y, color)


def draw_frame(rotation_deg, peak=False, halo=1.0, streak_len=5):
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    px = img.load()
    draw_core(px, peak=peak, halo_intensity=halo)
    # 3 radial streaks at 120° offsets, rotating each frame.
    start_r = 6
    end_r = start_r + streak_len
    for base in (0, 120, 240):
        draw_streak(px, base + rotation_deg, start_r, end_r)
    return img


frames = [
    # (rotation, peak, halo, streak_len)
    (  0, False, 0.5, 5),   # frame_00 — base, dim halo
    ( 30, False, 1.0, 6),   # frame_01 — halo brightening, streaks extending
    ( 60,  True, 1.0, 6),   # frame_02 — PEAK: white core, bright halo
    ( 90, False, 0.5, 5),   # frame_03 — fading, streaks pulling back
]

base = "/home/sparky/ogrs/art/projectiles/0_orb/frames"
for i, (rot, peak, halo, slen) in enumerate(frames):
    img = draw_frame(rot, peak, halo, slen)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print(f"frame_{i:02d}: rot={rot}° peak={peak} halo={halo} streak={slen}")
print("done")
