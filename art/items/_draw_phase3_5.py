#!/usr/bin/env python3
"""
Phase 3.5 — Missing ingredients for Tier 4+ recipes.

20 sprites at 32×32. Covers gaps in the Phase 1+2 ingredient set so we
can fully express dishes like Lasagna, Pad Thai, Biryani, Coq au Vin, Mole,
Kimchi Stew, Tagine, etc.

Grouped:
  Proteins        : bacon, sausage, shrimp, tofu
  Asian staples   : scallion, nori, peanut, bean sprouts, tamarind, kimchi
  Citrus          : lime, lemon
  Dairy           : yogurt, olive (jar)
  Herbs           : cilantro, basil (fresh bundles)
  Breads          : tortilla, naan
  Sweets          : cocoa, apricot
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


OUTLINE = (40, 24, 16, 255)


# ===========================================================
# PROTEINS
# ===========================================================
def bacon():
    """Strip of bacon with fat marbling."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    MEAT_DK = (160,  60,  40, 255)
    MEAT_B  = (220,  90,  60, 255)
    MEAT_HI = (250, 130,  90, 255)
    FAT     = (250, 220, 190, 255)
    OL      = ( 80,  30,  16, 255)
    STRIP = [
        ".OOOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBBBSO",
        "OBHHFFFFBBBBFFBSO",
        "OFFFBBBBFFFFBBBSO",
        "OBBBFFFFBBBBFFBSO",
        "OBHBBBBBBBBBBBSSO",
        ".OOOOOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': MEAT_B, 'H': MEAT_HI, 'S': MEAT_DK, 'F': FAT}
    stamp(px, 7, 13, STRIP, CM)
    return img


def sausage():
    """Plump sausage link, browned."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 80,  30,  20, 255)
    B  = (160,  80,  40, 255)
    HI = (220, 130,  70, 255)
    PEAK = (250, 180, 110, 255)
    OL = ( 40,  16,   8, 255)
    SAUSAGE = [
        "..OOOOOOOOOOOOO..",
        ".OHHBBBBBBBBBSSO.",
        "OBHHBBBBBBBBBBSSO",
        "OBHBPBBBBBBBBBSSO",
        "OBHBBBBBBBBBBBSSO",
        ".OBBBBBBBBBBBSSO.",
        "..OOOOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK, 'P': PEAK}
    stamp(px, 8, 13, SAUSAGE, CM)
    return img


def shrimp():
    """Pink curled shrimp with tail."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180,  60,  50, 255)
    B  = (240, 110,  90, 255)
    HI = (255, 160, 140, 255)
    TAIL = (200,  80,  70, 255)
    OL = ( 80,  20,  16, 255)
    # C-curved shrimp shape
    SHR = [
        "....OOOOO....",
        "...OBHHHBO...",
        "..OBHHHBBSO..",
        ".OBHHBBBBSO..",
        "OBHHBBBBSSO..",
        "OBHBBBSSSO...",
        "OBBBSSSSO....",
        ".OBSSSO......",
        "..OOSO.......",
        "..OTSO.......",
        "..OTTO.......",
        "...OO........",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK, 'T': TAIL}
    stamp(px, 10, 10, SHR, CM)
    return img


def tofu():
    """White tofu block — soft cube."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (200, 200, 180, 255)
    B  = (240, 240, 220, 255)
    HI = (255, 255, 250, 255)
    OL = ( 80,  80,  60, 255)
    CUBE = [
        ".OOOOOOOOOOOOOO.",
        "OHHHHBBBBBBBBSSO",
        "OHHHHBBBBBBBBSSO",
        "OHHHBBBBBBBBBSSO",
        "OBHHBBBBBBBBBSSO",
        "OBBBBBBBBBBBSSSO",
        "OBBBBBBBBBBBSSSO",
        "OBBBBBBBBBBSSSSO",
        ".OOOOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 8, 12, CUBE, CM)
    return img


# ===========================================================
# ASIAN STAPLES
# ===========================================================
def scallion():
    """Green onion bunch — white bulb + green stalks."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GREEN_DK = ( 40,  90,  30, 255)
    GREEN_B  = ( 90, 170,  60, 255)
    GREEN_HI = (140, 220, 100, 255)
    WHITE_DK = (200, 200, 180, 255)
    WHITE_B  = (240, 240, 220, 255)
    OL       = ( 16,  44,  10, 255)
    # 3 stalks bundled
    for x in (14, 16, 18):
        # Green top (long)
        for y in range(6, 18):
            put(px, x, y, GREEN_B)
            put(px, x - 1, y, OL if x == 14 else GREEN_DK)
            put(px, x + 1, y, OL if x == 18 else GREEN_DK)
        # White bulb (bottom)
        for y in range(18, 24):
            put(px, x, y, WHITE_B)
            put(px, x - 1, y, OL if x == 14 else WHITE_DK)
            put(px, x + 1, y, OL if x == 18 else WHITE_DK)
        # Highlight on left side
        put(px, x, 8, GREEN_HI)
        put(px, x, 11, GREEN_HI)
    # Top tips (slightly curved out)
    for x in (13, 19):
        put(px, x, 6, GREEN_DK)
    # Bulb bottoms (rounded)
    for x in (13, 19):
        put(px, x, 23, WHITE_DK)
    # Root wisps
    put(px, 15, 25, OL); put(px, 16, 25, OL); put(px, 17, 25, OL)
    return img


def nori():
    """Sheet of nori (seaweed) — dark green/black rectangle."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 10,  20,  10, 255)
    B  = ( 30,  60,  30, 255)
    HI = ( 60, 100,  50, 255)
    OL = (  5,  12,   5, 255)
    SHEET = [
        ".OOOOOOOOOOOOOOO.",
        "OBHHBBBBBBBBBSSSO",
        "OBHBBHBBBHBBBHSSO",
        "OBHBBBBHBBBBHBSSO",
        "OBHBHBBBBBBHBBSSO",
        "OBHBBBHBBBBBHHSSO",
        "OBHBBBBBHBBBBBSSO",
        "OBBBBBBBBBBBBSSSO",
        ".OOOOOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 7, 12, SHEET, CM)
    return img


def peanut():
    """Roasted peanuts in their double-lobed shells."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SHELL_DK = (140, 100,  50, 255)
    SHELL_B  = (200, 160,  90, 255)
    SHELL_HI = (240, 210, 150, 255)
    OL       = ( 70,  50,  20, 255)
    # 3 peanuts arranged
    peanuts = [(11, 14), (16, 19), (21, 14)]
    for cx, cy in peanuts:
        PEA = [
            "..OOO..",
            ".OBHBO.",
            "OBHHBSO",
            "OBBBBSO",
            ".OBBSO.",
            "OBBBBSO",
            "OBHHBSO",
            ".OBHBO.",
            "..OOO..",
        ]
        CM = {'O': OL, 'B': SHELL_B, 'H': SHELL_HI, 'S': SHELL_DK}
        stamp(px, cx - 3, cy - 4, PEA, CM)
    return img


def bean_sprouts():
    """Pale bean sprouts — long thin strands with bean heads."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BEAN = (250, 240, 200, 255)
    BEAN_DK = (200, 180, 130, 255)
    STEM = (240, 235, 220, 255)
    OL = (100,  90,  60, 255)
    # 5 sprouts, each = bean head + curved stem
    sprouts = [
        (8, 14, 'right'),
        (12, 11, 'down'),
        (16, 14, 'right'),
        (20, 11, 'down'),
        (24, 14, 'right'),
    ]
    for sx, sy, _ in sprouts:
        # Bean head (round)
        put(px, sx, sy, BEAN_DK)
        put(px, sx + 1, sy, BEAN)
        put(px, sx + 1, sy + 1, BEAN_DK)
        # Stem curving down
        for i in range(8):
            put(px, sx + 1 + (i // 3), sy + 2 + i, STEM)
            put(px, sx + 1 + (i // 3), sy + 3 + i, OL)
    return img


def tamarind():
    """Tamarind paste — sticky brown pile."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (100,  50,  20, 255)
    B  = (170,  90,  40, 255)
    HI = (220, 140,  70, 255)
    OL = ( 50,  20,   8, 255)
    PASTE = [
        "....OOOOOO....",
        "..OOBBBBBBSO..",
        ".OBHBBBBBBBSSO",
        ".OBHHBBBBBBSSO",
        "OBHHBBBBBBBSSO",
        "OBHBBBBBBBBSSO",
        ".OBBBBBBBBBSSO",
        "..OOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 8, 14, PASTE, CM)
    # Glossy spots
    for x, y in [(11, 16), (16, 16), (20, 17)]:
        put(px, x, y, HI)
    return img


def kimchi():
    """Jar of red kimchi (fermented cabbage)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    JAR_B  = (200, 200, 200, 255)
    JAR_HI = (235, 240, 245, 255)
    KIM_DK = (130,  20,  10, 255)
    KIM_B  = (200,  40,  30, 255)
    KIM_HI = (240,  90,  60, 255)
    CABB_DK = (140,  70,  30, 255)
    CABB_B  = (200, 130,  60, 255)
    LID    = ( 70,  50,  20, 255)
    OL     = ( 30,  18,   8, 255)
    JAR = [
        ".OOOOOOOO.",
        "OLLLLLLLLO",
        "OOOOOOOOOO",
        "OBHHGGBBBO",
        "OBHKKKKKBO",
        "OBKKCCCKKO",
        "OBKCCCCCKO",
        "OBKKCCCKKO",
        "OBKKKCCKKO",
        "OBBKKKKKBO",
        ".OOOOOOOO.",
    ]
    CM = {'O': OL, 'L': LID, 'B': JAR_B, 'H': JAR_HI, 'K': KIM_B, 'C': CABB_B, 'G': JAR_B}
    stamp(px, 11, 11, JAR, CM)
    # Kimchi highlights (fermented juice glimmer)
    for x, y in [(14, 16), (17, 17), (15, 19)]:
        put(px, x, y, KIM_HI)
    return img


# ===========================================================
# CITRUS
# ===========================================================
def lime():
    """Lime — bright green sphere with leaf, slight stem."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 50, 100,  20, 255)
    B  = (110, 180,  40, 255)
    HI = (170, 230,  80, 255)
    PALE = (210, 250, 130, 255)
    LEAF_DK = ( 30,  80,  20, 255)
    LEAF_B  = ( 80, 140,  40, 255)
    OL   = ( 18,  44,  10, 255)
    LIME = [
        "..OOOOOOO..",
        ".OHHHHHBBSO.",
        "OHHHHBBBBSO",
        "OHHHBBBBBSO",
        "OHHBBBBBBSO",
        "OHBBBBBBSSO",
        "OBBBBBBSSSO",
        "OBBBBSSSSSO",
        ".OBBSSSSSO.",
        "..OOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 12, LIME, CM)
    # Leaf
    for x, y in [(16, 11), (17, 11), (15, 10)]:
        put(px, x, y, LEAF_B)
    put(px, 16, 10, LEAF_DK)
    return img


def lemon():
    """Lemon — yellow oval with bumpy texture."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180, 130,  20, 255)
    B  = (230, 190,  40, 255)
    HI = (250, 220,  80, 255)
    PALE = (255, 240, 130, 255)
    OL = ( 80,  50,  10, 255)
    LEM = [
        "...OOO...",
        "..OHHHO..",
        ".OHHHBHO.",
        "OHHHBBBSO",
        "OHHHBBBSO",
        "OHHBBBBSO",
        "OHBBBBBSO",
        "OBBBBBSSO",
        ".OBBBSSO.",
        "..OOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 12, LEM, CM)
    # Bumpy texture
    for x, y in [(14, 14), (17, 15), (15, 17)]:
        put(px, x, y, PALE)
    return img


# ===========================================================
# DAIRY
# ===========================================================
def yogurt():
    """Small bowl of yogurt — white creamy contents."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 70,  46,  24, 255)
    BOWL_B  = (138,  90,  46, 255)
    Y_DK    = (220, 220, 200, 255)
    Y_B     = (250, 250, 240, 255)
    Y_HI    = (255, 255, 255, 255)
    OL      = ( 30,  18,   8, 255)
    BOWL = [
        "OOOOOOOOOOOO",
        "OBHYYYYYYYBO",
        "OBYYYYYYYYBO",
        "OBYHHHYYYBBO",
        "OBYYHHYYYBSO",
        ".OBBYYYYBBO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'H': Y_HI, 'Y': Y_B, 'S': BOWL_DK}
    stamp(px, 10, 14, BOWL, CM)
    return img


def olive():
    """Single big olive (or 2-3)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  40,  20, 255)
    B  = ( 70,  90,  40, 255)
    HI = (120, 150,  70, 255)
    PIT = (150, 120,  60, 255)
    OL = ( 14,  20,  10, 255)
    # 2 olives — one with pit visible
    olives = [(11, 16), (20, 18)]
    for cx, cy in olives:
        OLI = [
            ".OOOO.",
            "OBHHBO",
            "OBHBSO",
            "OBBBSO",
            "OBBSSO",
            ".OOOO.",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
        stamp(px, cx - 2, cy - 3, OLI, CM)
    # Pit hole in first olive
    put(px, 11, 15, PIT)
    put(px, 12, 15, PIT)
    return img


# ===========================================================
# HERBS (FRESH BUNDLES)
# ===========================================================
def cilantro():
    """Cilantro/coriander bundle — small green leafy bunch."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 40,  90,  30, 255)
    B  = ( 90, 170,  60, 255)
    HI = (140, 220, 100, 255)
    STEM = (100, 140,  50, 255)
    OL = ( 14,  44,  10, 255)
    # Leafy top — clusters of small round leaves
    leaves = [
        (13, 10), (16, 10), (19, 10),
        (12, 13), (15, 12), (18, 13), (20, 12),
        (14, 15), (17, 15), (11, 16), (21, 15),
    ]
    for x, y in leaves:
        # 3×2 leaf
        put(px, x, y, OL)
        put(px, x + 1, y, OL)
        put(px, x + 2, y, OL)
        put(px, x, y - 1, B)
        put(px, x + 1, y - 1, HI)
        put(px, x + 2, y - 1, B)
    # Stems descending
    for y in range(17, 24):
        put(px, 15, y, STEM)
        put(px, 16, y, STEM)
        put(px, 17, y, STEM)
    return img


def basil():
    """Fresh basil bunch — broader leaves than cilantro."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  80,  30, 255)
    B  = ( 70, 140,  60, 255)
    HI = (120, 200,  90, 255)
    PALE = (170, 240, 120, 255)
    STEM = ( 90, 130,  50, 255)
    OL = ( 14,  40,  10, 255)
    # Big oval leaves arranged
    leaves = [
        (11, 11, 'left'),
        (16, 8, 'top'),
        (21, 11, 'right'),
        (13, 16, 'lowleft'),
        (19, 16, 'lowright'),
    ]
    for cx, cy, _ in leaves:
        LEAF = [
            ".OOOO.",
            "OBHHBO",
            "OPHHBO",
            "OBHBSO",
            ".OOOO.",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'P': PALE, 'S': DK}
        stamp(px, cx - 2, cy - 2, LEAF, CM)
    # Center stems
    for y in range(15, 24):
        put(px, 16, y, STEM)
        put(px, 17, y, STEM)
    return img


# ===========================================================
# BREADS
# ===========================================================
def tortilla():
    """Round flat tortilla."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180, 140,  70, 255)
    B  = (230, 200, 130, 255)
    HI = (250, 230, 180, 255)
    SPOT = (160, 120,  60, 255)
    OL = ( 80,  50,  20, 255)
    TOR = [
        "..OOOOOOOOOOOO..",
        ".OBHHHHHHHHHHBO.",
        "OBHHHBBBBBHHHBO",
        "OBHHBBBBBBBHHBO",
        "OBHBBBBBBBBBHBO",
        "OBHBBBBBBBBBHBO",
        "OBHHBBBBBBBHHBO",
        "OBHHHBBBBBHHHBO",
        ".OBHHHHHHHHHHBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI}
    stamp(px, 8, 11, TOR, CM)
    # Toasted spots
    for x, y in [(14, 14), (18, 15), (15, 17)]:
        put(px, x, y, SPOT)
    return img


def naan():
    """Naan bread — teardrop shape with charred spots."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180, 130,  60, 255)
    B  = (230, 190, 120, 255)
    HI = (250, 220, 170, 255)
    SPOT = ( 80,  40,  20, 255)
    OL = ( 80,  50,  20, 255)
    # Teardrop shape (wider at top, narrower at bottom)
    NAAN = [
        "...OOOOOO...",
        "..OBHHHHBO..",
        ".OBHHHHHHBO.",
        "OBHHHHHHHBO.",
        "OBHHHHHHHBO.",
        ".OBHHHHHBSO.",
        "..OBHHHBSO..",
        "...OBHBSO...",
        "....OBSO....",
        "....OOOO....",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 10, 11, NAAN, CM)
    # Char spots
    for x, y in [(14, 13), (17, 15), (15, 18)]:
        put(px, x, y, SPOT)
    return img


# ===========================================================
# SWEETS
# ===========================================================
def cocoa():
    """Cocoa block — dark chocolate brick."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 40,  20,  10, 255)
    B  = ( 90,  50,  20, 255)
    HI = (140,  80,  40, 255)
    SHEEN = (190, 120,  60, 255)
    OL = ( 20,  10,   5, 255)
    BLOCK = [
        ".OOOOOOOOOOOO.",
        "OHHHBBBBBBBBSO",
        "OHHHBBBBBBBBSO",
        "OHBBBBBBBBBSSO",
        "OBBBBBBBBBBSSO",
        "OBBBBBBBBBBSSO",
        "OBBBBBBBBBSSSO",
        ".OOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 9, 13, BLOCK, CM)
    # Score lines (chocolate squares)
    for x in range(12, 22, 3):
        for y in range(14, 21):
            put(px, x, y, DK)
    for y in range(16, 21, 3):
        for x in range(10, 23):
            put(px, x, y, DK)
    # Sheen
    put(px, 11, 14, SHEEN)
    put(px, 14, 15, SHEEN)
    return img


def apricot():
    """Apricot — small orange fruit with leaf."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180,  90,  30, 255)
    B  = (240, 150,  60, 255)
    HI = (255, 190, 100, 255)
    BLUSH = (220,  90,  50, 255)
    LEAF  = ( 80, 140,  50, 255)
    OL = ( 90,  50,  10, 255)
    FRUIT = [
        "..OOOOOO..",
        ".OBHHHBSO.",
        "OBHHHBBBSO",
        "OBHHBBBBSO",
        "OBHBBBBBSO",
        "OBBBBBBSSO",
        "OBBBBBSSSO",
        ".OBBBSSSO.",
        "..OOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 13, FRUIT, CM)
    # Red blush
    put(px, 13, 14, BLUSH)
    put(px, 14, 14, BLUSH)
    # Crease line
    for y in range(14, 21):
        put(px, 16, y, DK)
    # Leaf
    put(px, 16, 12, LEAF)
    put(px, 17, 12, LEAF)
    put(px, 15, 11, LEAF)
    return img


# ===========================================================
# DRIVER
# ===========================================================
JOBS = [
    ("proteins",   "bacon",        bacon),
    ("proteins",   "sausage",      sausage),
    ("proteins",   "shrimp",       shrimp),
    ("proteins",   "tofu",         tofu),
    ("asian",      "scallion",     scallion),
    ("asian",      "nori_sheet",   nori),
    ("asian",      "peanut",       peanut),
    ("asian",      "bean_sprouts", bean_sprouts),
    ("asian",      "tamarind",     tamarind),
    ("asian",      "kimchi",       kimchi),
    ("citrus",     "lime",         lime),
    ("citrus",     "lemon",        lemon),
    ("dairy",      "yogurt",       yogurt),
    ("dairy",      "olive",        olive),
    ("herbs",      "cilantro",     cilantro),
    ("herbs",      "basil_fresh",  basil),
    ("breads",     "tortilla",     tortilla),
    ("breads",     "naan",         naan),
    ("sweets",     "cocoa",        cocoa),
    ("sweets",     "apricot",      apricot),
]

if __name__ == "__main__":
    for folder, name, fn in JOBS:
        out = f"/home/sparky/ogrs/art/items/{folder}"
        os.makedirs(out, exist_ok=True)
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {folder}/{name}")
    print(f"\n=== Phase 3.5 complete: {len(JOBS)} ingredients ===")
