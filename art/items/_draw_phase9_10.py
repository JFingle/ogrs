#!/usr/bin/env python3
"""
Phase 9 — Sacred Galilee crops + Tier-7 dishes (11 sprites)
Phase 10 — Tier-6 Legendary feasts (4 dishes)

Total 15 sprites at 32×32.

Phase 9 sacred ingredients use a subtle GOLDEN GLOW halo to mark them as
holy/blessed. Phase 10 feasts are multi-component plates that look RICH.
"""
import os, math
from PIL import Image

W = H = 32
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def stamp(px, ox, oy, rows, cm):
    for ty, row in enumerate(rows):
        for tx, ch in enumerate(row):
            if ch == '.':
                continue
            put(px, ox + tx, oy + ty, cm.get(ch))


HOLY_GLOW = (255, 240, 180, 100)


def add_holy_glow(px, cx=16, cy=16, inner=36, outer=80):
    """Add a soft golden halo for sacred items."""
    for x in range(W):
        for y in range(H):
            dx, dy = x - cx, y - cy
            d2 = dx * dx + dy * dy
            if inner <= d2 <= outer and (x + y) % 2 == 0:
                put(px, x, y, HOLY_GLOW)


# ===========================================================
# PHASE 9 — SACRED CROPS + DISHES
# ===========================================================

def manna():
    """Manna — small white grains with golden glow."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    WHITE_DK = (200, 200, 180, 255)
    WHITE_B  = (240, 240, 230, 255)
    WHITE_HI = (255, 255, 250, 255)
    GOLD = (250, 220, 120, 255)
    # Pile of small white grains
    grains = [(11, 16), (14, 14), (17, 16), (20, 14), (13, 18), (16, 17),
              (19, 18), (12, 20), (15, 20), (18, 20), (14, 22), (17, 22)]
    for x, y in grains:
        put(px, x, y, WHITE_HI)
        put(px, x + 1, y, WHITE_B)
        put(px, x, y + 1, WHITE_DK)
        put(px, x + 1, y + 1, GOLD)
    return img


def pomegranate():
    """Pomegranate — red ruby fruit with crown stem, partially cut showing arils."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    DK = (100, 10, 20, 255)
    B  = (180, 30, 40, 255)
    HI = (220, 60, 70, 255)
    ARIL = (240, 30, 50, 255)
    ARIL_HI = (255, 90, 100, 255)
    CROWN = (90, 50, 20, 255)
    OL = (60, 8, 8, 255)
    POM = [
        "...OOOO....",
        "..OBBBBO...",
        ".OBHHHBSO..",
        ".OBHHBBSO..",
        "OBHHBBBBSO.",
        "OBHHBBBBSO.",
        "OBHBBBBBSO.",
        "OBBBBBBSSO.",
        ".OBBBBSSO..",
        "..OBBSSO...",
        "...OOOO....",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 10, POM, CM)
    # Crown stem (calyx)
    for x, y in [(14, 9), (15, 9), (17, 9), (18, 9), (16, 8)]:
        put(px, x, y, CROWN)
    # Open section showing arils (seeds inside)
    for x, y in [(14, 15), (16, 15), (18, 15), (15, 17), (17, 17)]:
        put(px, x, y, ARIL_HI)
    for x, y in [(15, 15), (17, 15), (16, 16), (14, 17), (18, 17)]:
        put(px, x, y, ARIL)
    return img


def blessed_wheat():
    """Blessed wheat — golden wheat stalk with glow."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    WHEAT_DK = (180, 130, 30, 255)
    WHEAT_B  = (240, 200, 60, 255)
    WHEAT_HI = (255, 230, 130, 255)
    STEM = (160, 110, 40, 255)
    OL = (100, 60, 10, 255)
    # Stem
    for y in range(8, 28):
        put(px, 16, y, STEM)
    # Wheat head — grain bundle
    GRAINS = [
        (15, 6), (16, 6), (17, 6),
        (14, 8), (15, 8), (16, 8), (17, 8), (18, 8),
        (14, 10), (15, 10), (16, 10), (17, 10), (18, 10),
        (14, 12), (15, 12), (16, 12), (17, 12), (18, 12),
        (15, 14), (16, 14), (17, 14),
    ]
    for x, y in GRAINS:
        put(px, x, y, WHEAT_B)
        put(px, x, y - 1, WHEAT_HI)
    # Outline
    for x in (13, 19):
        for y in range(7, 15):
            put(px, x, y, OL)
    # Awns (bristles)
    for x in (15, 17):
        put(px, x, 5, OL)
    return img


def blessed_grapes():
    """Blessed grapes — purple grapes with golden halo."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    DK = (60, 30, 80, 255)
    B  = (110, 60, 140, 255)
    HI = (170, 110, 200, 255)
    LEAF = (80, 140, 50, 255)
    STEM = (130, 90, 40, 255)
    OL = (30, 10, 40, 255)
    # Cluster
    grapes = [
        (15, 13), (18, 13),
        (13, 16), (16, 16), (19, 16), (21, 16),
        (15, 19), (18, 19),
        (16, 22),
    ]
    for cx, cy in grapes:
        put(px, cx, cy - 1, OL); put(px, cx + 1, cy - 1, OL)
        put(px, cx - 1, cy, OL); put(px, cx, cy, HI); put(px, cx + 1, cy, B); put(px, cx + 2, cy, OL)
        put(px, cx - 1, cy + 1, OL); put(px, cx, cy + 1, B); put(px, cx + 1, cy + 1, DK); put(px, cx + 2, cy + 1, OL)
        put(px, cx, cy + 2, OL); put(px, cx + 1, cy + 2, OL)
    # Stem + leaf
    put(px, 16, 11, STEM)
    put(px, 17, 10, STEM)
    for x, y in [(14, 10), (13, 10), (12, 11)]:
        put(px, x, y, LEAF)
    return img


def sacred_fig():
    """Sacred fig — single perfect fig with golden glow."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    DK = (80, 20, 60, 255)
    B  = (130, 40, 100, 255)
    HI = (180, 90, 150, 255)
    GREEN = (80, 130, 50, 255)
    OL = (30, 10, 30, 255)
    FIG = [
        "...OOO...",
        "..OBHBO..",
        ".OBHHBO..",
        "OBHHBBSO.",
        "OBHHBBSO.",
        "OBHHBBSO.",
        "OBHBBSSO.",
        "OBBBBSSO.",
        ".OBBSSO..",
        "..OOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 12, 11, FIG, CM)
    # Leaf stem
    put(px, 15, 10, GREEN)
    put(px, 16, 10, GREEN)
    put(px, 17, 10, GREEN)
    return img


def olive_tree_fruit():
    """Olive tree fruit — golden olive cluster (anointing olive)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    DK = (40, 60, 30, 255)
    B  = (90, 130, 60, 255)
    HI = (150, 200, 90, 255)
    GOLD = (220, 180, 60, 255)
    BRANCH = (90, 110, 50, 255)
    LEAF_DK = (40, 90, 40, 255)
    LEAF_B  = (90, 150, 70, 255)
    OL = (14, 30, 10, 255)
    # Olives on branch
    olives = [(11, 14), (15, 14), (19, 14), (13, 17), (17, 17), (21, 17)]
    for cx, cy in olives:
        put(px, cx, cy - 1, OL); put(px, cx + 1, cy - 1, OL)
        put(px, cx - 1, cy, OL); put(px, cx, cy, HI); put(px, cx + 1, cy, B); put(px, cx + 2, cy, OL)
        put(px, cx - 1, cy + 1, OL); put(px, cx, cy + 1, B); put(px, cx + 1, cy + 1, DK); put(px, cx + 2, cy + 1, OL)
        put(px, cx, cy + 2, OL); put(px, cx + 1, cy + 2, OL)
        # Golden highlight on each (anointed)
        put(px, cx, cy - 1, GOLD)
    # Branch
    for x in range(10, 24):
        put(px, x, 20, BRANCH)
    # Leaves
    for x, y in [(13, 19), (16, 19), (19, 19)]:
        put(px, x, y, LEAF_B)
    put(px, 16, 19, LEAF_DK)
    return img


def faith_mustard_seed():
    """Faith mustard seed — same as Phase 7 blessed version (re-emit for sacred set)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    DK = (130, 100, 30, 255)
    B  = (220, 180, 60, 255)
    HI = (255, 240, 130, 255)
    WHITE = (255, 255, 255, 255)
    OL = (80, 60, 20, 255)
    # Single large seed centered
    cells = {
        (-1, -2): OL, (0, -2): OL, (1, -2): OL,
        (-2, -1): OL, (-1, -1): HI, (0, -1): HI, (1, -1): B, (2, -1): OL,
        (-2, 0): OL, (-1, 0): HI, (0, 0): WHITE, (1, 0): B, (2, 0): OL,
        (-2, 1): OL, (-1, 1): B, (0, 1): B, (1, 1): DK, (2, 1): OL,
        (-1, 2): OL, (0, 2): OL, (1, 2): OL,
    }
    for (dx, dy), c in cells.items():
        put(px, 16 + dx, 16 + dy, c)
    return img


def communion_meal():
    """Communion meal — bread + wine on small altar/plate."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px, cx=16, cy=18)
    PLATE_DK = (180, 180, 190, 255)
    PLATE_B  = (230, 230, 235, 255)
    BREAD_DK = (140, 90, 40, 255)
    BREAD_B  = (200, 150, 80, 255)
    BREAD_HI = (240, 200, 130, 255)
    CUP_B = (200, 180, 50, 255)  # gold cup
    CUP_HI = (250, 230, 100, 255)
    WINE = (130, 20, 40, 255)
    OL = (40, 20, 8, 255)
    # Plate
    PLATE = [
        ".OOOOOOOOOOOO.",
        "OBBBBBBBBBBBBO",
        ".OBBBBBBBBBBO.",
        "..OOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': PLATE_B}
    stamp(px, 9, 22, PLATE, CM)
    # Bread (left side)
    BREAD = [
        ".OOOO.",
        "OBHHBO",
        "OBHBSO",
        "OBBSSO",
        ".OOOO.",
    ]
    CM = {'O': OL, 'B': BREAD_B, 'H': BREAD_HI, 'S': BREAD_DK}
    stamp(px, 10, 17, BREAD, CM)
    # Wine cup (right side)
    CUP = [
        "OOOOO",
        "OBHBO",
        "OBWBO",
        "OBWBO",
        ".OOO.",
    ]
    CM = {'O': OL, 'B': CUP_B, 'H': CUP_HI, 'W': WINE}
    stamp(px, 19, 17, CUP, CM)
    return img


def last_supper_spread():
    """Last Supper Spread — long table with bread + wine + fish + olive + lamb."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px, cx=16, cy=16, inner=64, outer=140)
    TABLE_DK = (110, 70, 30, 255)
    TABLE_B  = (170, 120, 60, 255)
    BREAD = (210, 160, 80, 255)
    WINE = (130, 20, 40, 255)
    CUP_GOLD = (220, 180, 50, 255)
    FISH = (150, 170, 200, 255)
    OLIVE = (60, 90, 40, 255)
    LAMB = (180, 90, 60, 255)
    HERB = (90, 160, 50, 255)
    OL = (40, 20, 8, 255)
    # Long table
    for x in range(3, 30):
        put(px, x, 16, OL)
        put(px, x, 17, TABLE_B)
        put(px, x, 18, TABLE_B)
        put(px, x, 19, TABLE_DK)
        put(px, x, 20, OL)
    # Items spread along the table
    # Bread (3 loaves)
    for cx in (6, 14, 22):
        put(px, cx, 14, OL); put(px, cx + 1, 14, OL); put(px, cx + 2, 14, OL)
        put(px, cx, 15, BREAD); put(px, cx + 1, 15, BREAD); put(px, cx + 2, 15, BREAD)
        put(px, cx, 16, OL); put(px, cx + 1, 16, OL); put(px, cx + 2, 16, OL)
    # Wine cups (2)
    for cx in (10, 24):
        put(px, cx, 13, CUP_GOLD)
        put(px, cx + 1, 13, CUP_GOLD)
        put(px, cx, 14, WINE)
        put(px, cx + 1, 14, WINE)
        put(px, cx, 15, OL)
        put(px, cx + 1, 15, OL)
    # Small fish
    for x, y in [(18, 14), (19, 14), (20, 14)]:
        put(px, x, y, FISH)
    put(px, 21, 14, OL)  # tail
    # Olives + herbs
    put(px, 12, 14, OLIVE)
    put(px, 26, 14, OLIVE)
    put(px, 8, 14, HERB)
    put(px, 28, 14, HERB)
    # Lamb chunks
    put(px, 16, 14, LAMB)
    return img


def manna_bread():
    """Manna bread — golden loaf with manna grains on top."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    BREAD_DK = (180, 130, 50, 255)
    BREAD_B  = (230, 180, 90, 255)
    BREAD_HI = (250, 220, 130, 255)
    MANNA = (255, 255, 250, 255)
    OL = (100, 60, 20, 255)
    LOAF = [
        "..OOOOOOOOOOOO..",
        ".OBHHHHHHHHHHHBO.",
        "OBHHBBBBBBBBHHBO",
        "OBHBBBBBBBBBBHBO",
        "OBHBBBBBBBBBBHBO",
        "OBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BREAD_B, 'H': BREAD_HI}
    stamp(px, 8, 12, LOAF, CM)
    # Manna grains sprinkled on top
    for x, y in [(11, 14), (14, 14), (17, 14), (20, 14), (13, 15), (16, 15), (19, 15)]:
        put(px, x, y, MANNA)
    return img


def anointing_oil_bread():
    """Anointing oil bread — bread with golden oil drizzle and hyssop sprig."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    add_holy_glow(px)
    BREAD_DK = (140, 90, 40, 255)
    BREAD_B  = (200, 150, 80, 255)
    BREAD_HI = (240, 200, 130, 255)
    OIL_DK = (200, 140, 20, 255)
    OIL_B  = (240, 190, 50, 255)
    OIL_HI = (255, 230, 110, 255)
    HYSSOP = (100, 90, 160, 255)
    HYSSOP_LEAF = (80, 130, 50, 255)
    OL = (80, 40, 10, 255)
    LOAF = [
        "..OOOOOOOOOO..",
        ".OBHHHHHHHHBO.",
        "OBHHBBBBBBHHBO",
        "OBHBBBBBBBBHBO",
        "OBBBBBBBBBBBBO",
        ".OBBBBBBBBBBO.",
        "..OOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BREAD_B, 'H': BREAD_HI}
    stamp(px, 10, 14, LOAF, CM)
    # Oil drizzle (diagonal pattern)
    for x, y in [(12, 16), (15, 17), (18, 16), (21, 17), (13, 18), (17, 18), (20, 18)]:
        put(px, x, y, OIL_B)
    for x, y in [(14, 17), (16, 17), (19, 17)]:
        put(px, x, y, OIL_HI)
    # Hyssop sprig on top
    for y in (10, 11, 12):
        put(px, 16, y, HYSSOP_LEAF)
    put(px, 15, 11, HYSSOP)
    put(px, 17, 11, HYSSOP)
    return img


# ===========================================================
# PHASE 10 — LEGENDARY FEASTS
# ===========================================================

def wedding_feast():
    """Wedding feast — multi-course plate with pasta, meat, dessert, wine."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PLATE_B = (240, 240, 245, 255)
    PASTA = (240, 190, 100, 255)
    SAUCE = (180, 40, 30, 255)
    MEAT = (140, 70, 40, 255)
    CAKE = (250, 200, 200, 255)
    CAKE_TOP = (255, 100, 130, 255)
    WINE_GLASS = (140, 30, 50, 255)
    HERB = (90, 160, 50, 255)
    OL = (80, 80, 100, 255)
    # Large oval plate
    PLATE = [
        "..OOOOOOOOOOOOO..",
        ".OBBBBBBBBBBBBBO.",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOO...",
    ]
    CM = {'O': OL, 'B': PLATE_B}
    stamp(px, 7, 13, PLATE, CM)
    # Pasta swirl (left)
    for x, y in [(10, 17), (11, 17), (12, 17), (11, 16), (12, 18)]:
        put(px, x, y, PASTA)
    put(px, 11, 17, SAUCE)
    # Meat (center)
    for x, y in [(15, 16), (16, 16), (17, 16), (15, 17), (16, 17), (17, 17)]:
        put(px, x, y, MEAT)
    # Cake (right)
    for x, y in [(20, 17), (21, 17), (22, 17), (20, 16), (21, 16), (22, 16)]:
        put(px, x, y, CAKE)
    put(px, 21, 15, CAKE_TOP)
    # Wine glass garnish
    put(px, 13, 14, WINE_GLASS)
    # Herb sprigs
    put(px, 14, 15, HERB)
    put(px, 19, 15, HERB)
    return img


def royal_thai_banquet():
    """Royal Thai banquet — tray with curry, pad thai, soup, rice."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    TRAY_DK = (120, 80, 40, 255)
    TRAY_B  = (180, 130, 70, 255)
    CURRY = (240, 190, 50, 255)
    NOODLE = (240, 200, 100, 255)
    SOUP_RED = (220, 70, 40, 255)
    RICE = (250, 245, 230, 255)
    SHRIMP = (240, 110, 90, 255)
    HERB = (90, 160, 50, 255)
    OL = (50, 30, 10, 255)
    # Large tray
    TRAY = [
        "OOOOOOOOOOOOOOOO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OOOOOOOOOOOOOOOO",
    ]
    CM = {'O': OL, 'B': TRAY_B}
    stamp(px, 8, 13, TRAY, CM)
    # 4 quadrant compartments
    # Top-left: curry (yellow)
    for x in range(10, 14):
        for y in range(15, 17):
            put(px, x, y, CURRY)
    # Top-right: pad thai
    for x in range(17, 22):
        for y in range(15, 17):
            put(px, x, y, NOODLE)
    put(px, 19, 16, SHRIMP)
    # Bottom-left: red soup
    for x in range(10, 14):
        for y in range(18, 20):
            put(px, x, y, SOUP_RED)
    # Bottom-right: rice
    for x in range(17, 22):
        for y in range(18, 20):
            put(px, x, y, RICE)
    # Herb garnish in middle
    put(px, 15, 17, HERB)
    put(px, 16, 17, HERB)
    return img


def tea_ceremony_set():
    """Tea ceremony — tray with matcha bowl, wagashi sweet, tea pot."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    TRAY_DK = (80, 50, 20, 255)
    TRAY_B  = (140, 100, 60, 255)
    MATCHA = (140, 200, 80, 255)
    MATCHA_DK = (90, 150, 50, 255)
    BOWL_DK = (70, 50, 30, 255)
    BOWL_B  = (140, 110, 70, 255)
    WAGASHI = (240, 180, 200, 255)
    TEAPOT_B = (200, 200, 200, 255)
    TEAPOT_DK = (100, 100, 100, 255)
    OL = (40, 20, 8, 255)
    # Wide flat tray
    TRAY = [
        "OOOOOOOOOOOOOOOO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OOOOOOOOOOOOOOOO",
    ]
    CM = {'O': OL, 'B': TRAY_B}
    stamp(px, 8, 21, TRAY, CM)
    # Matcha bowl (left, with bright green foam)
    BOWL = [
        ".OOOOO.",
        "OBMMMMO",
        "OBMMMMO",
        ".OOOOO.",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'M': MATCHA}
    stamp(px, 9, 16, BOWL, CM)
    # Foam highlight
    put(px, 11, 17, MATCHA_DK)
    # Wagashi sweet (small pink dessert)
    put(px, 16, 17, WAGASHI)
    put(px, 17, 17, WAGASHI)
    put(px, 16, 18, OL)
    put(px, 17, 18, OL)
    # Teapot (right) — small kettle silhouette
    TEAPOT = [
        ".OOOOO.",
        "OBHHHBO",
        "OBBBBBO",
        ".OOOOO.",
    ]
    CM = {'O': OL, 'B': TEAPOT_B, 'H': TEAPOT_DK}
    stamp(px, 20, 16, TEAPOT, CM)
    # Spout
    put(px, 26, 18, TEAPOT_B)
    put(px, 27, 18, OL)
    return img


def royal_curry_thali():
    """Royal Curry Thali — round metal tray with multiple small bowls."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    TRAY = (200, 200, 210, 255)
    TRAY_DK = (140, 140, 150, 255)
    CURRY1 = (220, 130, 40, 255)   # butter chicken
    CURRY2 = (140, 100, 30, 255)   # dal
    CURRY3 = (90, 140, 40, 255)    # saag
    RICE = (250, 245, 230, 255)
    NAAN = (230, 180, 110, 255)
    CHUTNEY = (130, 30, 30, 255)
    SWEET = (250, 200, 80, 255)
    OL = (60, 60, 70, 255)
    # Round thali platter
    THALI = [
        "...OOOOOOOOOO...",
        "..OBBBBBBBBBBBO..",
        ".OBBBBBBBBBBBBBO.",
        "OBBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBBO.",
        "..OBBBBBBBBBBBO..",
        "...OOOOOOOOOO...",
    ]
    CM = {'O': OL, 'B': TRAY}
    stamp(px, 7, 11, THALI, CM)
    # Multiple curry pots arranged
    # Top-left
    put(px, 11, 13, CURRY1); put(px, 12, 13, CURRY1)
    # Top-right
    put(px, 19, 13, CURRY2); put(px, 20, 13, CURRY2)
    # Center: rice mound
    for x, y in [(14, 14), (15, 14), (16, 14), (17, 14), (15, 15), (16, 15)]:
        put(px, x, y, RICE)
    # Left-mid: saag
    put(px, 10, 16, CURRY3); put(px, 11, 16, CURRY3)
    # Right-mid: chutney
    put(px, 20, 16, CHUTNEY); put(px, 21, 16, CHUTNEY)
    # Bottom: naan
    for x in range(13, 19):
        put(px, x, 18, NAAN)
    # Sweet (small yellow dessert)
    put(px, 16, 17, SWEET)
    return img


# ===========================================================
# DRIVER
# ===========================================================
JOBS = [
    # Phase 9 — Sacred crops
    ("sacred", "manna",              manna),
    ("sacred", "pomegranate",        pomegranate),
    ("sacred", "blessed_wheat",      blessed_wheat),
    ("sacred", "blessed_grapes",     blessed_grapes),
    ("sacred", "sacred_fig",         sacred_fig),
    ("sacred", "olive_tree_fruit",   olive_tree_fruit),
    ("sacred", "faith_mustard_seed", faith_mustard_seed),
    # Phase 9 — Tier-7 dishes
    ("dishes", "communion_meal",     communion_meal),
    ("dishes", "last_supper_spread", last_supper_spread),
    ("dishes", "manna_bread",        manna_bread),
    ("dishes", "anointing_oil_bread", anointing_oil_bread),
    # Phase 10 — Legendary feasts
    ("dishes", "wedding_feast",      wedding_feast),
    ("dishes", "royal_thai_banquet", royal_thai_banquet),
    ("dishes", "tea_ceremony_set",   tea_ceremony_set),
    ("dishes", "royal_curry_thali",  royal_curry_thali),
]

if __name__ == "__main__":
    for folder, name, fn in JOBS:
        out = f"/home/sparky/ogrs/art/items/{folder}"
        os.makedirs(out, exist_ok=True)
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {folder}/{name}")
    print(f"\n=== Phase 9+10 complete: {len(JOBS)} sprites ===")
