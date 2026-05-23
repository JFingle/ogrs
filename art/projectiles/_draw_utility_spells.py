#!/usr/bin/env python3
"""
Utility spells — 7 sprites, 30×30 4-frame each.
Each is distinct: literal-icon style (banana, loaf, coin, hand) since
the spell purpose is informational, not combat. Player should know what
they cast at a glance.
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
# LOW ALCHEMY — single gold coin with sparkle
# ===========================================================
COIN_DEEP   = (120,  76,   8, 255)
COIN_BASE   = (200, 150,  40, 255)
COIN_HIGH   = (255, 220, 100, 255)
COIN_PEAK   = (255, 245, 200, 255)
SPARKLE_W   = (255, 255, 255, 255)


def draw_coin(px, cx, cy, peak=False):
    """Round-ish coin centered at (cx, cy), 7×7 with simple shading."""
    cells = {
        (-3, -1): COIN_DEEP, (-3, 0): COIN_DEEP, (-3, 1): COIN_DEEP,
        (-2, -2): COIN_DEEP, (-2, -1): COIN_HIGH, (-2, 0): COIN_HIGH, (-2, 1): COIN_BASE, (-2, 2): COIN_DEEP,
        (-1, -3): COIN_DEEP, (-1, -2): COIN_PEAK if peak else COIN_HIGH,
        (-1, -1): COIN_HIGH, (-1, 0): COIN_HIGH, (-1, 1): COIN_BASE, (-1, 2): COIN_BASE, (-1, 3): COIN_DEEP,
        (0, -3): COIN_DEEP, (0, -2): COIN_HIGH, (0, -1): COIN_HIGH, (0, 0): COIN_HIGH, (0, 1): COIN_BASE, (0, 2): COIN_DEEP, (0, 3): COIN_DEEP,
        (1, -3): COIN_DEEP, (1, -2): COIN_HIGH, (1, -1): COIN_HIGH, (1, 0): COIN_BASE, (1, 1): COIN_BASE, (1, 2): COIN_DEEP, (1, 3): COIN_DEEP,
        (2, -2): COIN_DEEP, (2, -1): COIN_BASE, (2, 0): COIN_BASE, (2, 1): COIN_DEEP, (2, 2): COIN_DEEP,
        (3, -1): COIN_DEEP, (3, 0): COIN_DEEP, (3, 1): COIN_DEEP,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def low_alch_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_coin(px, CX, CY, peak=(frame == 2))
    # Sparkle stars at varying positions
    sparkles_by_frame = {
        0: [(20, 8)],
        1: [(20, 8), (8, 20)],
        2: [(20, 7), (8, 20), (22, 22), (6, 8), (14, 4)],  # PEAK — most sparkles
        3: [(21, 9), (9, 21)],
    }
    for x, y in sparkles_by_frame[frame]:
        # 5-pixel star sparkle
        put(px, x, y, SPARKLE_W)
        put(px, x - 1, y, COIN_PEAK)
        put(px, x + 1, y, COIN_PEAK)
        put(px, x, y - 1, COIN_PEAK)
        put(px, x, y + 1, COIN_PEAK)
    return img


# ===========================================================
# HIGH ALCHEMY — 3 gold coins, brighter
# ===========================================================
def high_alch_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # 3 coins arranged in a triangle, peak frame all bright
    coins = [
        (CX - 5, CY - 3),    # left
        (CX + 5, CY - 3),    # right
        (CX, CY + 4),         # bottom
    ]
    for cx, cy in coins:
        draw_coin(px, cx, cy, peak=(frame == 2))
    # Many sparkles
    sparkles_by_frame = {
        0: [(20, 8), (8, 8), (14, 22)],
        1: [(22, 6), (6, 6), (14, 24), (3, 14), (25, 14)],
        2: [(22, 5), (6, 5), (14, 25), (2, 14), (26, 14),
            (8, 18), (20, 18), (14, 2), (14, 14)],
        3: [(21, 7), (7, 7), (14, 23), (4, 14), (24, 14)],
    }
    for x, y in sparkles_by_frame[frame]:
        put(px, x, y, SPARKLE_W)
        put(px, x - 1, y, COIN_PEAK)
        put(px, x + 1, y, COIN_PEAK)
    return img


# ===========================================================
# TELEKINETIC GRAB — translucent reaching hand
# ===========================================================
HAND_OUTLINE = ( 30,  40,  60, 255)
HAND_DEEP    = ( 70,  90, 130, 255)
HAND_BASE    = (120, 150, 200, 255)
HAND_HIGH    = (180, 210, 240, 255)
HAND_PEAK    = (240, 248, 255, 255)
HAND_AURA    = (200, 220, 255, 255)

# 11×9 hand (palm + 4 fingers extended, thumb folded)
HAND_TEMPLATE = [
    ".OOO.OOO..",
    "OBBOOBBO..",
    "OBHOOBHO..",
    "OBHOOBHO..",
    "OBBOOBBO..",
    "OBBHHHBBO.",
    "OBBBHBBBOO",
    ".OBBBBBBBO",
    "..OOOOOOO.",
]

HAND_COLOR_MAP = {
    'O': HAND_OUTLINE,
    'B': HAND_BASE,
    'H': HAND_HIGH,
    'D': HAND_DEEP,
}


def draw_hand(px, peak=False):
    th = len(HAND_TEMPLATE)
    tw = max(len(r) for r in HAND_TEMPLATE)
    for ty, row in enumerate(HAND_TEMPLATE):
        for tx, ch in enumerate(row):
            if ch == '.': continue
            color = HAND_COLOR_MAP[ch]
            if peak and color == HAND_HIGH:
                color = HAND_PEAK
            x = CX + tx - tw // 2
            y = CY + ty - th // 2
            put(px, x, y, color)


def telegrab_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_hand(px, peak=(frame == 2))
    # Aura specs reaching outward — fingers extending
    aura_positions = {
        0: [(6, 6), (9, 5), (12, 4)],
        1: [(5, 5), (8, 4), (11, 3), (14, 3)],
        2: [(4, 4), (7, 3), (10, 2), (13, 2), (16, 3), (3, 7), (3, 10)],
        3: [(5, 5), (8, 4), (11, 3)],
    }
    for x, y in aura_positions[frame]:
        put(px, x, y, HAND_AURA)
    return img


# ===========================================================
# BONES TO BANANAS — yellow banana glyph
# ===========================================================
BAN_DEEP    = (140, 100,  20, 255)
BAN_BASE    = (220, 180,  50, 255)
BAN_HIGH    = (255, 230,  80, 255)
BAN_PEAK    = (255, 250, 180, 255)
BAN_TIP     = (100,  70,  20, 255)

# Banana curve — defined as crescent shape, 11×9
BANANA_TEMPLATE = [
    "..OO.......",
    ".OBBO......",
    ".OBHO......",
    "..OBBO.....",
    "...OBBO....",
    "....OBBO...",
    ".....OBBO..",
    "......OBBO.",
    ".......OO..",
]
BAN_COLOR_MAP = {'O': BAN_DEEP, 'B': BAN_BASE, 'H': BAN_HIGH}


def draw_banana(px, peak=False):
    th = len(BANANA_TEMPLATE)
    tw = max(len(r) for r in BANANA_TEMPLATE)
    for ty, row in enumerate(BANANA_TEMPLATE):
        for tx, ch in enumerate(row):
            if ch == '.': continue
            color = BAN_COLOR_MAP[ch]
            if peak and color == BAN_HIGH:
                color = BAN_PEAK
            x = CX + tx - tw // 2
            y = CY + ty - th // 2
            put(px, x, y, color)
    # Tips at both ends
    put(px, CX - tw // 2 + 2, CY - th // 2 + 0, BAN_TIP)


def bones_bananas_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_banana(px, peak=(frame == 2))
    # Some yellow specks orbiting (transformation effect)
    radii = [6, 8, 10, 8]
    count = [3, 4, 6, 4][frame]
    offset = frame * 25
    r = radii[frame]
    for i in range(count):
        ang = math.radians(i * (360 / count) + offset)
        x = CX + int(round(math.cos(ang) * r))
        y = CY + int(round(math.sin(ang) * r))
        put(px, x, y, BAN_BASE if frame == 2 else BAN_DEEP)
    return img


# ===========================================================
# BONES TO BREAD — brown loaf glyph
# ===========================================================
BREAD_DEEP   = ( 90,  50,  20, 255)
BREAD_BASE   = (170, 110,  60, 255)
BREAD_HIGH   = (220, 170, 110, 255)
BREAD_CRUMB  = (240, 200, 140, 255)

LOAF_TEMPLATE = [
    "...OOOOOOO.....",
    "..OBBHHHHBO....",
    ".OBHHCCCHHBO...",
    ".OBHHCCCCHBBO..",
    "..OBBHHHHBBBO..",
    "...OOOOOOOOO...",
]
LOAF_COLORS = {'O': BREAD_DEEP, 'B': BREAD_BASE, 'H': BREAD_HIGH, 'C': BREAD_CRUMB}


def draw_loaf(px, peak=False):
    th = len(LOAF_TEMPLATE)
    tw = max(len(r) for r in LOAF_TEMPLATE)
    for ty, row in enumerate(LOAF_TEMPLATE):
        for tx, ch in enumerate(row):
            if ch == '.': continue
            color = LOAF_COLORS[ch]
            if peak and color == BREAD_CRUMB:
                color = (255, 230, 180, 255)
            x = CX + tx - tw // 2
            y = CY + ty - th // 2
            put(px, x, y, color)


def bones_bread_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_loaf(px, peak=(frame == 2))
    # Bread crumbs falling
    crumbs_by_frame = {
        0: [(8, 8), (22, 9)],
        1: [(7, 6), (23, 8), (15, 4)],
        2: [(6, 5), (24, 7), (15, 3), (10, 22), (20, 22)],
        3: [(8, 7), (22, 9)],
    }
    for x, y in crumbs_by_frame[frame]:
        put(px, x, y, BREAD_BASE)
        put(px, x + 1, y, BREAD_DEEP)
    return img


# ===========================================================
# SUPERHEAT ITEM — orange ore-melt drip
# ===========================================================
HEAT_DEEP   = ( 80,  20,   8, 255)
HEAT_BASE   = (180,  60,  20, 255)
HEAT_HOT    = (255, 140,  40, 255)
HEAT_PEAK   = (255, 230, 140, 255)
HEAT_WHITE  = (255, 255, 220, 255)
ORE_GREY    = (100, 100, 110, 255)


def superheat_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Ore lump being melted — grey rock above, hot drip below
    # Top: grey ore (shrinks per frame as it melts)
    ore_y_top = [10, 11, 12, 13][frame]
    ore_h = [6, 5, 4, 3][frame]
    for x in range(CX - 4, CX + 5):
        for y in range(ore_y_top, ore_y_top + ore_h):
            d_from_center = abs(x - CX)
            if d_from_center <= 4 - (y - ore_y_top) // 2:
                put(px, x, y, ORE_GREY)
    # Melting glow at the bottom of ore
    glow_y = ore_y_top + ore_h
    for x in range(CX - 3, CX + 4):
        put(px, x, glow_y, HEAT_HOT)
        put(px, x, glow_y + 1, HEAT_BASE)
    # Hot drips falling
    drip_count = [1, 2, 3, 4][frame]
    for i in range(drip_count):
        dx = (i - 1) * 2
        dy = (i + 1) * 2
        x = CX + dx
        y = glow_y + 2 + dy
        if frame == 2 and i == drip_count - 1:
            color = HEAT_WHITE
        else:
            color = HEAT_HOT if i < drip_count - 1 else HEAT_BASE
        put(px, x, y, color)
        put(px, x, y + 1, HEAT_DEEP)
    # Peak — extra heat aura around ore
    if frame == 2:
        for ang_deg in range(0, 360, 60):
            ang = math.radians(ang_deg)
            r = 7
            x = CX + int(round(math.cos(ang) * r))
            y = CY - 2 + int(round(math.sin(ang) * r))
            put(px, x, y, HEAT_HOT)
    return img


# ===========================================================
# CHARGE — lavender energy pulse (preps god magic)
# ===========================================================
CHARGE_DEEP  = ( 50,  30, 100, 255)
CHARGE_BASE  = (120,  80, 180, 255)
CHARGE_HIGH  = (200, 160, 240, 255)
CHARGE_PEAK  = (240, 220, 255, 255)
CHARGE_AURA  = (180, 140, 230, 255)


def charge_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Pulsing lavender orb that grows then contracts
    radii = [3, 5, 7, 5]
    r = radii[frame]
    r2 = r * r
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                put(px, x, y, CHARGE_PEAK if frame == 2 else CHARGE_HIGH)
            elif d2 <= 4:
                put(px, x, y, CHARGE_HIGH)
            elif d2 <= r2:
                put(px, x, y, CHARGE_BASE)
            elif d2 <= r2 + 8:
                put(px, x, y, CHARGE_DEEP)
    # Energy beams rising upward
    beams_by_frame = {
        0: [(14, 8), (14, 6)],
        1: [(14, 6), (14, 4), (12, 7), (16, 7)],
        2: [(14, 4), (14, 2), (12, 5), (16, 5), (10, 7), (18, 7)],
        3: [(14, 6), (14, 4), (12, 6)],
    }
    for x, y in beams_by_frame[frame]:
        put(px, x, y, CHARGE_AURA)
    # Vertical pulse line at peak
    if frame == 2:
        for y in range(0, 28):
            if y % 2 == 0:
                put(px, CX, y, CHARGE_HIGH)
    return img


# ===========================================================
# Driver
# ===========================================================
SPELLS = [
    ("util_low_alch",        low_alch_frame),
    ("util_high_alch",       high_alch_frame),
    ("util_telegrab",        telegrab_frame),
    ("util_bones_to_bananas", bones_bananas_frame),
    ("util_bones_to_bread",  bones_bread_frame),
    ("util_superheat",       superheat_frame),
    ("util_charge",          charge_frame),
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
