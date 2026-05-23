#!/usr/bin/env python3
"""
Phase 6 — Orchard fruits (Tier-3 crops, longer cycle).

10 fruits × 2 sprites (raw + prepared) = 20 sprites at 32×32.

Orchard fruits don't have seed icons because they propagate from
cuttings/saplings (different scenery system). Just raw fruit + processed.

  Wine Grapes → Wine (bottle exists in Phase 2 addons; here we have grapes + must)
  Olives      → Olive Oil (oil bottle in Phase 2; here olives + tapenade)
  Figs        → Dried figs
  Apples      → Apple pie
  Pears       → Poached pears
  Cherries    → Cherry jam
  Pineapples  → Sliced rings
  Bananas     → Banana bread
  Coconuts    → Halved/cracked
  Avocado     → Halved / guacamole
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


OL_GENERAL = ( 40,  24,  16, 255)


# ===========================================================
# WINE GRAPES
# ===========================================================
def grapes():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 50,  20,  50, 255)
    B  = ( 90,  40, 100, 255)
    HI = (140,  80, 170, 255)
    PALE = (180, 120, 210, 255)
    LEAF_DK = ( 30,  80,  20, 255)
    LEAF_B  = ( 80, 140,  50, 255)
    STEM = (130,  90,  40, 255)
    OL = ( 20,   8,  30, 255)
    # Cluster of grapes in triangular bunch
    grape_positions = [
        (14, 14), (17, 14), (20, 14),
        (13, 17), (16, 17), (19, 17), (22, 17),
        (15, 20), (18, 20),
        (16, 23),
    ]
    for cx, cy in grape_positions:
        # 3x3 grape
        put(px, cx, cy - 1, OL); put(px, cx + 1, cy - 1, OL)
        put(px, cx - 1, cy, OL); put(px, cx, cy, HI); put(px, cx + 1, cy, B); put(px, cx + 2, cy, OL)
        put(px, cx - 1, cy + 1, OL); put(px, cx, cy + 1, B); put(px, cx + 1, cy + 1, DK); put(px, cx + 2, cy + 1, OL)
        put(px, cx, cy + 2, OL); put(px, cx + 1, cy + 2, OL)
    # Stem + leaf at top
    put(px, 16, 12, STEM)
    put(px, 17, 11, STEM)
    put(px, 18, 10, STEM)
    # Grape leaf
    LEAF = [
        ".OO.",
        "OBHO",
        "OBBO",
        ".OO.",
    ]
    CM = {'O': LEAF_DK, 'B': LEAF_B, 'H': LEAF_B}
    stamp(px, 11, 10, LEAF, CM)
    return img


def grape_must():
    """Grape must (crushed grapes ready for wine)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 70,  46,  24, 255)
    BOWL_B  = (138,  90,  46, 255)
    MUST_DK = ( 70,  20,  60, 255)
    MUST_B  = (130,  40, 110, 255)
    MUST_HI = (180,  90, 180, 255)
    OL      = ( 30,  18,   8, 255)
    BOWL = [
        ".OOOOOOOOOOOOO.",
        "OBBBBBBBBBBBBBO",
        "OBBMMMMMMMMMBBO",
        "OBMMMMMMMMMMMBO",
        "OBMHMMMHMMMMHBO",
        "OBMMMMMMMMMMMBO",
        ".OBBMMMMMMMMBO.",
        "..OOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'M': MUST_B, 'H': MUST_HI}
    stamp(px, 8, 14, BOWL, CM)
    return img


# ===========================================================
# OLIVES
# ===========================================================
def olives_cluster():
    """Branch of olives (5-6 olives on branch)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  40,  20, 255)
    B  = ( 70,  90,  40, 255)
    HI = (120, 150,  70, 255)
    BLACK_DK = ( 20,  20,  20, 255)
    BLACK_B  = ( 60,  60,  60, 255)
    BRANCH = ( 90, 110,  50, 255)
    LEAF_DK = ( 40,  90,  40, 255)
    LEAF_B  = ( 80, 140,  70, 255)
    OL = ( 14,  20,  10, 255)
    # Olives in 2 clusters
    green_olives = [(11, 14), (14, 14), (10, 17), (13, 17)]
    black_olives = [(19, 14), (22, 14), (20, 17)]
    for cx, cy in green_olives:
        put(px, cx, cy - 1, OL); put(px, cx + 1, cy - 1, OL)
        put(px, cx - 1, cy, OL); put(px, cx, cy, HI); put(px, cx + 1, cy, B); put(px, cx + 2, cy, OL)
        put(px, cx - 1, cy + 1, OL); put(px, cx, cy + 1, B); put(px, cx + 1, cy + 1, DK); put(px, cx + 2, cy + 1, OL)
        put(px, cx, cy + 2, OL); put(px, cx + 1, cy + 2, OL)
    for cx, cy in black_olives:
        put(px, cx, cy - 1, OL); put(px, cx + 1, cy - 1, OL)
        put(px, cx - 1, cy, OL); put(px, cx, cy, BLACK_B); put(px, cx + 1, cy, BLACK_DK); put(px, cx + 2, cy, OL)
        put(px, cx - 1, cy + 1, OL); put(px, cx, cy + 1, BLACK_DK); put(px, cx + 1, cy + 1, BLACK_DK); put(px, cx + 2, cy + 1, OL)
        put(px, cx, cy + 2, OL); put(px, cx + 1, cy + 2, OL)
    # Branch
    for x in range(11, 24):
        put(px, x, 21, BRANCH)
    # Leaf
    for x, y in [(15, 19), (16, 19), (17, 20)]:
        put(px, x, y, LEAF_B)
    put(px, 16, 19, LEAF_DK)
    return img


def tapenade():
    """Olive tapenade — chunky olive paste in bowl."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 70,  46,  24, 255)
    BOWL_B  = (138,  90,  46, 255)
    TAP_DK  = ( 30,  40,  20, 255)
    TAP_B   = ( 70,  90,  40, 255)
    TAP_HI  = (110, 140,  60, 255)
    OIL     = (220, 180,  40, 255)
    OL      = ( 30,  18,   8, 255)
    BOWL = [
        ".OOOOOOOOOOOOO.",
        "OBBBBBBBBBBBBBO",
        "OBBTTTTTTTTTBBO",
        "OBTTTTTTTTTTTBO",
        "OBTTTTTTTTTTTBO",
        ".OBBTTTTTTTBBO.",
        "..OOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'T': TAP_B}
    stamp(px, 8, 14, BOWL, CM)
    # Chunky texture
    for x, y in [(12, 16), (15, 16), (18, 16), (13, 17), (16, 17), (19, 17)]:
        put(px, x, y, TAP_DK)
    # Oil sheen
    for x, y in [(14, 17), (17, 17)]:
        put(px, x, y, OIL)
    return img


# ===========================================================
# FIGS
# ===========================================================
def figs_raw():
    """2-3 ripe figs."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 80,  20,  60, 255)
    B  = (130,  40, 100, 255)
    HI = (180,  90, 150, 255)
    GREEN = ( 80, 130,  50, 255)
    INSIDE = (240, 110, 100, 255)
    SEED = (240, 220, 150, 255)
    OL = ( 30,  10,  30, 255)
    # First fig (whole, teardrop shape)
    FIG = [
        "..OOO..",
        ".OBHO..",
        ".OHHBO.",
        "OBHBBSO",
        "OBHBBSO",
        "OBHBBSO",
        "OBBBSSO",
        ".OBSSO.",
        "..OOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 9, 11, FIG, CM)
    # Stem leaf at top
    put(px, 12, 10, GREEN)
    put(px, 13, 10, GREEN)
    # Second fig (cut open, showing inside)
    stamp(px, 18, 11, FIG, CM)
    put(px, 21, 10, GREEN)
    # Cut interior — pinkish with seeds
    for x in range(20, 24):
        put(px, x, 14, INSIDE)
        put(px, x, 15, INSIDE)
    for x, y in [(21, 14), (22, 15)]:
        put(px, x, y, SEED)
    return img


def figs_dried():
    """Dried figs — wrinkly brown."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 80,  50,  20, 255)
    B  = (140,  90,  40, 255)
    HI = (190, 140,  70, 255)
    WRINKLE = ( 60,  30,  10, 255)
    OL = ( 30,  16,   8, 255)
    figs = [(12, 16), (20, 17), (16, 21)]
    for cx, cy in figs:
        FIG = [
            ".OOOO.",
            "OBHHBO",
            "OBHBBSO",
            "OBHBBSO",
            "OBBSSSO",
            ".OOOOO.",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
        stamp(px, cx - 2, cy - 3, FIG, CM)
        # Wrinkle lines
        put(px, cx, cy, WRINKLE)
        put(px, cx + 1, cy + 1, WRINKLE)
    return img


# ===========================================================
# APPLES
# ===========================================================
def apple():
    """Red apple."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (140,  20,  10, 255)
    B  = (210,  40,  30, 255)
    HI = (240,  90,  50, 255)
    SHEEN = (255, 180, 130, 255)
    LEAF_DK = ( 30,  80,  20, 255)
    LEAF_B  = ( 80, 140,  50, 255)
    STEM = (100,  60,  20, 255)
    OL = ( 60,  10,   8, 255)
    APPLE = [
        "...OOOOOO...",
        "..OBHHHHBSO.",
        ".OBHHHHBBBSO",
        "OBHHHBBBBBSO",
        "OBHHBBBBBBSSO",
        "OBHBBBBBBBSSO",
        "OBBBBBBBBSSSO",
        "OBBBBBBBSSSSO",
        ".OBBBBSSSSSO.",
        "..OOBSSSSOO..",
        "...OOOOOO....",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 10, 10, APPLE, CM)
    # Shiny highlight
    put(px, 13, 12, SHEEN)
    put(px, 14, 12, SHEEN)
    # Stem
    put(px, 15, 9, STEM)
    put(px, 16, 9, STEM)
    # Leaf
    put(px, 17, 9, LEAF_B)
    put(px, 18, 9, LEAF_DK)
    return img


def apple_pie():
    """Slice of apple pie."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CRUST_DK = ( 90,  56,  20, 255)
    CRUST_B  = (180, 130,  60, 255)
    CRUST_HI = (230, 180, 100, 255)
    FILL_DK  = (160,  90,  30, 255)
    FILL_B   = (220, 150,  70, 255)
    FILL_HI  = (250, 200, 110, 255)
    APPLE_BIT = (230,  80,  40, 255)
    OL = ( 40,  20,   8, 255)
    PIE = [
        "..OOOOOOOOOO..",
        ".OBBBBBBBBBBO.",
        "OBHHBBBBBBBHBO",
        "OBHFFFFFFFHBSO",
        "OBFFFFFFFFFBSO",
        "OBFFFFFFFFFBSO",
        ".OBBFFFFFBBSO.",
        "..OBBBBBBBSO..",
        "...OOOOOOOO...",
    ]
    CM = {'O': OL, 'B': CRUST_B, 'H': CRUST_HI, 'F': FILL_B, 'S': CRUST_DK}
    stamp(px, 9, 13, PIE, CM)
    # Apple chunks visible in filling
    for x, y in [(13, 17), (16, 16), (19, 17), (14, 18)]:
        put(px, x, y, APPLE_BIT)
    # Lattice top hints
    for x in [14, 17, 20]:
        put(px, x, 16, FILL_HI)
    return img


# ===========================================================
# PEARS
# ===========================================================
def pear():
    """Yellow-green pear."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (140, 130,  20, 255)
    B  = (210, 200,  60, 255)
    HI = (240, 230, 110, 255)
    PALE = (180, 200,  80, 255)
    BLUSH = (220, 100,  40, 255)
    STEM = (100,  60,  20, 255)
    LEAF = ( 80, 140,  50, 255)
    OL = ( 80,  60,  10, 255)
    PEAR = [
        "....OOO....",
        "...OBHBO...",
        "..OBHHBO...",
        "..OBHHBSO..",
        ".OBHHBBBSO.",
        "OBHHHBBBBSO",
        "OBHHBBBBBSO",
        "OBHBBBBBBSO",
        "OBBBBBBBSSO",
        ".OBBBBBSSO.",
        "..OOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 10, PEAR, CM)
    # Blush
    put(px, 14, 14, BLUSH)
    put(px, 13, 15, BLUSH)
    # Stem
    put(px, 15, 9, STEM)
    # Leaf
    put(px, 16, 9, LEAF)
    return img


def pear_poached():
    """Poached pear in syrup — pear sits in a small bowl."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 70,  46,  24, 255)
    BOWL_B  = (138,  90,  46, 255)
    SYRUP = (200, 120,  60, 255)
    SYRUP_HI = (240, 160,  90, 255)
    PEAR_DK = (140, 100,  40, 255)
    PEAR_B  = (200, 160,  80, 255)
    PEAR_HI = (240, 200, 130, 255)
    OL = ( 30,  18,   8, 255)
    # Small bowl
    BOWL = [
        ".OOOOOOOOOOOO.",
        "OBBBBBBBBBBBBO",
        "OBSSSSSSSSSBBO",
        "OBSSSSSSSSSBBO",
        ".OOBBBBBBBBOO.",
        "..OOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'S': SYRUP}
    stamp(px, 9, 18, BOWL, CM)
    # Pear sitting in bowl (smaller, upright)
    PEAR = [
        "..OOO..",
        ".OBHBO.",
        "OBHHBSO",
        "OBHBBSO",
        "OBBBSSO",
        ".OBSSO.",
        ".OOOOO.",
    ]
    CM = {'O': OL, 'B': PEAR_B, 'H': PEAR_HI, 'S': PEAR_DK}
    stamp(px, 13, 12, PEAR, CM)
    # Syrup highlight
    for x, y in [(12, 21), (18, 21), (15, 22)]:
        put(px, x, y, SYRUP_HI)
    return img


# ===========================================================
# CHERRIES
# ===========================================================
def cherries():
    """Pair of red cherries on stems."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 90,  10,  10, 255)
    B  = (180,  20,  30, 255)
    HI = (230,  60,  70, 255)
    SHEEN = (255, 130, 130, 255)
    STEM = (100,  80,  20, 255)
    LEAF = ( 80, 140,  50, 255)
    OL = ( 40,   8,   8, 255)
    # Two cherries side-by-side on connected stems
    cherries = [(12, 19), (20, 21)]
    for cx, cy in cherries:
        CH = [
            ".OOOO.",
            "OBHHBO",
            "OBHHBSO",
            "OBHBBSO",
            "OBBBSSO",
            ".OBSSO.",
            "..OOO..",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
        stamp(px, cx - 2, cy - 3, CH, CM)
        # Sheen
        put(px, cx, cy - 1, SHEEN)
    # Stems meeting at top
    for x, y in [(13, 16), (14, 15), (15, 14), (16, 13), (17, 12), (18, 11), (19, 12), (20, 13), (21, 14), (22, 16), (21, 18)]:
        put(px, x, y, STEM)
    # Leaf
    for x, y in [(18, 9), (19, 9), (20, 10)]:
        put(px, x, y, LEAF)
    return img


def cherry_jam():
    """Cherry jam — red jam in jar."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    JAR_DK = ( 70,  90, 110, 255)
    JAR_B  = (150, 180, 210, 255)
    JAR_HI = (210, 230, 245, 255)
    JAM_DK = (100,  10,  20, 255)
    JAM_B  = (180,  30,  40, 255)
    JAM_HI = (230,  70,  90, 255)
    LID    = (140,  20,  30, 255)
    OL     = ( 30,  40,  60, 255)
    JAR = [
        ".OOOOOOOO.",
        "OLLLLLLLLO",
        "OOOOOOOOOO",
        "OBHHBBBBBO",
        "OBHJJJJJJO",
        "OBJJJJJJJO",
        "OBJJJJJJJO",
        "OBJJJJJJJO",
        "OBBJJJJJJO",
        "OBBBBBBBBO",
        ".OOOOOOOO.",
    ]
    CM = {'O': OL, 'B': JAR_B, 'H': JAR_HI, 'J': JAM_B, 'L': LID}
    stamp(px, 11, 11, JAR, CM)
    # Cherry chunks in jam
    for x, y in [(14, 17), (17, 18), (15, 19)]:
        put(px, x, y, JAM_DK)
    return img


# ===========================================================
# PINEAPPLES
# ===========================================================
def pineapple():
    """Whole pineapple with spiky crown."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (140,  90,  20, 255)
    B  = (210, 150,  40, 255)
    HI = (240, 190,  80, 255)
    PALE = (255, 220, 120, 255)
    LEAF_DK = ( 30,  80,  20, 255)
    LEAF_B  = ( 80, 140,  50, 255)
    LEAF_HI = (130, 200,  80, 255)
    OL = ( 60,  30,  10, 255)
    # Crown (spiky leaves at top)
    crown_cells = [
        (16, 5), (15, 6), (16, 6), (17, 6),
        (14, 7), (15, 7), (16, 7), (17, 7), (18, 7),
        (13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 8), (19, 8),
        (13, 9), (15, 9), (17, 9), (19, 9),
    ]
    for x, y in crown_cells:
        put(px, x, y, LEAF_B)
    # Crown highlights
    for x, y in [(16, 5), (16, 6), (16, 7)]:
        put(px, x, y, LEAF_HI)
    # Pineapple body (oval)
    BODY = [
        "..OOOOOO..",
        ".OBHHHHBSO.",
        "OBHHHBBBBSO",
        "OBHHHBBBBSO",
        "OBHHBBBBBSO",
        "OBHBBBBBBSO",
        "OBBBBBBBSSO",
        ".OBBBBBSSO.",
        "..OOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 12, BODY, CM)
    # Diamond pattern texture
    for x, y in [(13, 14), (15, 14), (17, 14), (19, 14),
                 (12, 16), (14, 16), (16, 16), (18, 16), (20, 16),
                 (13, 18), (15, 18), (17, 18), (19, 18)]:
        put(px, x, y, DK)
    return img


def pineapple_rings():
    """Pineapple rings (cut)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180, 140,  20, 255)
    B  = (240, 200,  60, 255)
    HI = (255, 230, 100, 255)
    CORE = (240, 220, 150, 255)
    OL = ( 80,  50,  10, 255)
    # 3 rings stacked
    rings = [(16, 12), (16, 19), (16, 26)]
    for cx, cy in rings:
        RING = [
            "..OOOOOOO..",
            ".OBHHHHHBSO.",
            "OBHHCCCHHHSO",
            "OBHCCCCCHSSO",
            "OBHHCCCHHHSO",
            ".OBBHHHBBSO.",
            "..OOOOOOO..",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'C': CORE, 'S': DK}
        stamp(px, cx - 5, cy - 3, RING, CM)
    return img


# ===========================================================
# BANANAS
# ===========================================================
def banana():
    """Yellow banana, curved."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180, 140,  20, 255)
    B  = (240, 210,  40, 255)
    HI = (255, 235,  80, 255)
    TIP = (130,  90,  20, 255)
    BROWN = (100,  60,  10, 255)
    OL = ( 80,  50,  10, 255)
    BAN = [
        "...OOO........",
        "..OBBO........",
        ".OBHBO........",
        ".OBHO.........",
        "..OBBO........",
        "...OBBO.......",
        "....OBBO......",
        ".....OBBO.....",
        "......OBBO....",
        ".......OBBO...",
        "........OBBO..",
        ".........OBOO.",
        "..........OBOO",
        "...........OOO",
    ]
    CM = {'O': OL, 'B': B, 'H': HI}
    stamp(px, 8, 7, BAN, CM)
    # Tip dot
    put(px, 8, 8, TIP)
    return img


def banana_bread():
    """Banana bread — golden brown loaf."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BREAD_DK = (130,  70,  20, 255)
    BREAD_B  = (200, 140,  60, 255)
    BREAD_HI = (240, 190, 100, 255)
    INSIDE = (240, 210, 130, 255)
    WALNUT = ( 90,  50,  20, 255)
    OL = ( 50,  20,   8, 255)
    LOAF = [
        "..OOOOOOOOOOO..",
        ".OBHHHHHHHHHBO.",
        "OBHIIIIIIIIIHBO",
        "OBIIIIIIIIIIIBO",
        "OBIWIIWIIWIIBSO",
        "OBIIIIIIIIIIBBO",
        "OBIIWIIIIWIIBSO",
        "OBBIIIIIIIIBSSO",
        ".OBBBBBBBBBBSO.",
        "..OOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BREAD_B, 'H': BREAD_HI, 'I': INSIDE, 'S': BREAD_DK, 'W': WALNUT}
    stamp(px, 8, 11, LOAF, CM)
    return img


# ===========================================================
# COCONUTS
# ===========================================================
def coconut():
    """Whole coconut — brown husky sphere."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 60,  30,  10, 255)
    B  = (110,  60,  20, 255)
    HI = (170,  90,  40, 255)
    HUSK = ( 90,  50,  20, 255)
    OL = ( 30,  16,   8, 255)
    COC = [
        "...OOOOOOOO...",
        "..OBHHHHHHBSO.",
        ".OBHHBBBBBBBSO",
        "OBHHBBBBBBBBSO",
        "OBHBBBBBBBBSSO",
        "OBHBBBBBBBBSSO",
        "OBBBBBBBBBBSSO",
        "OBBBBBBBBBSSSO",
        ".OBBBBBBBSSSO.",
        "..OOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 9, 11, COC, CM)
    # Hairy fiber texture
    for x, y in [(12, 14), (15, 15), (18, 14), (13, 17), (19, 17), (16, 19)]:
        put(px, x, y, HUSK)
    # 3 "eyes" of the coconut
    for x, y in [(14, 15), (17, 15), (15, 17)]:
        put(px, x, y, DK)
    return img


def coconut_halved():
    """Halved coconut showing white interior + brown rim."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 60,  30,  10, 255)
    B  = (110,  60,  20, 255)
    WHITE = (250, 245, 230, 255)
    WHITE_DK = (210, 200, 180, 255)
    OL = ( 30,  16,   8, 255)
    HALF = [
        "..OOOOOOOOOO..",
        ".OBBBBBBBBBBSO.",
        "OBBWWWWWWWWBSO",
        "OBWWWWWWWWWWBSO",
        "OBWWWWWWWWWWBSO",
        "OBWWWWWWWWWBSSO",
        "OBBBBBBBBBSSSSO",
        ".OOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B, 'W': WHITE, 'S': DK}
    stamp(px, 9, 12, HALF, CM)
    # Inner shadow
    for x in range(13, 20):
        put(px, x, 18, WHITE_DK)
    return img


# ===========================================================
# AVOCADO
# ===========================================================
def avocado():
    """Whole avocado — pear-shaped green fruit."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  60,  20, 255)
    B  = ( 70, 110,  40, 255)
    HI = (110, 160,  60, 255)
    PALE = (160, 200, 100, 255)
    STEM = ( 80,  50,  20, 255)
    OL = ( 14,  30,   8, 255)
    AVO = [
        "....OOO....",
        "...OBHBO...",
        "..OBHHBSO..",
        ".OBHHBBSO..",
        ".OBHHBBSO..",
        ".OBHBBBSO..",
        "OBHBBBBSSO.",
        "OBHBBBBSSO.",
        "OBBBBBSSSSO",
        "OBBBBSSSSSO",
        ".OBBBSSSSO.",
        "..OOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 9, AVO, CM)
    # Stem
    put(px, 15, 8, STEM)
    return img


def avocado_halved():
    """Halved avocado showing flesh + pit."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SKIN_DK = ( 30,  60,  20, 255)
    SKIN_B  = ( 70, 110,  40, 255)
    FLESH_B = (180, 200,  80, 255)
    FLESH_HI = (220, 230, 120, 255)
    PIT_DK = (100,  60,  20, 255)
    PIT_B  = (160, 100,  40, 255)
    OL = ( 14,  30,   8, 255)
    HALF = [
        "....OOOOOOO....",
        "...OBFFFFFFBO..",
        "..OBFFFFFFFFBO.",
        ".OBFFFFFFFFFFBO",
        ".OBFFFPPFFFFFBO",
        ".OBFFFPPPFFFFBO",
        ".OBFFFFPPFFFFBO",
        ".OBFFFFFFFFFFBO",
        ".OBBFFFFFFFFFBO",
        "..OBBFFFFFFFBO.",
        "...OBBBBBBBO...",
        "....OOOOOOO....",
    ]
    CM = {'O': OL, 'B': SKIN_B, 'F': FLESH_B, 'P': PIT_B}
    stamp(px, 9, 10, HALF, CM)
    # Highlight on flesh
    for x, y in [(12, 13), (15, 12), (18, 13)]:
        put(px, x, y, FLESH_HI)
    # Pit detail
    put(px, 15, 14, PIT_DK)
    put(px, 16, 14, PIT_DK)
    return img


# ===========================================================
# DRIVER
# ===========================================================
JOBS = [
    ("fruit_grapes",    "grapes",       grapes),
    ("fruit_grapes",    "grape_must",   grape_must),
    ("fruit_olives",    "olives",       olives_cluster),
    ("fruit_olives",    "tapenade",     tapenade),
    ("fruit_figs",      "figs_raw",     figs_raw),
    ("fruit_figs",      "figs_dried",   figs_dried),
    ("fruit_apple",     "apple",        apple),
    ("fruit_apple",     "apple_pie",    apple_pie),
    ("fruit_pear",      "pear",         pear),
    ("fruit_pear",      "pear_poached", pear_poached),
    ("fruit_cherry",    "cherries",     cherries),
    ("fruit_cherry",    "cherry_jam",   cherry_jam),
    ("fruit_pineapple", "pineapple",    pineapple),
    ("fruit_pineapple", "pineapple_rings", pineapple_rings),
    ("fruit_banana",    "banana",       banana),
    ("fruit_banana",    "banana_bread", banana_bread),
    ("fruit_coconut",   "coconut",      coconut),
    ("fruit_coconut",   "coconut_halved", coconut_halved),
    ("fruit_avocado",   "avocado",      avocado),
    ("fruit_avocado",   "avocado_halved", avocado_halved),
]

if __name__ == "__main__":
    for folder, name, fn in JOBS:
        out = f"/home/sparky/ogrs/art/items/{folder}"
        os.makedirs(out, exist_ok=True)
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {folder}/{name}")
    print(f"\n=== Phase 6 complete: {len(JOBS)} orchard fruit sprites ===")
