#!/usr/bin/env python3
"""
STUN debuff projectile (v2 — spicier).
8 lightning bolts (4 cardinal main + 4 diagonal secondary), thicker
with 1-px white-hot cores, a bigger central white burst, and an outer
shock ring of yellow specks. Per-frame strobe for electric flicker.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)

WHITE     = (255, 255, 255, 255)
HOT_YEL   = (255, 255, 160, 255)
GOLD      = (240, 192,   0, 255)
DIM_GOLD  = (176, 128,   0, 255)
EDGE      = ( 96,  70,   8, 255)
ARC       = (255, 220, 100, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def bresenham(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    x, y = x0, y0
    while True:
        pts.append((x, y))
        if x == x1 and y == y1: break
        e2 = 2 * err
        if e2 > -dy: err -= dy; x += sx
        if e2 <  dx: err += dx; y += sy
    return pts


def main_bolts(jitter=0):
    """4 long cardinal bolts going N/E/S/W with kinks."""
    return [
        # North
        [(0, -3), (1 + jitter, -6), (-1, -9), (1, -12), (-1, -14)],
        # East
        [(3, 0), (6, 1 - jitter), (9, -1), (12, 1), (14, -1)],
        # South
        [(0, 3), (-1 + jitter, 6), (1, 9), (-1, 12), (1, 14)],
        # West
        [(-3, 0), (-6, -1 + jitter), (-9, 1), (-12, -1), (-14, 1)],
    ]


def diagonal_bolts(jitter=0):
    """4 shorter diagonal bolts (NE/SE/SW/NW)."""
    return [
        # NE
        [(3, -3), (5, -5 + jitter), (8, -7), (10, -10)],
        # SE
        [(3, 3), (5 - jitter, 5), (7, 8), (10, 10)],
        # SW
        [(-3, 3), (-5, 5 + jitter), (-8, 7), (-10, 10)],
        # NW
        [(-3, -3), (-5 + jitter, -5), (-7, -8), (-10, -10)],
    ]


def draw_bolt(px, waypoints, thick=False, peak=False):
    """Walk waypoints connecting with bresenham; color by distance from origin."""
    pixels = []
    last = (CX, CY)
    for dx, dy in waypoints:
        nx, ny = CX + dx, CY + dy
        pixels.extend(bresenham(last[0], last[1], nx, ny))
        last = (nx, ny)
    seen = set()
    pixels = [p for p in pixels if not (p in seen or seen.add(p))]
    n = len(pixels)
    for i, (x, y) in enumerate(pixels):
        t = i / max(1, n - 1)
        if t < 0.15:
            c = WHITE if peak else HOT_YEL
        elif t < 0.4:
            c = HOT_YEL
        elif t < 0.7:
            c = GOLD
        elif t < 0.9:
            c = DIM_GOLD
        else:
            c = EDGE
        put(px, x, y, c)
        if thick:
            # 1-px shoulder
            put(px, x + 1, y, GOLD if t < 0.5 else DIM_GOLD)
            put(px, x, y + 1, GOLD if t < 0.5 else DIM_GOLD)


def draw_burst_core(px, peak=False):
    """Bigger central burst — a 5×5 white explosion with yellow halo."""
    core_cells = {
        (0, 0): WHITE,
        (-1, 0): HOT_YEL, (1, 0): HOT_YEL,
        (0, -1): HOT_YEL, (0, 1): HOT_YEL,
        (-2, 0): GOLD, (2, 0): GOLD,
        (0, -2): GOLD, (0, 2): GOLD,
        (-1, -1): HOT_YEL, (1, -1): HOT_YEL,
        (-1, 1): HOT_YEL, (1, 1): HOT_YEL,
    }
    if peak:
        # Extend to 7×7 with white cross
        core_cells[(-3, 0)] = DIM_GOLD
        core_cells[(3, 0)] = DIM_GOLD
        core_cells[(0, -3)] = DIM_GOLD
        core_cells[(0, 3)] = DIM_GOLD
        # Crosshair white at center
        core_cells[(0, 0)] = WHITE
        core_cells[(-1, 0)] = WHITE
        core_cells[(1, 0)] = WHITE
        core_cells[(0, -1)] = WHITE
        core_cells[(0, 1)] = WHITE
    for (dx, dy), c in core_cells.items():
        put(px, CX + dx, CY + dy, c)


def draw_shock_ring(px, frame):
    """Outer ring of arcing specks orbiting at radius ~13."""
    base_angles = [0, 45, 90, 135, 180, 225, 270, 315]
    offset = frame * 18
    for ang_deg in base_angles:
        ang = math.radians(ang_deg + offset)
        r = 13
        x = CX + int(round(math.cos(ang) * r))
        y = CY + int(round(math.sin(ang) * r))
        put(px, x, y, ARC if frame in (1, 2) else DIM_GOLD)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    jitter = [0, 1, 0, -1][frame]
    # Outer shock ring (only on bright/peak frames)
    draw_shock_ring(px, frame)
    # Diagonal secondary bolts (always drawn, vary thickness with frame)
    for wp in diagonal_bolts(jitter):
        draw_bolt(px, wp, thick=(frame in (1, 2)), peak=(frame == 2))
    # Main cardinal bolts
    for wp in main_bolts(jitter):
        draw_bolt(px, wp, thick=(frame in (1, 2)), peak=(frame == 2))
    # Central burst core (on top of bolts)
    draw_burst_core(px, peak=(frame == 2))
    return img


base = "/home/sparky/ogrs/art/projectiles/debuff_stun/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
print("done")
