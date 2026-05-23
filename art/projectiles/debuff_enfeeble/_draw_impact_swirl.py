#!/usr/bin/env python3
"""
ENFEEBLE impact swirl (triple-helix) — 48×48, 4 frames.
Three toxic mist ribbons wrap and travel up the target.
Thicker bands than STUN (mist, not lightning).
"""
import os, math
from PIL import Image

W = H = 48
CX = 24
TARGET_TOP, TARGET_BOTTOM = 6, 42
TARGET_H = TARGET_BOTTOM - TARGET_TOP

TRANS = (0, 0, 0, 0)
DEEP    = ( 42,  46,  12, 255)
BASE    = ( 80,  78,  28, 255)
MID     = (140, 132,  64, 255)
PALE    = (188, 180,  96, 255)
HIGH    = (228, 220, 140, 255)
GLOW    = (255, 245, 180, 255)
TOXIC   = (170, 200,  80, 255)

RADIUS      = 11
TURNS       = 2.2
TAIL_LENGTH = 20
NUM_HELICES = 3


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def stable_hash(x, y, salt=0):
    v = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    return (v & 0xFFFF) / 0xFFFF


def spiral_angle(y, frame, helix_offset_deg):
    progress = (TARGET_BOTTOM - y) / TARGET_H
    return (progress * (TURNS * 2 * math.pi)
            + frame * (math.pi / 3)
            + math.radians(helix_offset_deg))


def spiral_x(y, frame, off):
    return CX + RADIUS * math.cos(spiral_angle(y, frame, off))


def depth_factor(y, frame, off):
    return math.sin(spiral_angle(y, frame, off))


def leading_y(frame):
    return [44, 32, 20, 8][frame]


def color_for_swirl(intensity, depth, peak=False):
    front = depth > 0.3
    side = -0.3 <= depth <= 0.3
    if peak and intensity > 0.85 and front:
        return GLOW
    if intensity >= 0.85:
        return HIGH if front else (PALE if side else MID)
    if intensity >= 0.6:
        return PALE if front else (MID if side else BASE)
    if intensity >= 0.35:
        return MID if front else (BASE if side else DEEP)
    if intensity >= 0.15:
        return BASE if front or side else DEEP
    return DEEP


def draw_helix(px, frame, helix_offset_deg):
    lead = leading_y(frame)
    tail = lead + TAIL_LENGTH
    peak = (frame == 2)
    for y4 in range(tail * 4, (lead - 1) * 4 - 1, -1):
        y = y4 / 4.0
        if not (lead <= y <= tail):
            continue
        sx = spiral_x(y, frame, helix_offset_deg)
        depth = depth_factor(y, frame, helix_offset_deg)
        intensity = (tail - y) / TAIL_LENGTH
        ix, iy = int(round(sx)), int(round(y))
        # 3-px thick mist band with fuzzy outer pixels
        for offset in (-1, 0, 1):
            c = color_for_swirl(intensity * (0.7 if offset != 0 else 1.0), depth, peak=peak)
            if offset != 0:
                n = stable_hash(ix + offset, iy, salt=frame * 7 + int(helix_offset_deg))
                if n < 0.4:
                    continue
            put(px, ix + offset, iy, c)


def draw_drifting_specks(px, frame):
    """Toxic specks drifting near the leading edges of each helix."""
    for helix in range(NUM_HELICES):
        offset = helix * (360 / NUM_HELICES)
        lead = leading_y(frame)
        sx = spiral_x(lead, frame, offset)
        ix = int(round(sx))
        # Spec near each leading edge
        if frame in (2, 3):
            put(px, ix + 1, lead - 2, TOXIC)
            put(px, ix - 1, lead - 1, GLOW if frame == 2 else PALE)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    for i in range(NUM_HELICES):
        draw_helix(px, frame, i * (360 / NUM_HELICES))
    draw_drifting_specks(px, frame)
    return img



if __name__ == "__main__":

    base = "/home/sparky/ogrs/art/projectiles/debuff_enfeeble/impact_swirl"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
