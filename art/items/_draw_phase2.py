#!/usr/bin/env python3
"""
Phase 2 — mid-tier ingredients (Tier-2 crops, pasta, spices, recipe add-ons).

GROUPS:
  A. Tier-2 crops (raw + cooked)  — 9 crops × 2 = 18 sprites
  B. Pasta variants               — 5 sprites
  C. Spices                       — 8 sprites
  D. Recipe add-ons               — 8 sprites
  E. Tier-2 seeds (loose handful) — 9 crops × 4 tiers = 36 sprites

Total: 75 sprites, all 32×32 with transparent background.
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
# A. TIER-2 CROPS
# ===========================================================

def mushroom_crop():
    """Brown-cap mushroom with white stem."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CAP_DK = ( 60,  30,  10, 255)
    CAP_B  = (130,  74,  30, 255)
    CAP_HI = (190, 130,  70, 255)
    STEM_B = (240, 220, 180, 255)
    STEM_S = (180, 160, 130, 255)
    GILL   = (110,  80,  50, 255)
    OL     = ( 30,  16,   8, 255)
    SHAPE = [
        "...OOOOOOO...",
        "..OBHHHHHBSO.",
        ".OBHHHHHHHBSO",
        "OBHHHHHHHHHBSO",
        "OBHHHHHHHHHBSO",
        ".OBBBBBBBBBSO.",
        "..OGGGGGGGGO..",
        "...OBBSBBBBO..",
        "....OBSBBBO...",
        "....OBSBBBO...",
        "....OBBBBBO...",
        ".....OOOOO....",
    ]
    CM = {'O': OL, 'B': CAP_B, 'H': CAP_HI, 'S': CAP_DK, 'G': GILL}
    stamp(px, 8, 8, SHAPE, CM)
    # Replace stem with light color
    for y in range(17, 21):
        for x in range(13, 19):
            if (x, y) in [(13, 17), (18, 17)]: continue
            put(px, x, y, STEM_B)
    for y in range(17, 21):
        put(px, 14, y, STEM_S)
    return img


def mushroom_cooked():
    """Pan-fried mushroom slices."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 60,  30,  10, 255)
    B  = (130,  74,  30, 255)
    HI = (180, 110,  50, 255)
    PALE = (220, 180, 130, 255)
    # 4 mushroom slices arranged
    slices = [(10, 14, 0), (16, 12, 0), (10, 20, 1), (17, 19, 1)]
    for cx, cy, flip in slices:
        SLICE = [
            ".OOOO.",
            "OBHHBO",
            "OBPHBO",
            "OBHHBO",
            ".OOOO.",
        ]
        CM = {'O': DK, 'B': B, 'H': HI, 'P': PALE}
        stamp(px, cx, cy, SLICE, CM)
    return img


def strawberry_crop():
    """Red strawberry with green stem leaves."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    R_DK = (120,  20,  20, 255)
    R_B  = (200,  40,  40, 255)
    R_HI = (240,  80,  70, 255)
    SEED = (240, 220,   0, 255)
    GR   = ( 40,  90,  20, 255)
    GR_HI= (110, 170,  60, 255)
    OL   = ( 60,   8,   8, 255)
    BERRY = [
        "..GGGGGG..",
        ".GHGGGGHG.",
        "OOOOOOOOOO",
        "OBHHBBBBSO",
        "OBHHBBBBSO",
        "OBHBSBBSSO",
        "OBBBSBSSSO",
        ".OBBBBSSO.",
        ".OBBBSSO..",
        "..OBSSO...",
        "...OSO....",
        "....O.....",
    ]
    CM = {'O': OL, 'B': R_B, 'H': R_HI, 'S': R_DK, 'G': GR}
    stamp(px, 11, 9, BERRY, CM)
    # Replace some greens with highlight
    for x, y in [(13, 9), (15, 10), (18, 10)]:
        put(px, x, y, GR_HI)
    # Seeds (yellow specks)
    for x, y in [(14, 13), (17, 13), (15, 15), (19, 15), (16, 17)]:
        put(px, x, y, SEED)
    return img


def strawberry_cooked():
    """Strawberry jam jar."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    JAR_DK = ( 70,  90, 110, 255)
    JAR_B  = (150, 180, 210, 255)
    JAR_HI = (210, 230, 245, 255)
    JAM_DK = (120,  20,  30, 255)
    JAM_B  = (190,  40,  50, 255)
    JAM_HI = (230,  80,  90, 255)
    LID    = (180,  40,  40, 255)
    OL     = ( 30,  40,  60, 255)
    JAR = [
        ".OOOOOOOO.",
        "OLLLLLLLLO",
        "OOOOOOOOOO",
        "OBHHBBBBBO",
        "OBHHJJJJJO",
        "OBHJJJJJJO",
        "OBJJJJJJJO",
        "OBJJJJJJJO",
        "OBBJJJJJJO",
        "OBBBBBBBBO",
        ".OOOOOOOO.",
    ]
    CM = {'O': OL, 'B': JAR_B, 'H': JAR_HI, 'L': LID, 'J': JAM_B}
    stamp(px, 11, 11, JAR, CM)
    # Jam highlight chunks
    for x, y in [(14, 17), (17, 18), (15, 19)]:
        put(px, x, y, JAM_HI)
    return img


def blueberry_crop():
    """Cluster of blueberries on a tiny stem."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  30,  80, 255)
    B  = ( 70,  70, 160, 255)
    HI = (130, 140, 220, 255)
    OL = ( 18,  18,  44, 255)
    GR = ( 60, 110,  40, 255)
    # 5 berries in a cluster
    berries = [(13, 16), (19, 14), (16, 18), (22, 18), (15, 22)]
    for cx, cy in berries:
        cells = {
            (-1, -1): OL, (0, -1): OL, (1, -1): OL,
            (-2, 0): OL, (-1, 0): HI, (0, 0): HI, (1, 0): B, (2, 0): OL,
            (-2, 1): OL, (-1, 1): B, (0, 1): B, (1, 1): DK, (2, 1): OL,
            (-1, 2): OL, (0, 2): OL, (1, 2): OL,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
    # Stem
    for y in (10, 11, 12, 13):
        put(px, 16, y, GR)
    return img


def blueberry_cooked():
    """Blueberry pie slice."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CRUST_DK = ( 90,  56,  20, 255)
    CRUST_B  = (180, 130,  60, 255)
    CRUST_HI = (230, 180, 100, 255)
    FILL_DK  = ( 30,  30,  80, 255)
    FILL_B   = ( 70,  70, 160, 255)
    OL       = ( 40,  20,   8, 255)
    PIE = [
        "..OOOOOOOO..",
        ".OBHBBBBHBO.",
        "OBHHBBBBBHBO",
        "OBFFFFFFFFBO",
        "OBFFFFFFFFBO",
        ".OBFFFFFFBO.",
        "..OBBBBBBO..",
        "...OOOOOO...",
    ]
    CM = {'O': OL, 'B': CRUST_B, 'H': CRUST_HI, 'F': FILL_B}
    stamp(px, 10, 12, PIE, CM)
    # Filling chunks (blueberries visible in filling)
    for x, y in [(13, 15), (16, 15), (19, 15), (14, 16), (18, 16)]:
        put(px, x, y, FILL_DK)
    return img


def hotpepper_crop():
    """Red chili pepper, curving down."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    R_DK = (130,  10,   8, 255)
    R_B  = (210,  30,  20, 255)
    R_HI = (250,  80,  50, 255)
    GR   = ( 50, 110,  30, 255)
    OL   = ( 60,   8,   4, 255)
    PEP = [
        "...OOO.",
        "..OGGO.",
        ".OOGOO.",
        "OBHBO..",
        "OBHBSO.",
        "OBHBBSO",
        ".OBHBSO",
        ".OBHBSO",
        "..OBHSO",
        "...OBSO",
        "....OSO",
        "....OOO",
    ]
    CM = {'O': OL, 'B': R_B, 'H': R_HI, 'S': R_DK, 'G': GR}
    stamp(px, 12, 9, PEP, CM)
    return img


def hotpepper_cooked():
    """Hot sauce bottle."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GLASS_DK = ( 60,  60,  60, 255)
    GLASS_B  = (200, 200, 200, 255)
    SAUCE_DK = (130,  10,   8, 255)
    SAUCE_B  = (210,  30,  20, 255)
    SAUCE_HI = (250,  80,  50, 255)
    LABEL    = (240, 220,  60, 255)
    OL       = ( 30,  18,   8, 255)
    BOTTLE = [
        "...OOOO..",
        "...OBBOO.",
        "...OBBOO.",
        "..OOBBOO.",
        "..OLLLLO.",
        "..OLBBLO.",
        "..OLBBLO.",
        "..OBSSBO.",
        "..OBSSBO.",
        "..OBSSBO.",
        "..OBBBBO.",
        "..OOOOOO.",
    ]
    CM = {'O': OL, 'B': SAUCE_B, 'S': SAUCE_HI, 'L': LABEL}
    stamp(px, 12, 10, BOTTLE, CM)
    return img


def rice_crop():
    """Raw rice — sack with grains."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SACK_B = (180, 150,  90, 255)
    SACK_S = (130, 100,  50, 255)
    SACK_HI = (220, 190, 130, 255)
    GRAIN  = (250, 245, 230, 255)
    GR_DK  = (200, 190, 170, 255)
    OL     = ( 60,  40,  20, 255)
    SACK = [
        "..OOOOOOO..",
        ".OBHHBBSSO.",
        "OBHHBBBSSO.",
        "OBHBBBBSSO.",
        "OBHBBBBSSO.",
        "OBBBBBBSSO.",
        "OBBBBBSSSO.",
        ".OBBBBSSO..",
        "..OOOOOOO..",
    ]
    CM = {'O': OL, 'B': SACK_B, 'H': SACK_HI, 'S': SACK_S}
    stamp(px, 10, 14, SACK, CM)
    # Rice grains spilling out top
    for x, y in [(13, 11), (15, 10), (17, 10), (19, 11), (14, 12), (18, 12), (16, 11)]:
        put(px, x, y, GRAIN)
    for x, y in [(13, 13), (19, 13)]:
        put(px, x, y, GR_DK)
    return img


def rice_cooked():
    """Bowl of cooked rice."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 70,  46,  24, 255)
    BOWL_B  = (138,  90,  46, 255)
    RICE_DK = (200, 190, 170, 255)
    RICE_B  = (250, 245, 230, 255)
    OL      = ( 30,  16,   8, 255)
    # Rice mound
    for y in range(14, 19):
        for x in range(11 + (y - 14), 22 - (y - 14)):
            put(px, x, y, RICE_B)
    # Grain texture dots
    for x, y in [(13, 14), (15, 14), (17, 14), (19, 14),
                 (13, 16), (15, 16), (17, 16), (19, 16),
                 (14, 17), (16, 17), (18, 17)]:
        put(px, x, y, RICE_DK)
    # Bowl
    BOWL = [
        "OOOOOOOOOO",
        "OBBBBBBBBO",
        ".OOBBBBOO.",
        "..OOOOOO..",
    ]
    CM = {'O': BOWL_DK, 'B': BOWL_B}
    stamp(px, 11, 18, BOWL, CM)
    return img


def eggplant_crop():
    """Dark-purple eggplant."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  10,  50, 255)
    B  = ( 70,  30, 100, 255)
    HI = (130,  80, 170, 255)
    GR = ( 60, 110,  40, 255)
    GR_HI = (110, 170, 60, 255)
    OL = ( 18,   6,  30, 255)
    EGG = [
        "...GGGGG...",
        "...GHHHG...",
        "..OOGGGOO..",
        ".OBHHBBBSO.",
        "OBHHBBBBBSO",
        "OBHHBBBBBSO",
        "OBHBBBBBSSO",
        "OBBBBBBBSSO",
        "OBBBBBBSSSO",
        ".OBBBSSSSO.",
        "..OBBSSSO..",
        "...OOOOO...",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK, 'G': GR}
    stamp(px, 10, 10, EGG, CM)
    # Highlight green leaves
    for x, y in [(13, 11), (15, 11), (17, 11)]:
        put(px, x, y, GR_HI)
    return img


def eggplant_cooked():
    """Eggplant parmesan — sliced rounds."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PURPLE_DK = ( 70,  30, 100, 255)
    PURPLE_B  = (130,  80, 170, 255)
    FLESH     = (240, 230, 200, 255)
    CHEESE    = (250, 220,  80, 255)
    OL        = ( 30,  10,  50, 255)
    rounds = [(11, 14), (18, 14), (15, 19), (22, 18)]
    for cx, cy in rounds:
        cells = {
            (-2, -1): OL, (-1, -1): PURPLE_B, (0, -1): PURPLE_B, (1, -1): OL,
            (-2, 0):  OL, (-1, 0):  FLESH,    (0, 0):  FLESH,    (1, 0):  OL,
            (-2, 1):  OL, (-1, 1):  PURPLE_DK,(0, 1):  PURPLE_B, (1, 1):  OL,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
        # Cheese drizzle
        put(px, cx, cy - 1, CHEESE)
    return img


def zucchini_crop():
    """Green zucchini squash."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 40,  80,  30, 255)
    B  = ( 80, 140,  60, 255)
    HI = (130, 200,  80, 255)
    PALE = (180, 230, 130, 255)
    STEM = ( 80, 100,  40, 255)
    OL = ( 18,  44,  10, 255)
    # Horizontal zucchini
    Z = [
        ".OOOOOOOOOOOOO.",
        "OHHBBBBBBBBBSSO",
        "OPHBBBBBBBBSSSO",
        "OPHBBBBBBBSSSSO",
        "OHHBBBBBBBSSSSO",
        ".OOOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'P': PALE, 'S': DK}
    stamp(px, 8, 13, Z, CM)
    # Stem at left end
    for y in (15, 16):
        put(px, 7, y, STEM)
        put(px, 6, y, OL)
    return img


def zucchini_cooked():
    """Zucchini fritters — golden disks."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GOLD_DK = (140,  90,  30, 255)
    GOLD_B  = (210, 160,  60, 255)
    GOLD_HI = (240, 200, 110, 255)
    GREEN   = ( 80, 140,  60, 255)
    OL      = ( 60,  40,  10, 255)
    fritters = [(11, 14), (19, 14), (15, 19), (22, 19)]
    for cx, cy in fritters:
        cells = {
            (-2, -1): OL, (-1, -1): GOLD_HI, (0, -1): GOLD_B, (1, -1): OL,
            (-2, 0): OL, (-1, 0): GOLD_B, (0, 0): GOLD_HI, (1, 0): OL,
            (-2, 1): OL, (-1, 1): GOLD_DK, (0, 1): GOLD_B, (1, 1): OL,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
        # Tiny green fleck
        put(px, cx, cy, GREEN)
    return img


def spinach_crop():
    """Leafy green spinach bunch."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 20,  60,  20, 255)
    B  = ( 50, 120,  40, 255)
    HI = ( 90, 180,  70, 255)
    PALE = (140, 220, 100, 255)
    STEM = (150, 120,  50, 255)
    OL = ( 10,  30,   8, 255)
    # 5 leaves arranged
    leaves = [
        (11, 13, 'left'),
        (16, 11, 'center'),
        (21, 13, 'right'),
        (13, 19, 'lowleft'),
        (19, 19, 'lowright'),
    ]
    for cx, cy, _ in leaves:
        LEAF = [
            ".OOOOO.",
            "OBHHBSO",
            "OPHHBSO",
            "OPHBBSO",
            "OBHBSSO",
            ".OBSSO.",
            "..OOO..",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'P': PALE, 'S': DK}
        stamp(px, cx, cy, LEAF, CM)
    # Center stem cluster
    for y in range(15, 22):
        put(px, 16, y, STEM)
    return img


def spinach_cooked():
    """Wilted spinach pile."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 20,  60,  20, 255)
    B  = ( 50, 110,  40, 255)
    HI = ( 80, 150,  60, 255)
    OL = ( 10,  30,   8, 255)
    # Wilted clumps
    for y in range(16, 22):
        for x in range(10 + (y - 16), 24 - (y - 16)):
            put(px, x, y, B if (x + y) % 3 != 0 else HI)
    # Outline
    for x in range(10, 24):
        put(px, x, 15, OL)
    for x in (10, 14, 18, 22):
        put(px, x, 22, OL)
    # Texture lines
    for x in [12, 16, 20]:
        for y in [17, 19]:
            put(px, x, y, DK)
    return img


def pumpkin_crop():
    """Orange pumpkin with stem."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    O_DK = (160,  70,  10, 255)
    O_B  = (230, 120,  30, 255)
    O_HI = (250, 170,  70, 255)
    STEM_DK = ( 50,  80,  20, 255)
    STEM_B  = ( 90, 140,  40, 255)
    OL   = ( 60,  20,   8, 255)
    PUM = [
        "....SS....",
        "...SBBS...",
        ".OOOOOOOO.",
        "OBHBSBSBBO",
        "OBHBSBSBBO",
        "OBHBBSBBSO",
        "OBHBSBSBSO",
        "OBHBBSBBSO",
        "OBHBSBSBSO",
        "OBBBSBSBSO",
        ".OOOOOOOO.",
    ]
    CM = {'O': OL, 'B': O_B, 'H': O_HI, 'S': O_DK}
    stamp(px, 10, 11, PUM, CM)
    # Stem (green)
    for x, y in [(15, 11), (16, 11), (15, 12), (16, 12)]:
        put(px, x, y, STEM_B)
    put(px, 15, 10, STEM_DK)
    put(px, 16, 10, STEM_DK)
    return img


def pumpkin_cooked():
    """Pumpkin pie slice (existing in vanilla but redrawn)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CRUST_B = (200, 150,  80, 255)
    CRUST_HI= (240, 200, 130, 255)
    CRUST_DK= (130,  80,  30, 255)
    FILL    = (200,  90,  20, 255)
    FILL_HI = (250, 150,  60, 255)
    OL      = ( 50,  20,   8, 255)
    PIE = [
        "..OOOOOOOOOO..",
        ".OBHBBBBBBBHBO.",
        "OBHHFFFFFFHHBO",
        "OBFFFFFFFFFBSO",
        "OBFFFFFFFFFBSO",
        ".OBBFFFFFBBSO.",
        "..OBBBBBBBSO..",
        "...OOOOOOOO...",
    ]
    CM = {'O': OL, 'B': CRUST_B, 'H': CRUST_HI, 'S': CRUST_DK, 'F': FILL}
    stamp(px, 9, 12, PIE, CM)
    # Highlight on filling
    for x, y in [(14, 15), (17, 15), (15, 16)]:
        put(px, x, y, FILL_HI)
    return img


# ===========================================================
# B. PASTA VARIANTS
# ===========================================================

PASTA_DK = (160, 120,  60, 255)
PASTA_B  = (220, 190, 130, 255)
PASTA_HI = (250, 230, 180, 255)
PASTA_OL = ( 80,  60,  30, 255)


def spaghetti():
    """Curly spaghetti noodles."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Wavy lines crossing the canvas
    strands = [
        # (start_x, start_y, freq, amp)
        (4, 12), (4, 16), (4, 20), (4, 24), (4, 14), (4, 18), (4, 22),
    ]
    for sx, sy in strands:
        for dx in range(24):
            wave = math.sin((sx + dx) * 0.6) * 1.5
            y = sy + int(round(wave))
            put(px, sx + dx, y, PASTA_B)
            put(px, sx + dx, y + 1, PASTA_DK)
            if dx % 4 == 0:
                put(px, sx + dx, y, PASTA_HI)
    return img


def penne():
    """Penne tubes — angled tubes."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Diagonal tubes
    tubes = [(8, 14), (16, 13), (12, 19), (20, 19), (10, 23)]
    for sx, sy in tubes:
        # Tube body — slanted parallelogram
        for i in range(8):
            x1 = sx + i
            y1 = sy + i // 2
            put(px, x1, y1, PASTA_DK)
            put(px, x1, y1 + 1, PASTA_B)
            put(px, x1, y1 + 2, PASTA_B)
            put(px, x1, y1 + 3, PASTA_HI)
            put(px, x1, y1 + 4, PASTA_DK)
        # Hollow ends
        put(px, sx, sy + 1, PASTA_DK)
        put(px, sx, sy + 2, PASTA_DK)
        put(px, sx + 7, sy + 4, PASTA_DK)
    return img


def lasagna_sheets():
    """Flat lasagna pasta sheets."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # 3 stacked rectangles representing flat sheets
    sheets = [(8, 11), (10, 17), (8, 23)]
    for sx, sy in sheets:
        # Sheet body
        for y in range(5):
            for x in range(16):
                if y == 0 or y == 4 or x == 0 or x == 15:
                    put(px, sx + x, sy + y, PASTA_OL)
                elif y == 1:
                    put(px, sx + x, sy + y, PASTA_HI)
                else:
                    put(px, sx + x, sy + y, PASTA_B)
        # Wavy edge texture
        for x in range(2, 14, 2):
            put(px, sx + x, sy + 4, PASTA_DK)
    return img


def ravioli():
    """Square ravioli pillows."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # 4 ravioli arranged
    pillows = [(8, 10), (18, 10), (8, 20), (18, 20)]
    for cx, cy in pillows:
        # 6×5 pillow with crimped edges
        RAV = [
            ".OOOOO.",
            "OBHHHBO",
            "OHBBHBO",
            "OBBBBBO",
            ".OOOOO.",
        ]
        CM = {'O': PASTA_OL, 'B': PASTA_B, 'H': PASTA_HI}
        stamp(px, cx, cy, RAV, CM)
        # Crimped texture
        for x in (cx + 1, cx + 3, cx + 5):
            put(px, x, cy, PASTA_DK)
            put(px, x, cy + 4, PASTA_DK)
    return img


def gnocchi():
    """Small dumpling-like gnocchi."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Cluster of small oval dumplings
    dumplings = [
        (10, 14), (15, 13), (20, 14),
        (12, 19), (17, 18), (22, 19),
        (10, 24), (15, 23), (20, 24),
    ]
    for cx, cy in dumplings:
        cells = {
            (-1, -1): PASTA_OL, (0, -1): PASTA_OL, (1, -1): PASTA_OL,
            (-2, 0): PASTA_OL, (-1, 0): PASTA_HI, (0, 0): PASTA_B, (1, 0): PASTA_B, (2, 0): PASTA_OL,
            (-1, 1): PASTA_OL, (0, 1): PASTA_OL, (1, 1): PASTA_OL,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
        # Ridge marks
        put(px, cx - 1, cy, PASTA_DK)
    return img


# ===========================================================
# C. SPICES
# ===========================================================

def spice_jar(label_color, powder_color, label_dk=None, powder_dk=None):
    """Reusable spice jar with colored label + powder visible inside."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GLASS_O = ( 50,  50,  60, 255)
    GLASS_B = (180, 200, 220, 255)
    GLASS_HI= (230, 240, 250, 255)
    LID     = ( 80,  60,  40, 255)
    LID_HI  = (140, 110,  70, 255)
    OL      = ( 30,  20,  10, 255)
    if powder_dk is None: powder_dk = tuple(max(0, c - 40) for c in powder_color[:3]) + (255,)

    JAR = [
        "..OOOOOO..",
        ".OLLLLLLO.",
        "OOLHLLLLOO",
        "OBHHGGBBBO",   # G = glass
        "OBHGPPPGBO",   # P = powder
        "OBHPPPPPBO",
        "OBPPPPPPBO",
        "OBPPPPPPBO",
        ".OBBBBBBO.",
        "..OOOOOO..",
    ]
    CM = {'O': OL, 'L': LID, 'H': LID_HI, 'G': GLASS_B, 'B': GLASS_O, 'P': powder_color}
    stamp(px, 11, 11, JAR, CM)
    # Label band
    for x in range(13, 19):
        put(px, x, 14, label_color)
        put(px, x, 15, label_color)
    return img


# 8 different spices, each with distinct color
def spice_salt():       return spice_jar((240, 240, 240, 255), (250, 250, 250, 255))
def spice_pepper():     return spice_jar(( 30,  30,  30, 255), ( 50,  50,  50, 255))
def spice_paprika():    return spice_jar((180,  40,  20, 255), (220,  70,  30, 255))
def spice_cumin():      return spice_jar((140,  90,  30, 255), (180, 130,  60, 255))
def spice_curry():      return spice_jar((200, 160,  20, 255), (240, 200,  60, 255))
def spice_garam():      return spice_jar((100,  50,  20, 255), (160,  90,  40, 255))
def spice_oregano():    return spice_jar(( 60, 120,  40, 255), (100, 160,  60, 255))
def spice_basil():      return spice_jar(( 40, 110,  30, 255), ( 90, 170,  60, 255))


# ===========================================================
# D. RECIPE ADD-ONS
# ===========================================================

def olive_oil():
    """Small glass bottle of golden olive oil."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GLASS_DK = ( 40,  60,  40, 255)
    GLASS_B  = (140, 200, 130, 255)
    OIL_DK   = (160, 120,  20, 255)
    OIL_B    = (220, 180,  60, 255)
    OIL_HI   = (250, 220, 130, 255)
    CORK     = ( 90,  60,  20, 255)
    OL       = ( 20,  30,  20, 255)
    BOTTLE = [
        "...CC..",
        "...CC..",
        "..OOOO.",
        "..OGGOO",
        "..OOGOO",
        "..OGGOO",
        "..OGOOO",
        ".OOOOOO",
        "OGOOIIO",
        "OGOIIIO",
        "OGIIIIO",
        "OGIIIBO",
        "OGIIBBO",
        "OGBBBBO",
        ".OOOOOO",
    ]
    CM = {'O': OL, 'G': GLASS_B, 'C': CORK, 'I': OIL_HI, 'B': OIL_B}
    stamp(px, 11, 7, BOTTLE, CM)
    return img


def beet():
    """Red beet root with green tops."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 90,  10,  30, 255)
    B  = (150,  20,  60, 255)
    HI = (200,  40,  90, 255)
    GR_DK = ( 30,  80,  20, 255)
    GR_B  = ( 80, 140,  50, 255)
    OL = ( 30,   8,  10, 255)
    # Beet root (round)
    ROOT = [
        "..OOOOOO..",
        ".OBHHBBSO.",
        "OBHHHBBBSO",
        "OBHHBBBBSO",
        "OBHBBBBBSO",
        "OBBBBBBSSO",
        ".OBBBBSSO.",
        "..OBBSSO..",
        "...OSSO...",
        "....OO....",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 14, ROOT, CM)
    # Greens
    for x, y in [(13, 11), (15, 10), (17, 10), (19, 11)]:
        put(px, x, y, GR_B)
    for x, y in [(14, 11), (16, 9), (18, 11)]:
        put(px, x, y, GR_DK)
    return img


def milk():
    """White milk jug."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    JUG_DK = (170, 180, 190, 255)
    JUG_B  = (230, 240, 245, 255)
    JUG_HI = (255, 255, 255, 255)
    HANDLE = (200, 210, 220, 255)
    OL     = ( 60,  70,  80, 255)
    JUG = [
        "..OOOO..",
        ".OBHHBO.",
        "OBHHBBO.",
        "OBBBBBOOO",
        "OBHHBBBHO",
        "OBHBBBHHO",
        "OBHHBBBBO",
        "OBBBBBBBO",
        "OBBBBBBBO",
        "OBBBBBBSO",
        ".OOOOOOO.",
    ]
    CM = {'O': OL, 'B': JUG_B, 'H': JUG_HI, 'S': JUG_DK}
    stamp(px, 11, 10, JUG, CM)
    return img


def butter():
    """Yellow butter stick."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    B_DK = (200, 160,  30, 255)
    B_B  = (250, 210,  80, 255)
    B_HI = (255, 235, 140, 255)
    OL   = (130,  90,  10, 255)
    STICK = [
        ".OOOOOOOOOOO.",
        "OBHHBBBBBBBSO",
        "OBHHBBBBBBSSO",
        "OBHBBBBBBSSSO",
        "OBHBBBBBBSSSO",
        "OBBBBBBBSSSSO",
        ".OOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B_B, 'H': B_HI, 'S': B_DK}
    stamp(px, 9, 14, STICK, CM)
    return img


def honey():
    """Honey jar with honeycomb pattern."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    JAR_DK = ( 80,  60,  20, 255)
    JAR_B  = (200, 200, 200, 255)
    HONEY_DK = (180, 120,  20, 255)
    HONEY_B  = (240, 180,  40, 255)
    HONEY_HI = (255, 220,  90, 255)
    LID    = (120,  80,  20, 255)
    OL     = ( 30,  20,   8, 255)
    JAR = [
        "..OOOOOO..",
        ".OLLLLLLO.",
        "OOLHLLLLOO",
        "OBHHGGBBBO",
        "OBHHHHHBBO",
        "OBHHHBBBBO",
        "OBHHBBBBSO",
        "OBHBBBBSSO",
        "OBBBBBSSSO",
        ".OBBBBSSO.",
        "..OOOOOO..",
    ]
    CM = {'O': OL, 'L': LID, 'B': HONEY_B, 'H': HONEY_HI, 'S': HONEY_DK, 'G': HONEY_B}
    stamp(px, 11, 10, JAR, CM)
    return img


def wine():
    """Wine bottle — dark green glass."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GLASS_DK = ( 20,  50,  30, 255)
    GLASS_B  = ( 40, 100,  60, 255)
    GLASS_HI = ( 80, 150,  90, 255)
    LABEL    = (210, 200, 180, 255)
    LABEL_DK = (130, 110,  80, 255)
    CORK     = ( 90,  60,  20, 255)
    OL       = ( 10,  20,  10, 255)
    BOTTLE = [
        "...CC..",
        "..OOOO.",
        "..OGGO.",
        "..OGGO.",
        "..OGGO.",
        "..OGGO.",
        "..OOOO.",
        "..OGGO.",
        "..OGGO.",
        "..OLLO.",
        "..OLLO.",
        "..OGGO.",
        "..OGGO.",
        "..OOOO.",
    ]
    CM = {'O': OL, 'G': GLASS_B, 'C': CORK, 'L': LABEL}
    stamp(px, 12, 7, BOTTLE, CM)
    # Bottle highlight
    for y in range(9, 19):
        put(px, 13, y, GLASS_HI)
    return img


def mustard():
    """Mustard jar — bright yellow."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    M_DK = (180, 130,  20, 255)
    M_B  = (240, 200,  40, 255)
    M_HI = (255, 230,  90, 255)
    JAR_B = (200, 200, 200, 255)
    LID  = ( 80,  60,  30, 255)
    OL   = ( 30,  20,   8, 255)
    JAR = [
        "..OOOOOO..",
        ".OLLLLLLO.",
        "OOLLLLLLOO",
        "OBHHHHHBBO",
        "OBHHMMHHBO",
        "OBHMMMMHBO",
        "OBHMMMMHBO",
        "OBHHMMHHBO",
        "OBHHHHHHBO",
        "OBBBBBBBBO",
        ".OOOOOOOO.",
    ]
    CM = {'O': OL, 'L': LID, 'B': JAR_B, 'H': M_B, 'M': M_HI}
    stamp(px, 11, 10, JAR, CM)
    return img


def vinegar():
    """Vinegar bottle — clear with amber liquid."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GLASS_DK = ( 60,  60,  60, 255)
    GLASS_B  = (200, 200, 200, 255)
    LIQ_DK   = (140,  80,  20, 255)
    LIQ_B    = (200, 130,  50, 255)
    CORK     = ( 90,  60,  20, 255)
    OL       = ( 20,  20,  20, 255)
    BOTTLE = [
        "...CC..",
        "..OOOO.",
        "..OGGO.",
        "..OGGO.",
        ".OOGGOO",
        ".OGGGGO",
        ".OGGGGO",
        ".OGLLGO",
        ".OGLLGO",
        ".OLLLLO",
        ".OLLLLO",
        ".OLLLLO",
        ".OOOOOO",
    ]
    CM = {'O': OL, 'G': GLASS_B, 'L': LIQ_B, 'C': CORK}
    stamp(px, 12, 8, BOTTLE, CM)
    return img


# ===========================================================
# E. TIER-2 SEEDS (loose handfuls — v2 style)
# ===========================================================

# Per-crop seed visual: shape + palette
def shape_round_seed(px, x, y, dk, base, hi):
    put(px, x, y - 1, dk); put(px, x - 1, y, dk); put(px, x, y, hi); put(px, x + 1, y, base); put(px, x, y + 1, dk)


def shape_oval_seed(px, x, y, dk, base, hi):
    put(px, x - 1, y, dk); put(px, x, y, hi); put(px, x + 1, y, base); put(px, x, y + 1, dk)


def shape_drop_seed(px, x, y, dk, base, hi):
    put(px, x, y - 1, dk); put(px, x - 1, y, base); put(px, x, y, hi); put(px, x + 1, y, dk); put(px, x, y + 1, dk)


def shape_long_seed(px, x, y, dk, base, hi):
    """Long rice-grain seed."""
    put(px, x - 1, y, dk); put(px, x, y, hi); put(px, x + 1, y, base); put(px, x + 2, y, dk)


TIER2_CROPS = {
    'mushroom':   {'shape': shape_round_seed, 'palette': (( 60,  30,  10), (130,  74,  30), (190, 130,  70))},
    'strawberry': {'shape': shape_round_seed, 'palette': ((140,  20,  20), (200,  40,  40), (240,  80,  70))},
    'blueberry':  {'shape': shape_round_seed, 'palette': (( 30,  30,  80), ( 70,  70, 160), (130, 140, 220))},
    'hotpepper':  {'shape': shape_drop_seed,  'palette': ((130,  10,   8), (210,  30,  20), (250,  80,  50))},
    'rice':       {'shape': shape_long_seed,  'palette': ((200, 190, 170), (240, 235, 220), (255, 250, 240))},
    'eggplant':   {'shape': shape_round_seed, 'palette': (( 30,  10,  50), ( 70,  30, 100), (130,  80, 170))},
    'zucchini':   {'shape': shape_oval_seed,  'palette': (( 40,  80,  30), ( 80, 140,  60), (130, 200,  80))},
    'spinach':    {'shape': shape_round_seed, 'palette': (( 20,  60,  20), ( 50, 120,  40), ( 90, 180,  70))},
    'pumpkin':    {'shape': shape_drop_seed,  'palette': ((160,  70,  10), (230, 120,  30), (250, 170,  70))},
}

CX, CY = 16, 16
TIER1_POS = [(0, 0)]
TIER2_POS = [(-2, -3), (3, -2), (-3, 2), (2, 3), (0, 0)]
TIER3_POS = [(-4, -5), (0, -5), (4, -5), (-5, -2), (-2, -2), (2, -2), (5, -2),
             (-4, 1), (0, 1), (4, 1), (-3, 4), (3, 4), (-1, 6), (2, 6), (0, 3)]
TIER4_POS = [(-8, -8), (-4, -8), (0, -8), (4, -8), (8, -8),
             (-9, -5), (-5, -5), (-1, -5), (3, -5), (7, -5),
             (-10, -2), (-6, -2), (-2, -2), (2, -2), (6, -2), (10, -2),
             (-9, 2), (-5, 2), (-1, 2), (3, 2), (7, 2),
             (-10, 6), (-6, 6), (-2, 6), (2, 6), (6, 6), (10, 6),
             (-8, 9), (-4, 9), (0, 9), (4, 9), (8, 9)]


def draw_tier2_seed(crop, tier):
    positions = {1: TIER1_POS, 2: TIER2_POS, 3: TIER3_POS, 4: TIER4_POS}[tier]
    cfg = TIER2_CROPS[crop]
    shape_fn = cfg['shape']
    dk, base, hi = cfg['palette']
    dk = (*dk, 255); base = (*base, 255); hi = (*hi, 255)
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    for (dx, dy) in positions:
        shape_fn(px, CX + dx, CY + dy, dk, base, hi)
    return img


# ===========================================================
# DRIVER
# ===========================================================
JOBS = [
    # A — Tier-2 crops
    ("veg_mushroom",    "mushroom_crop",    mushroom_crop),
    ("veg_mushroom",    "mushroom_cooked",  mushroom_cooked),
    ("veg_strawberry",  "strawberry_crop",  strawberry_crop),
    ("veg_strawberry",  "strawberry_cooked",strawberry_cooked),
    ("veg_blueberry",   "blueberry_crop",   blueberry_crop),
    ("veg_blueberry",   "blueberry_cooked", blueberry_cooked),
    ("veg_hotpepper",   "hotpepper_crop",   hotpepper_crop),
    ("veg_hotpepper",   "hotpepper_cooked", hotpepper_cooked),
    ("veg_rice",        "rice_crop",        rice_crop),
    ("veg_rice",        "rice_cooked",      rice_cooked),
    ("veg_eggplant",    "eggplant_crop",    eggplant_crop),
    ("veg_eggplant",    "eggplant_cooked",  eggplant_cooked),
    ("veg_zucchini",    "zucchini_crop",    zucchini_crop),
    ("veg_zucchini",    "zucchini_cooked",  zucchini_cooked),
    ("veg_spinach",     "spinach_crop",     spinach_crop),
    ("veg_spinach",     "spinach_cooked",   spinach_cooked),
    ("veg_pumpkin",     "pumpkin_crop",     pumpkin_crop),
    ("veg_pumpkin",     "pumpkin_cooked",   pumpkin_cooked),
    # B — Pasta
    ("pasta",           "spaghetti",        spaghetti),
    ("pasta",           "penne",            penne),
    ("pasta",           "lasagna",          lasagna_sheets),
    ("pasta",           "ravioli",          ravioli),
    ("pasta",           "gnocchi",          gnocchi),
    # C — Spices
    ("spices",          "salt",             spice_salt),
    ("spices",          "pepper",           spice_pepper),
    ("spices",          "paprika",          spice_paprika),
    ("spices",          "cumin",            spice_cumin),
    ("spices",          "curry_powder",     spice_curry),
    ("spices",          "garam_masala",     spice_garam),
    ("spices",          "oregano",          spice_oregano),
    ("spices",          "basil",            spice_basil),
    # D — Recipe add-ons
    ("addons",          "olive_oil",        olive_oil),
    ("addons",          "beet",             beet),
    ("addons",          "milk",             milk),
    ("addons",          "butter",           butter),
    ("addons",          "honey",            honey),
    ("addons",          "wine",             wine),
    ("addons",          "mustard",          mustard),
    ("addons",          "vinegar",          vinegar),
]


if __name__ == "__main__":
    # Main items
    for folder, name, fn in JOBS:
        out = f"/home/sparky/ogrs/art/items/{folder}"
        os.makedirs(out, exist_ok=True)
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {folder}/{name}")

    # Tier-2 seeds (loose handfuls)
    for crop in TIER2_CROPS.keys():
        out = f"/home/sparky/ogrs/art/items/seeds/{crop}/tiers"
        os.makedirs(out, exist_ok=True)
        for tier in (1, 2, 3, 4):
            img = draw_tier2_seed(crop, tier)
            img.save(f"{out}/tier_{tier}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/tier_{tier}_x8.png")
        print(f"done seeds: {crop}")

    print("\n=== Phase 2 complete ===")
