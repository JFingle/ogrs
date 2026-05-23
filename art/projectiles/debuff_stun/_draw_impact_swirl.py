#!/usr/bin/env python3
"""
STUN impact swirl (triple-helix) — 48×48, 4 frames.
Three lightning ribbons offset 120° apart wrap around the target and
travel bottom-to-top. Each ribbon is depth-shaded so we see the 3D
helix illusion: front-facing pixels bright, back-facing pixels dim.
"""
import os, math
from PIL import Image

W = H = 48
CX = 24
TARGET_TOP, TARGET_BOTTOM = 6, 42
TARGET_H = TARGET_BOTTOM - TARGET_TOP

TRANS    = (0, 0, 0, 0)
WHITE    = (255, 255, 255, 255)
HOT_YEL  = (255, 255, 160, 255)
GOLD     = (240, 192,   0, 255)
DIM_GOLD = (176, 128,   0, 255)
EDGE     = ( 96,  70,   8, 255)
ARC      = (255, 220, 100, 255)
SPARK    = (255, 240, 180, 255)

RADIUS      = 10
TURNS       = 2.5
TAIL_LENGTH = 18
NUM_HELICES = 3   # triple helix


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def spiral_angle(y, frame, helix_offset_deg):
    progress = (TARGET_BOTTOM - y) / TARGET_H
    return (progress * (TURNS * 2 * math.pi)
            + frame * (math.pi / 3)
            + math.radians(helix_offset_deg))


def spiral_x(y, frame, helix_offset_deg):
    return CX + RADIUS * math.cos(spiral_angle(y, frame, helix_offset_deg))


def depth_factor(y, frame, helix_offset_deg):
    return math.sin(spiral_angle(y, frame, helix_offset_deg))


def leading_y(frame):
    return [42, 30, 18, 6][frame]


def color_for_swirl(intensity, depth, peak=False):
    front = depth > 0.3
    side = -0.3 <= depth <= 0.3
    if peak and intensity > 0.85 and front:
        return WHITE
    if intensity >= 0.85:
        return WHITE if front else (HOT_YEL if side else GOLD)
    if intensity >= 0.6:
        return HOT_YEL if front else (GOLD if side else DIM_GOLD)
    if intensity >= 0.35:
        return GOLD if front else (DIM_GOLD if side else EDGE)
    if intensity >= 0.15:
        return DIM_GOLD if front or side else EDGE
    return EDGE


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
        # Color the spiral
        c = color_for_swirl(intensity, depth, peak=peak)
        put(px, ix, iy, c)
        # Widen the band when viewed side-on for chunkier look
        if abs(depth) < 0.6 and intensity > 0.3:
            c2 = color_for_swirl(intensity * 0.7, depth, peak=peak)
            put(px, ix + 1, iy, c2)


def draw_lead_burst(px, frame, helix_offset_deg, scale=1.0):
    """Hot flash at the leading edge of each helix."""
    lead = leading_y(frame)
    sx = spiral_x(lead, frame, helix_offset_deg)
    ix, iy = int(round(sx)), int(round(lead))
    cells = [(0, 0)] + ([(-1, 0), (1, 0), (0, -1), (0, 1)] if scale >= 1.0 else [])
    for dx, dy in cells:
        put(px, ix + dx, iy + dy, WHITE)
    if scale >= 1.0:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2),
                       (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            put(px, ix + dx, iy + dy, HOT_YEL)


def draw_sparks(px, frame):
    sets = {
        0: [(20, 44, SPARK), (28, 46, GOLD)],
        1: [(16, 36, SPARK), (32, 34, SPARK), (22, 40, DIM_GOLD)],
        2: [(14, 22, SPARK), (34, 24, SPARK), (20, 28, GOLD), (28, 30, GOLD)],
        3: [(18, 12, SPARK), (30, 14, GOLD), (24, 8, ARC),
            (12, 18, DIM_GOLD), (36, 20, DIM_GOLD)],
    }
    for x, y, c in sets[frame]:
        put(px, x, y, c)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Triple helix — 3 offsets at 120° apart
    for i in range(NUM_HELICES):
        offset = i * (360 / NUM_HELICES)
        draw_helix(px, frame, offset)
    # Lead bursts on the primary helix only (cleaner read)
    draw_lead_burst(px, frame, 0)
    # Smaller hints for the other two helices
    draw_lead_burst(px, frame, 120, scale=0.5)
    draw_lead_burst(px, frame, 240, scale=0.5)
    draw_sparks(px, frame)
    return img



if __name__ == "__main__":

    base = "/home/sparky/ogrs/art/projectiles/debuff_stun/impact_swirl"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
