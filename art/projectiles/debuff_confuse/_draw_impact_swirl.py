#!/usr/bin/env python3
"""
CONFUSE triple-helix swirl — 48×48, 4 frames.
Three purple ribbons spiral around the target. Leading edges carry tiny
'?' glyphs that travel up with the swirl. Distinct purple-mystic feel.
"""
import os, math
from PIL import Image

W = H = 48
CX = 24
TARGET_TOP, TARGET_BOTTOM = 6, 42
TARGET_H = TARGET_BOTTOM - TARGET_TOP

TRANS = (0, 0, 0, 0)
P_DEEP   = ( 58,  26,  96, 255)
P_MID    = (106,  58, 160, 255)
P_BRIGHT = (176, 128, 224, 255)
P_HIGH   = (232, 204, 255, 255)
WHITE    = (255, 255, 255, 255)

RADIUS      = 10
TURNS       = 2.4
TAIL_LENGTH = 18
NUM_HELICES = 3


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def spiral_angle(y, frame, off):
    progress = (TARGET_BOTTOM - y) / TARGET_H
    return progress * (TURNS * 2 * math.pi) + frame * (math.pi / 3) + math.radians(off)


def spiral_x(y, frame, off):
    return CX + RADIUS * math.cos(spiral_angle(y, frame, off))


def depth_factor(y, frame, off):
    return math.sin(spiral_angle(y, frame, off))


def leading_y(frame):
    return [42, 30, 18, 6][frame]


def color_for_swirl(intensity, depth, peak=False):
    front = depth > 0.3
    side = -0.3 <= depth <= 0.3
    if peak and intensity > 0.85 and front:
        return WHITE
    if intensity >= 0.85:
        return P_HIGH if front else (P_BRIGHT if side else P_MID)
    if intensity >= 0.6:
        return P_BRIGHT if front else (P_MID if side else P_DEEP)
    if intensity >= 0.35:
        return P_MID if front else P_DEEP
    if intensity >= 0.15:
        return P_DEEP
    return None


def draw_helix(px, frame, off):
    lead = leading_y(frame)
    tail = lead + TAIL_LENGTH
    peak = (frame == 2)
    for y4 in range(tail * 4, (lead - 1) * 4 - 1, -1):
        y = y4 / 4.0
        if not (lead <= y <= tail):
            continue
        sx = spiral_x(y, frame, off)
        depth = depth_factor(y, frame, off)
        intensity = (tail - y) / TAIL_LENGTH
        ix, iy = int(round(sx)), int(round(y))
        c = color_for_swirl(intensity, depth, peak=peak)
        put(px, ix, iy, c)
        if abs(depth) < 0.6 and intensity > 0.3:
            put(px, ix + 1, iy, color_for_swirl(intensity * 0.7, depth, peak=peak))


def draw_q(px, cx, cy):
    """Tiny ? glyph at the leading edge."""
    cells = [(0, -1), (1, -1), (-1, 0), (2, 0), (2, 1), (1, 2), (1, 4)]
    for ox, oy in cells:
        put(px, cx + ox, cy + oy, WHITE)


def draw_lead_q(px, frame, off, bright=True):
    lead = leading_y(frame)
    sx = spiral_x(lead, frame, off)
    ix, iy = int(round(sx)), int(round(lead))
    draw_q(px, ix, iy - 2)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    for i in range(NUM_HELICES):
        draw_helix(px, frame, i * (360 / NUM_HELICES))
    # Question marks at all 3 leading edges
    for i in range(NUM_HELICES):
        draw_lead_q(px, frame, i * (360 / NUM_HELICES))
    return img


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/debuff_confuse/impact_swirl"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
