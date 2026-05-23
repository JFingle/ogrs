#!/usr/bin/env python3
"""
4 retro buff spells (Thick Skin / Burst of Strength / Rock Skin / Camouflage).
All 30×30 4-frame. Self-buff feel — the energy applies to the caster's
body rather than flying at an enemy. Designed so the silhouette plus the
hue clearly communicates the buff type.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# ===========================================================
# THICK SKIN — brown stone shield outline
# ===========================================================
STONE_OUTLINE = ( 40,  28,  16, 255)
STONE_DEEP    = ( 78,  56,  32, 255)
STONE_BASE    = (118,  88,  52, 255)
STONE_HIGH    = (170, 130,  80, 255)
STONE_PEAK    = (215, 180, 130, 255)
SHIELD_GLINT  = (255, 240, 200, 255)

# 11×11 shield template — kite-shaped heater shield with iron rim
SHIELD_TEMPLATE = [
    "..OOOOOOO..",
    ".OBBBBBBBO.",
    "OBHHHBBBBBO",
    "OBHHBBDDBBO",
    "OBHBBBDDBBO",
    "OBBBBBDDBBO",
    "OBBBBDDDBBO",
    ".OBBBDDDBO.",
    "..OBBDDBO..",
    "...OBDBO...",
    "....OOO....",
]

SHIELD_COLOR_MAP = {
    'O': STONE_OUTLINE,
    'B': STONE_BASE,
    'D': STONE_DEEP,
    'H': STONE_HIGH,
    'P': STONE_PEAK,
}


def draw_shield(px, peak=False, glint=False):
    """Draw the shield centered on (CX, CY)."""
    template_h = len(SHIELD_TEMPLATE)
    template_w = max(len(row) for row in SHIELD_TEMPLATE)
    for ty, row in enumerate(SHIELD_TEMPLATE):
        for tx, ch in enumerate(row):
            if ch == '.': continue
            color = SHIELD_COLOR_MAP[ch]
            x = CX + tx - template_w // 2
            y = CY + ty - template_h // 2
            put(px, x, y, color)
    # Peak: brighten a center band
    if peak:
        put(px, CX, CY - 1, STONE_PEAK)
        put(px, CX + 1, CY - 1, STONE_PEAK)
        put(px, CX, CY, STONE_PEAK)
    if glint:
        put(px, CX + 1, CY - 2, SHIELD_GLINT)


def thick_skin_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        draw_shield(px)
    elif frame == 1:
        draw_shield(px, peak=False, glint=False)
        # Stone particles forming
        for x, y in [(6, 8), (22, 9), (6, 20), (22, 20)]:
            put(px, x, y, STONE_BASE)
    elif frame == 2:
        draw_shield(px, peak=True, glint=True)
        # Stone particles converging onto shield
        for x, y in [(8, 10), (20, 10), (8, 18), (20, 18), (14, 4), (14, 24)]:
            put(px, x, y, STONE_HIGH)
        for x, y in [(7, 9), (21, 9), (7, 19), (21, 19)]:
            put(px, x, y, STONE_DEEP)
    elif frame == 3:
        draw_shield(px)
        # Settling particles
        for x, y in [(8, 11), (20, 11)]:
            put(px, x, y, STONE_BASE)
    return img


# ===========================================================
# BURST OF STRENGTH — red clenched fist sparkle
# ===========================================================
FIST_OUTLINE = ( 80,   8,   8, 255)
FIST_DEEP    = (160,  30,  30, 255)
FIST_BASE    = (210,  60,  50, 255)
FIST_HIGH    = (240, 130, 100, 255)
FIST_PEAK    = (255, 200, 160, 255)
FIST_SPARK   = (255, 220, 100, 255)
FIST_AURA    = (255, 100,  60, 255)

# 11×11 fist — closed knuckles facing viewer, thumb wrapping at bottom
FIST_TEMPLATE = [
    "...OOOOO...",
    "..OHHHHHO..",
    ".OHHBHBHHO.",
    "OHBBHBHBBHO",
    "OHBHHBHHBHO",
    "OBBBBBBBBBO",
    "OBBDBBDBBBO",
    "OBBDBBDBBBO",
    ".OBBBBBBBO.",
    "..OOOBBOO..",
    "....OOO....",
]

FIST_COLOR_MAP = {
    'O': FIST_OUTLINE,
    'B': FIST_BASE,
    'D': FIST_DEEP,
    'H': FIST_HIGH,
}


def draw_fist(px, peak=False):
    th = len(FIST_TEMPLATE)
    tw = max(len(r) for r in FIST_TEMPLATE)
    for ty, row in enumerate(FIST_TEMPLATE):
        for tx, ch in enumerate(row):
            if ch == '.': continue
            color = FIST_COLOR_MAP[ch]
            x = CX + tx - tw // 2
            y = CY + ty - th // 2
            put(px, x, y, color)
    if peak:
        # Brighten knuckles
        put(px, CX - 1, CY - 1, FIST_PEAK)
        put(px, CX + 1, CY - 1, FIST_PEAK)


def burst_strength_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_fist(px, peak=(frame == 2))
    # Power lines / sparkles radiating out
    if frame >= 1:
        radii = {1: 8, 2: 10, 3: 9}
        offsets_deg = [30, 90, 150, 210, 270, 330]
        for ang_deg in offsets_deg:
            ang = math.radians(ang_deg + frame * 10)
            r = radii[frame]
            x = CX + int(round(math.cos(ang) * r))
            y = CY + int(round(math.sin(ang) * r))
            color = FIST_SPARK if frame == 2 else FIST_AURA
            put(px, x, y, color)
        if frame == 2:
            # peak — extra sparkles further out
            for ang_deg in [0, 60, 120, 180, 240, 300]:
                ang = math.radians(ang_deg + 15)
                r = 13
                x = CX + int(round(math.cos(ang) * r))
                y = CY + int(round(math.sin(ang) * r))
                put(px, x, y, FIST_SPARK)
    return img


# ===========================================================
# ROCK SKIN — grey stone armor wrap
# ===========================================================
ROCK_OUTLINE = ( 30,  30,  35, 255)
ROCK_DEEP    = ( 70,  72,  80, 255)
ROCK_BASE    = (115, 118, 128, 255)
ROCK_HIGH    = (170, 175, 188, 255)
ROCK_PEAK    = (225, 230, 240, 255)


def rock_skin_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Spiraling stone-chunk band around a central core
    # Core: 5×5 stone sphere
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                put(px, x, y, ROCK_PEAK if frame == 2 else ROCK_HIGH)
            elif d2 <= 4:
                put(px, x, y, ROCK_HIGH)
            elif d2 <= 9:
                put(px, x, y, ROCK_BASE)
            elif d2 <= 16:
                put(px, x, y, ROCK_DEEP)
            elif d2 <= 25:
                put(px, x, y, ROCK_OUTLINE)
    # Orbiting rock chunks (3 chunks at varying angles)
    chunks = 5 if frame == 2 else 3
    radius = [8, 10, 12, 10][frame]
    offset = frame * 30
    for i in range(chunks):
        ang = math.radians(i * (360 / chunks) + offset)
        bx = CX + int(round(math.cos(ang) * radius))
        by = CY + int(round(math.sin(ang) * radius))
        # 2×2 chunk
        put(px, bx, by, ROCK_BASE)
        put(px, bx + 1, by, ROCK_DEEP)
        put(px, bx, by + 1, ROCK_HIGH)
        put(px, bx + 1, by + 1, ROCK_OUTLINE)
    return img


# ===========================================================
# CAMOUFLAGE — faded green leaf cluster fading at edges
# ===========================================================
LEAF_DEEP   = ( 30,  60,  30, 255)
LEAF_BASE   = ( 70, 110,  50, 255)
LEAF_MID    = (110, 150,  70, 255)
LEAF_HIGH   = (160, 195, 100, 255)
LEAF_FADE   = (110, 150,  70, 100)  # half-alpha for fading edges
LEAF_PALE   = (200, 220, 150, 255)


def camo_leaf(px, cx, cy, dx_dir, dy_dir, dim=False):
    """Single leaf — pointed teardrop with stem."""
    body_color = LEAF_BASE if dim else LEAF_MID
    edge_color = LEAF_DEEP
    bright = LEAF_HIGH
    # Body — 2×3 cluster
    put(px, cx, cy, body_color)
    put(px, cx + dx_dir, cy + dy_dir, body_color)
    put(px, cx + dx_dir * 2, cy + dy_dir * 2, bright)
    # Side cells perpendicular for width
    tx, ty = -dy_dir, dx_dir
    put(px, cx + tx, cy + ty, edge_color)
    put(px, cx + dx_dir + tx, cy + dy_dir + ty, body_color)
    put(px, cx - tx, cy - ty, edge_color)


def camo_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Cluster of 5-7 leaves arranged in a rough sphere
    leaf_positions_per_frame = {
        0: [(CX, CY-3, 0, -1), (CX-3, CY, -1, 0), (CX+3, CY, 1, 0)],
        1: [(CX, CY-4, 0, -1), (CX-4, CY+1, -1, 0), (CX+4, CY+1, 1, 0),
            (CX-2, CY+3, -1, 1), (CX+2, CY+3, 1, 1)],
        2: [(CX, CY-5, 0, -1), (CX-5, CY, -1, 0), (CX+5, CY, 1, 0),
            (CX-3, CY+4, -1, 1), (CX+3, CY+4, 1, 1),
            (CX-2, CY-3, -1, -1), (CX+2, CY-3, 1, -1)],
        3: [(CX, CY-3, 0, -1), (CX-3, CY+1, -1, 0), (CX+3, CY+1, 1, 0),
            (CX-1, CY+3, 0, 1)],
    }
    for cx, cy, dx, dy in leaf_positions_per_frame[frame]:
        camo_leaf(px, cx, cy, dx, dy, dim=(frame in (0, 3)))
    # Central glow at peak
    if frame == 2:
        put(px, CX, CY, LEAF_PALE)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            put(px, CX + dx, CY + dy, LEAF_HIGH)
    # Fading edge specks — dithered leaves at the boundary
    if frame == 2:
        for x, y in [(4, 14), (24, 14), (14, 4), (14, 24), (6, 6), (22, 22)]:
            put(px, x, y, LEAF_BASE)
    return img


# Driver
SPELLS = [
    ("buff_thick_skin",       thick_skin_frame),
    ("buff_burst_of_strength", burst_strength_frame),
    ("buff_rock_skin",        rock_skin_frame),
    ("buff_camouflage",       camo_frame),
]

if __name__ == "__main__":
    for folder, fn in SPELLS:
        out = f"/home/sparky/ogrs/art/projectiles/{folder}/frames"
        os.makedirs(out, exist_ok=True)
        for i in range(4):
            img = fn(i)
            img.save(f"{out}/frame_{i:02d}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/frame_{i:02d}_x8.png")
        print(f"done: {folder}")
