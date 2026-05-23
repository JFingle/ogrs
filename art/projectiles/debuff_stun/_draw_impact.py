#!/usr/bin/env python3
"""
STUN impact effect — 48×48, 4 frames.
White-hot shock at impact point grows into a full lightning cage that
wraps the target. Peak frame: 8 thick lightning forks reaching the
canvas edge, target silhouette visible inside the electric cage.
"""
import os, math
from PIL import Image

W = H = 48
CX, CY = 24, 24
TRANS = (0, 0, 0, 0)

WHITE     = (255, 255, 255, 255)
HOT_YEL   = (255, 255, 160, 255)
GOLD      = (240, 192,   0, 255)
DIM_GOLD  = (176, 128,   0, 255)
EDGE      = ( 96,  70,   8, 255)
ARC       = (255, 220, 100, 255)
SPARK     = (255, 240, 180, 255)


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


def draw_burst(px, radius, peak=False):
    """Central explosion — filled disk with white-hot core."""
    for x in range(W):
        for y in range(H):
            d2 = (x - CX) ** 2 + (y - CY) ** 2
            if d2 <= 1:
                put(px, x, y, WHITE)
            elif d2 <= 4:
                put(px, x, y, WHITE if peak else HOT_YEL)
            elif d2 <= radius:
                put(px, x, y, HOT_YEL if peak else GOLD)
            elif d2 <= radius + 6:
                put(px, x, y, GOLD)
            elif d2 <= radius + 12:
                put(px, x, y, DIM_GOLD)


def fork_paths(reach, jitter=0):
    """8 fork paths — 4 cardinal + 4 diagonal, each with 2-3 kinks."""
    # Returns list of waypoint lists (each waypoint is (dx, dy) from center).
    forks = []
    for i in range(8):
        base_angle = i * 45  # 0, 45, 90, ... 315
        # Each fork is a series of waypoints walking outward
        path = []
        for step in range(3):
            r = reach * (step + 1) / 3
            wobble = (jitter if step % 2 == 0 else -jitter)
            ang = math.radians(base_angle + wobble * 8)
            dx = math.cos(ang) * r
            dy = math.sin(ang) * r
            # Add a slight tangential offset for jagged feel
            tang_ang = math.radians(base_angle + 90)
            offset = (5 if step == 1 else 0) * (1 if i % 2 == 0 else -1) * 0.5
            dx += math.cos(tang_ang) * offset
            dy += math.sin(tang_ang) * offset
            path.append((int(round(dx)), int(round(dy))))
        forks.append(path)
    return forks


def draw_fork(px, waypoints, thick=True, peak=False):
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
        if t < 0.2:
            c = WHITE if peak else HOT_YEL
        elif t < 0.5:
            c = HOT_YEL
        elif t < 0.8:
            c = GOLD
        else:
            c = DIM_GOLD
        put(px, x, y, c)
        if thick:
            shoulder_color = GOLD if t < 0.5 else DIM_GOLD
            put(px, x + 1, y, shoulder_color)
            put(px, x, y + 1, shoulder_color)


def draw_sparks(px, frame):
    """Stray electric sparks for late frames."""
    if frame == 3:
        sparks = [(8, 18, SPARK), (40, 22, SPARK), (24, 6, SPARK),
                  (12, 36, GOLD), (38, 38, GOLD), (10, 8, GOLD),
                  (44, 12, DIM_GOLD), (4, 30, DIM_GOLD)]
        for x, y, c in sparks:
            put(px, x, y, c)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        # Just landed — small bright core, short tendrils
        draw_burst(px, radius=4, peak=False)
        for path in fork_paths(reach=10, jitter=0):
            draw_fork(px, path, thick=False, peak=False)
    elif frame == 1:
        # Expanding
        draw_burst(px, radius=12, peak=False)
        for path in fork_paths(reach=18, jitter=1):
            draw_fork(px, path, thick=True, peak=False)
    elif frame == 2:
        # PEAK — full cage
        draw_burst(px, radius=20, peak=True)
        for path in fork_paths(reach=24, jitter=0):
            draw_fork(px, path, thick=True, peak=True)
    elif frame == 3:
        # Fading
        draw_burst(px, radius=8, peak=False)
        for path in fork_paths(reach=14, jitter=-1):
            draw_fork(px, path, thick=False, peak=False)
        draw_sparks(px, frame)
    return img



if __name__ == "__main__":

    base = "/home/sparky/ogrs/art/projectiles/debuff_stun/impact"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
