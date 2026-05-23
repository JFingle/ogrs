#!/usr/bin/env python3
"""
WEAKEN triple-helix swirl — 48×48, 4 frames.
*** GOES TOP-TO-BOTTOM *** unlike all other swirls — Weaken saps strength
DOWNWARD out of the target. Three olive ribbons start at the head and
travel down to the feet. Drip trails fall off the leading edges as the
swirl reaches the legs.
"""
import os, math
from PIL import Image

W = H = 48
CX = 24
TARGET_TOP, TARGET_BOTTOM = 6, 42
TARGET_H = TARGET_BOTTOM - TARGET_TOP

TRANS = (0, 0, 0, 0)
DEEP    = ( 74,  80,  40, 255)
BASE    = (107, 116,  56, 255)
MID     = (139, 144,  80, 255)
PALE    = (168, 176, 112, 255)
HIGH    = (192, 196, 144, 255)
DRIP_LO = ( 74,  80,  40, 255)

RADIUS      = 10
TURNS       = 2.4
TAIL_LENGTH = 16
NUM_HELICES = 3


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def spiral_angle(y, frame, off):
    """Spiral progresses from top to bottom (sap direction)."""
    progress = (y - TARGET_TOP) / TARGET_H   # 0 at top, 1 at bottom
    return progress * (TURNS * 2 * math.pi) + frame * (math.pi / 3) + math.radians(off)


def spiral_x(y, frame, off):
    return CX + RADIUS * math.cos(spiral_angle(y, frame, off))


def depth_factor(y, frame, off):
    return math.sin(spiral_angle(y, frame, off))


def leading_y(frame):
    """Leading edge starts at top (head) and travels down to bottom (feet)."""
    return [4, 16, 28, 40][frame]


def color_for_swirl(intensity, depth, peak=False):
    front = depth > 0.3
    side = -0.3 <= depth <= 0.3
    if peak and intensity > 0.85 and front:
        return HIGH
    if intensity >= 0.85:
        return HIGH if front else (PALE if side else MID)
    if intensity >= 0.6:
        return PALE if front else (MID if side else BASE)
    if intensity >= 0.35:
        return MID if front else (BASE if side else DEEP)
    if intensity >= 0.15:
        return BASE if front or side else DEEP
    return DEEP


def draw_helix(px, frame, off):
    """Swirl renders ABOVE the leading edge (the trail extends upward from current y)."""
    lead = leading_y(frame)
    tail = lead - TAIL_LENGTH   # tail is ABOVE leading edge
    peak = (frame == 2)
    for y4 in range((tail - 1) * 4, (lead + 1) * 4 + 1):
        y = y4 / 4.0
        if not (tail <= y <= lead):
            continue
        sx = spiral_x(y, frame, off)
        depth = depth_factor(y, frame, off)
        # Intensity: 1.0 at leading edge (bottom), fading to 0 at tail (top)
        intensity = (y - tail) / TAIL_LENGTH
        ix, iy = int(round(sx)), int(round(y))
        c = color_for_swirl(intensity, depth, peak=peak)
        put(px, ix, iy, c)
        if abs(depth) < 0.6 and intensity > 0.3:
            put(px, ix + 1, iy, color_for_swirl(intensity * 0.7, depth, peak=peak))


def draw_falling_drips(px, frame):
    """Drip drops falling off the leading edge as the swirl descends."""
    lead = leading_y(frame)
    if frame >= 1:
        for i in range(NUM_HELICES):
            off = i * (360 / NUM_HELICES)
            sx = spiral_x(lead, frame, off)
            ix = int(round(sx))
            # 2-3 drip pixels falling below the leading edge
            for step in range(1, 4):
                put(px, ix, lead + step, DRIP_LO if step < 3 else DEEP)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    for i in range(NUM_HELICES):
        draw_helix(px, frame, i * (360 / NUM_HELICES))
    draw_falling_drips(px, frame)
    return img


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/debuff_weaken/impact_swirl"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
