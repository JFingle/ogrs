#!/usr/bin/env python3
"""
4 special bolts — Chill / Shock / Elemental / Iban.
Each 30×30, 4 frames. Distinct silhouettes so they read as different bolt
types in flight.

- CHILL  : frozen arrow shape with ice crystals + cold mist trail
- SHOCK  : yellow lightning zigzag (vertical, vs Stun's radial burst)
- ELEMENTAL: multi-hue swirling orb (rainbow cycling per frame)
- IBAN   : crimson chaos blast with dark rune flicker
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)


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


# ===========================================================
# CHILL BOLT — frozen arrow with mist trail
# ===========================================================
ICE_WHITE = (240, 250, 255, 255)
ICE_BASE  = (168, 222, 255, 255)
ICE_MID   = (108, 162, 210, 255)
ICE_DEEP  = ( 58, 100, 140, 255)
ICE_EDGE  = ( 28,  56,  90, 255)
MIST_PALE = (200, 220, 240, 255)


def chill_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Diagonal "arrow" of ice — tail lower-left, tip upper-right
    tail = (6, 23)
    tip  = (22, 7)
    line = bresenham(*tail, *tip)
    # Main shaft of pale ice
    body = line[2:-2]
    for x, y in body:
        put(px, x, y, ICE_MID)
        put(px, x - 1, y + 1, ICE_DEEP)  # underside shadow
        put(px, x + 1, y - 1, ICE_WHITE) # upperside highlight
    # Tip = ice crystal (4-pixel diamond)
    cells = [(0,0), (1,0), (0,1), (-1,0), (0,-1), (1,-1), (1,1)]
    colors = [ICE_WHITE, ICE_BASE, ICE_BASE, ICE_MID, ICE_BASE, ICE_BASE, ICE_DEEP]
    for (dx, dy), c in zip(cells, colors):
        put(px, tip[0] + dx, tip[1] + dy, c)
    # Tail = frozen fletching (frost cluster)
    for (dx, dy), c in [((0,0), ICE_DEEP), ((-1,0), ICE_MID), ((0,1), ICE_MID),
                        ((1,0), ICE_BASE), ((-1,1), ICE_BASE), ((1,1), ICE_DEEP)]:
        put(px, tail[0] + dx, tail[1] + dy, c)
    # Cold mist trail behind the tail
    mist = {
        0: [(4, 25), (3, 27)],
        1: [(4, 25), (3, 27), (5, 26)],
        2: [(3, 25), (2, 27), (5, 26), (4, 28)],   # peak — biggest trail
        3: [(4, 26), (3, 27)],
    }
    for x, y in mist[frame]:
        put(px, x, y, MIST_PALE)
    # Tiny ice flakes drifting off the shaft (frame 2 only — peak chill)
    if frame == 2:
        for x, y in [(16, 14), (12, 18), (18, 11)]:
            put(px, x, y, ICE_WHITE)
    return img


# ===========================================================
# SHOCK BOLT — vertical lightning zigzag
# ===========================================================
LIGHT_WHITE = (255, 255, 255, 255)
LIGHT_HOT   = (255, 255, 160, 255)
LIGHT_GOLD  = (240, 192,   0, 255)
LIGHT_DIM   = (176, 128,   0, 255)
LIGHT_DARK  = ( 96,  70,   8, 255)


def shock_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Vertical zigzag bolt — 6 segments
    # Slight per-frame x-shift for flicker
    shift = [0, 1, 0, -1][frame]
    waypoints = [
        (CX + 0 + shift, 4),
        (CX + 2 + shift, 8),
        (CX - 1 + shift, 12),
        (CX + 2 + shift, 16),
        (CX - 1 + shift, 20),
        (CX + 1 + shift, 24),
    ]
    pixels = []
    for i in range(len(waypoints) - 1):
        pixels.extend(bresenham(*waypoints[i], *waypoints[i + 1]))
    seen = set()
    pixels = [p for p in pixels if not (p in seen or seen.add(p))]
    n = len(pixels)
    for i, (x, y) in enumerate(pixels):
        t = i / max(1, n - 1)
        if t < 0.15:
            c = LIGHT_WHITE
        elif t < 0.4:
            c = LIGHT_HOT
        elif t < 0.7:
            c = LIGHT_GOLD
        else:
            c = LIGHT_DIM
        put(px, x, y, c)
        # 1-px shoulder for thickness
        put(px, x + 1, y, c if t < 0.5 else LIGHT_DARK)
    # Bright sparks at the head and tail
    put(px, waypoints[0][0], waypoints[0][1] - 1, LIGHT_WHITE)
    if frame == 2:
        # Peak — branching micro-bolts off the main
        for x, y in [(11, 14), (18, 13), (10, 19), (19, 22)]:
            put(px, x, y, LIGHT_HOT)
        for x, y in [(10, 14), (19, 13)]:
            put(px, x, y, LIGHT_GOLD)
    return img


# ===========================================================
# ELEMENTAL BOLT — rainbow swirling orb
# ===========================================================
EL_COLORS = [
    (255, 100, 100, 255),  # red
    (255, 200,  80, 255),  # orange
    (255, 255, 120, 255),  # yellow
    (130, 230, 130, 255),  # green
    (130, 200, 255, 255),  # blue
    (200, 130, 255, 255),  # violet
]


def elemental_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Core orb — color cycles with frame
    primary = EL_COLORS[frame % len(EL_COLORS)]
    secondary = EL_COLORS[(frame + 2) % len(EL_COLORS)]
    tertiary = EL_COLORS[(frame + 4) % len(EL_COLORS)]
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                put(px, x, y, (255, 255, 255, 255))
            elif d2 <= 4:
                put(px, x, y, primary)
            elif d2 <= 10:
                put(px, x, y, secondary)
            elif d2 <= 16:
                put(px, x, y, tertiary)
            elif d2 <= 25:
                # Outer halo — dither all 3 colors
                if (x + y) % 3 == 0:
                    put(px, x, y, primary)
                elif (x + y) % 3 == 1:
                    put(px, x, y, secondary)
                else:
                    put(px, x, y, tertiary)
    # 3 rotating streaks each in its own hue
    for i, color in enumerate([primary, secondary, tertiary]):
        ang = math.radians(i * 120 + frame * 30)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        for step in range(7, 12):
            x = CX + int(round(cos_a * step))
            y = CY + int(round(sin_a * step))
            put(px, x, y, color)
    return img


# ===========================================================
# IBAN BLAST — crimson chaos with rune flicker
# ===========================================================
IBAN_HOT    = (255, 200,  80, 255)
IBAN_FLAME  = (255, 100,  40, 255)
IBAN_BASE   = (200,  40,  40, 255)
IBAN_DEEP   = (130,  10,  10, 255)
IBAN_RUNE   = ( 50,   0,  10, 255)
IBAN_DARK   = ( 25,   0,   5, 255)


def iban_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Core flame body — irregular circle with dark rune patterns
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                put(px, x, y, IBAN_HOT)
            elif d2 <= 4:
                put(px, x, y, IBAN_FLAME)
            elif d2 <= 16:
                put(px, x, y, IBAN_BASE)
            elif d2 <= 30:
                put(px, x, y, IBAN_DEEP)
            elif d2 <= 36:
                if (x + y) % 2 == 0:
                    put(px, x, y, IBAN_DARK)
    # Dark rune flecks inside the flame — different positions per frame
    runes_by_frame = {
        0: [(11, 11), (17, 16), (13, 17)],
        1: [(12, 12), (16, 15), (14, 18), (11, 16)],
        2: [(10, 13), (18, 13), (12, 17), (16, 17), (14, 10), (14, 19)],  # peak — 6 runes
        3: [(13, 12), (15, 15), (12, 17)],
    }
    for x, y in runes_by_frame[frame]:
        put(px, x, y, IBAN_RUNE)
    # Flame-tongues licking outward (4 directions)
    if frame >= 1:
        offsets = [(0, -7), (7, 0), (0, 7), (-7, 0)]
        for ox, oy in offsets:
            put(px, CX + ox, CY + oy, IBAN_FLAME)
            put(px, CX + ox // 2, CY + oy // 2, IBAN_HOT)
    if frame == 2:
        # Peak — corner flame sparks
        for ox, oy in [(-5, -5), (5, -5), (-5, 5), (5, 5)]:
            put(px, CX + ox, CY + oy, IBAN_FLAME)
    return img


# ===========================================================
# Driver
# ===========================================================
SPELLS = [
    ("bolt_chill",      chill_frame),
    ("bolt_shock",      shock_frame),
    ("bolt_elemental",  elemental_frame),
    ("bolt_iban",       iban_frame),
]

if __name__ == "__main__":
    for folder, frame_fn in SPELLS:
        out = f"/home/sparky/ogrs/art/projectiles/{folder}/frames"
        os.makedirs(out, exist_ok=True)
        for i in range(4):
            img = frame_fn(i)
            img.save(f"{out}/frame_{i:02d}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/frame_{i:02d}_x8.png")
        print(f"done: {folder}")
