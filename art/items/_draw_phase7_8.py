#!/usr/bin/env python3
"""
Phase 7 — Tier-4 rare crops (8 × 2 = 16 sprites)
Phase 8 — Flowers (15 species)

Total 31 sprites at 32×32.
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


# ===========================================================
# PHASE 7 — RARE CROPS
# ===========================================================

def saffron_raw():
    """Saffron crocus — purple flower with 3 red stigmas (the saffron)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    P_DK = ( 50,  20,  80, 255)
    P_B  = (100,  50, 150, 255)
    P_HI = (160, 100, 210, 255)
    RED = (220,  40,  20, 255)
    YELLOW = (250, 200,  60, 255)
    GR = ( 80, 130,  40, 255)
    OL = ( 20,  10,  40, 255)
    # 3 purple petals
    FLOWER = [
        "..OOO.OOO..",
        ".OBHO.OBHO.",
        "OBHHBOBHHBO",
        "OBHBBBBHHBO",
        ".OBBBBBBBO.",
        "..OBBBBBO..",
        "...OOOOO...",
    ]
    CM = {'O': OL, 'B': P_B, 'H': P_HI}
    stamp(px, 11, 9, FLOWER, CM)
    # Red stigmas (the saffron threads)
    for x, y in [(15, 13), (16, 13), (17, 13), (16, 12), (16, 14)]:
        put(px, x, y, RED)
    put(px, 16, 12, YELLOW)
    # Stem
    for y in range(16, 24):
        put(px, 16, y, GR)
    return img


def saffron_threads():
    """Dried saffron threads — red stringy spice."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    RED_DK = (130,  20,  10, 255)
    RED_B  = (200,  40,  20, 255)
    RED_HI = (240,  90,  50, 255)
    JAR_B  = (200, 200, 200, 255)
    JAR_HI = (240, 240, 245, 255)
    OL = ( 30,  18,   8, 255)
    # Small glass dish/jar with red threads piled
    DISH = [
        ".OOOOOOOOOO.",
        "OBHBBBBBBBBO",
        "OBHHRRRRRBBO",
        "OBHRRRRRRBBO",
        "OBHRRRRRRBBO",
        ".OOBBBBBBOO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': JAR_B, 'H': JAR_HI, 'R': RED_B}
    stamp(px, 10, 15, DISH, CM)
    # Thread strands
    for x in range(12, 21):
        put(px, x, 19, RED_HI if x % 2 == 0 else RED_DK)
        put(px, x, 18, RED_DK if x % 3 == 0 else RED_B)
    return img


def truffle_raw():
    """Black truffle — knobby dark mushroom."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  20,  10, 255)
    B  = ( 70,  50,  30, 255)
    HI = (110,  90,  60, 255)
    DIRT = ( 90,  70,  40, 255)
    OL = ( 14,   8,   4, 255)
    TRUFFLE = [
        "....OOOOO....",
        "..OOBBBBBOO..",
        ".OBHBBBBBBO.",
        "OBHHBBBBBBBO",
        "OBHHBBBBBBSO",
        "OBHBBBBBBSSO",
        "OBBBBBBBSSSO",
        ".OBBBBBBSSO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 9, 11, TRUFFLE, CM)
    # Knobby bumps
    for x, y in [(13, 14), (17, 14), (15, 17), (20, 16)]:
        put(px, x, y, DK)
    # Dirt clings
    for x, y in [(11, 17), (21, 18)]:
        put(px, x, y, DIRT)
    return img


def truffle_shaved():
    """Shaved truffle — small dish with thin black slices."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DISH_B  = (220, 220, 230, 255)
    DISH_HI = (250, 250, 255, 255)
    SLICE_DK = ( 30,  20,  10, 255)
    SLICE_B  = ( 70,  50,  30, 255)
    OL = ( 30,  18,   8, 255)
    DISH = [
        "..OOOOOOOOO..",
        ".OBBBBBBBBBO.",
        "OBHHHBBBBBBO",
        "OBBBBBBBBBBO",
        ".OBBBBBBBBO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': DISH_B, 'H': DISH_HI}
    stamp(px, 10, 15, DISH, CM)
    # Thin truffle slices on top
    for x in range(12, 21):
        put(px, x, 17, SLICE_DK if x % 2 == 0 else SLICE_B)
    for x in range(13, 20):
        put(px, x, 18, SLICE_B)
    return img


def vanilla_pod():
    """Vanilla bean — long brown pod."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 50,  30,  10, 255)
    B  = ( 90,  60,  30, 255)
    HI = (140, 100,  60, 255)
    OL = ( 20,  10,   4, 255)
    # Long thin pod, diagonal
    for i in range(20):
        x = 7 + i
        y = 20 - i // 2
        put(px, x, y, B)
        put(px, x, y - 1, HI)
        put(px, x, y + 1, DK)
        put(px, x - 1, y, OL)
        put(px, x, y - 2, OL)
        put(px, x, y + 2, OL)
    # Tips
    put(px, 7, 21, OL); put(px, 27, 11, OL)
    return img


def vanilla_ground():
    """Vanilla powder — dark brown ground spice in dish."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DISH_DK = ( 70,  46,  24, 255)
    DISH_B  = (138,  90,  46, 255)
    POWDER_DK = ( 40,  20,   8, 255)
    POWDER_B  = ( 80,  50,  20, 255)
    POWDER_HI = (120,  80,  40, 255)
    OL = ( 30,  18,   8, 255)
    DISH = [
        ".OOOOOOOOOO.",
        "OBBBBBBBBBBO",
        "OBPPPPPPPPBO",
        "OBPHPPPHPPBO",
        "OBPPPHPPPHBO",
        ".OBBPPPPBBO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': DISH_B, 'P': POWDER_B, 'H': POWDER_HI}
    stamp(px, 10, 14, DISH, CM)
    return img


def cocoa_pod():
    """Cocoa pod — large oval brown-red fruit on tree."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (110,  20,  10, 255)
    B  = (180,  50,  30, 255)
    HI = (220,  90,  60, 255)
    GROOVE = ( 80,  10,   8, 255)
    OL = ( 50,   8,   4, 255)
    POD = [
        "...OOOOO...",
        "..OBHHHBO..",
        ".OBHHHHHBO.",
        "OBHHHHHHHBO",
        "OBHHHHHHHBO",
        "OBHHHHHHBSO",
        "OBHHHHBBSSO",
        "OBHHBBBBSSO",
        ".OBBBBBSSO.",
        "..OOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 11, POD, CM)
    # Vertical grooves
    for y in range(12, 20):
        put(px, 15, y, GROOVE)
        put(px, 18, y, GROOVE)
    return img


def cocoa_beans():
    """Cocoa beans — handful of dark brown beans."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 50,  30,  10, 255)
    B  = (100,  60,  20, 255)
    HI = (160, 100,  40, 255)
    OL = ( 30,  16,   8, 255)
    beans = [(11, 17), (16, 16), (21, 17), (13, 20), (18, 21), (15, 19)]
    for cx, cy in beans:
        BEAN = [
            ".OOO.",
            "OBHBO",
            "OBHBSO",
            "OBBSSO",
            ".OOO.",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
        stamp(px, cx - 2, cy - 2, BEAN, CM)
    return img


def coffee_cherry():
    """Coffee cherries on branch — red ripe berries."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (130,  10,  20, 255)
    B  = (200,  30,  40, 255)
    HI = (240,  70,  80, 255)
    GREEN = ( 80, 140,  50, 255)
    STEM = ( 90,  60,  30, 255)
    OL = ( 50,   8,   8, 255)
    # 3 red cherries on branch
    cherries = [(12, 14), (17, 16), (21, 14)]
    for cx, cy in cherries:
        CHERRY = [
            ".OOO.",
            "OBHBO",
            "OBHBSO",
            "OBBSSO",
            ".OOO.",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
        stamp(px, cx - 2, cy - 2, CHERRY, CM)
    # Branch
    for x in range(11, 23):
        put(px, x, 20, STEM)
    # Leaf
    for x, y in [(16, 19), (17, 19), (18, 18)]:
        put(px, x, y, GREEN)
    return img


def coffee_beans():
    """Roasted coffee beans — dark brown with center groove."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  18,   8, 255)
    B  = ( 80,  44,  20, 255)
    HI = (130,  80,  40, 255)
    OL = ( 14,   8,   4, 255)
    beans = [(11, 16), (16, 17), (21, 16), (13, 20), (19, 21)]
    for cx, cy in beans:
        BEAN = [
            ".OOOO.",
            "OBHHBO",
            "OBBBSO",
            ".OOOO.",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
        stamp(px, cx - 2, cy - 2, BEAN, CM)
        # Center groove (signature coffee bean)
        put(px, cx, cy, DK)
    return img


def tea_leaves():
    """Fresh tea leaves on stem — light green oval leaves."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 40,  90,  30, 255)
    B  = ( 90, 160,  60, 255)
    HI = (140, 220, 100, 255)
    PALE = (180, 240, 130, 255)
    STEM = ( 80, 120,  40, 255)
    OL = ( 14,  40,  10, 255)
    # Stem + 5 leaves
    leaves = [(12, 12), (18, 11), (10, 16), (20, 17), (15, 20)]
    for cx, cy in leaves:
        LEAF = [
            ".OOO.",
            "OBHBO",
            "OPHBO",
            "OBHBSO",
            ".OOO.",
        ]
        CM = {'O': OL, 'B': B, 'H': HI, 'P': PALE, 'S': DK}
        stamp(px, cx - 2, cy - 2, LEAF, CM)
    # Stem
    for y in range(14, 22):
        put(px, 15, y, STEM)
    return img


def tea_dried():
    """Dried tea — small pile of curled leaves in tin."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    TIN_DK = ( 70,  60,  40, 255)
    TIN_B  = (140, 120,  80, 255)
    TIN_HI = (200, 180, 140, 255)
    LEAF_DK = ( 50,  70,  30, 255)
    LEAF_B  = ( 90, 120,  50, 255)
    OL = ( 30,  20,  10, 255)
    TIN = [
        ".OOOOOOOOOO.",
        "OBBBBBBBBBBO",
        "OBHHHHHHHHBO",
        "OBHLLLLLLHBO",
        "OBHLLLLLLHBO",
        "OBHLLLLLLHBO",
        ".OBBBBBBBBO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': TIN_B, 'H': TIN_HI, 'L': LEAF_B}
    stamp(px, 10, 13, TIN, CM)
    # Dried leaf texture
    for x, y in [(13, 17), (16, 18), (19, 17), (15, 19)]:
        put(px, x, y, LEAF_DK)
    return img


def mustard_seed_raw():
    """Tiny mustard seeds — pile of small yellow-brown spheres."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (130, 100,  30, 255)
    B  = (190, 150,  50, 255)
    HI = (240, 200,  80, 255)
    # Many tiny spheres clustered
    positions = [
        (11, 14), (13, 13), (15, 14), (17, 13), (19, 14), (21, 13),
        (10, 16), (12, 17), (14, 16), (16, 17), (18, 16), (20, 17), (22, 16),
        (11, 19), (13, 18), (15, 19), (17, 18), (19, 19), (21, 18),
        (12, 21), (14, 20), (16, 21), (18, 20), (20, 21),
    ]
    for x, y in positions:
        put(px, x, y, DK)
        put(px, x + 1, y, B)
        put(px, x, y + 1, HI)
        put(px, x + 1, y + 1, DK)
    return img


def mustard_seed_blessed():
    """Blessed mustard seed — single glowing seed (faith parable)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (130, 100,  30, 255)
    B  = (220, 180,  60, 255)
    HI = (255, 240, 130, 255)
    GLOW = (255, 255, 200, 100)
    WHITE = (255, 255, 255, 255)
    OL = ( 80,  60,  20, 255)
    # Halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 16, y - 16
            d2 = dx * dx + dy * dy
            if 36 <= d2 <= 80 and (x + y) % 2 == 0:
                put(px, x, y, GLOW)
    # Big single seed at center (3x prior size for emphasis)
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


def ginseng_root():
    """Ginseng root — gnarled tan root with multiple legs."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 90,  70,  30, 255)
    B  = (160, 130,  70, 255)
    HI = (220, 190, 120, 255)
    OL = ( 50,  30,  10, 255)
    # Body (rounded)
    BODY = [
        "....OOO....",
        "...OBHBO...",
        "..OBHHBSO..",
        ".OBHHHBSO..",
        ".OBHHBBSO..",
        "OBHHBBBSO..",
        "OBHBBBSSO..",
        ".OBBBSSO...",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 9, BODY, CM)
    # Branching legs (descending lines)
    legs = [
        [(12, 17), (11, 18), (10, 19), (9, 20)],
        [(14, 17), (13, 18), (12, 19), (12, 21), (11, 22)],
        [(16, 17), (16, 19), (16, 21), (16, 23)],
        [(18, 17), (19, 18), (20, 19)],
        [(20, 17), (21, 18), (22, 19), (22, 21)],
    ]
    for leg in legs:
        for x, y in leg:
            put(px, x, y, B)
            put(px, x, y + 1, OL)
    return img


def ginseng_tonic():
    """Ginseng tonic — small vial with golden liquid."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GLASS_DK = ( 40,  60,  80, 255)
    GLASS_B  = (180, 200, 220, 255)
    GLASS_HI = (220, 240, 250, 255)
    LIQ_DK = (160, 120,  20, 255)
    LIQ_B  = (220, 180,  60, 255)
    LIQ_HI = (250, 220, 130, 255)
    CORK = ( 90,  60,  20, 255)
    OL   = ( 20,  20,  30, 255)
    VIAL = [
        "...CC...",
        "..OOOO..",
        "..OGGO..",
        "..OGGO..",
        ".OOGGOO.",
        ".OGGGGO.",
        ".OGLLGO.",
        ".OLLLLO.",
        ".OLLLLO.",
        ".OHLLLO.",
        ".OLLLLO.",
        ".OOOOOO.",
    ]
    CM = {'O': OL, 'G': GLASS_B, 'C': CORK, 'L': LIQ_B, 'H': LIQ_HI}
    stamp(px, 12, 8, VIAL, CM)
    return img


# ===========================================================
# PHASE 8 — FLOWERS
# ===========================================================

def flower_helper(petal_colors, center_color, stem_color, leaf_color):
    """Generic 5-petal flower template. petal_colors = (dk, base, hi)."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    dk, base, hi = petal_colors
    OL = (10, 10, 10, 255)
    # 5 petals around center
    petals = [
        (16, 9),   # top
        (21, 12),  # right
        (19, 17),  # bottom right
        (13, 17),  # bottom left
        (11, 12),  # left
    ]
    for cx, cy in petals:
        PETAL = [
            ".OOO.",
            "OBHBO",
            "OBHBO",
            ".OOO.",
        ]
        CM = {'O': OL, 'B': base, 'H': hi}
        stamp(px, cx - 2, cy - 2, PETAL, CM)
    # Center bud
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        put(px, 16 + dx, 13 + dy, center_color)
    # Stem
    for y in range(18, 26):
        put(px, 16, y, stem_color)
    # Leaf
    for x, y in [(13, 21), (14, 21), (12, 22)]:
        put(px, x, y, leaf_color)
    return img


# Common flowers
def rose():
    return flower_helper(
        petal_colors=((100, 10, 30, 255), (200, 30, 50, 255), (240, 80, 90, 255)),
        center_color=(80, 0, 20, 255),
        stem_color=(80, 120, 40, 255),
        leaf_color=(110, 170, 60, 255))


def lavender():
    """Lavender — purple sprigs of small flowers on tall stems."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    P_DK = (60, 30, 100, 255)
    P_B  = (120, 80, 180, 255)
    P_HI = (180, 140, 220, 255)
    STEM = (80, 120, 40, 255)
    OL = (20, 10, 40, 255)
    # 3 lavender sprigs
    sprigs = [(13, 8), (16, 6), (19, 8)]
    for sx, sy in sprigs:
        # Tall sprig with multiple small purple buds
        for i in range(6):
            y = sy + i * 2
            put(px, sx, y, P_DK)
            put(px, sx + 1, y, P_B)
            put(px, sx, y + 1, P_HI)
            put(px, sx + 1, y + 1, P_DK)
        # Stem below
        for y in range(sy + 13, 28):
            put(px, sx, y, STEM)
    return img


def daisy():
    return flower_helper(
        petal_colors=((180, 180, 180, 255), (240, 240, 240, 255), (255, 255, 255, 255)),
        center_color=(250, 200, 60, 255),
        stem_color=(80, 130, 40, 255),
        leaf_color=(120, 180, 60, 255))


def sunflower():
    return flower_helper(
        petal_colors=((180, 130, 20, 255), (240, 190, 40, 255), (255, 220, 80, 255)),
        center_color=(80, 40, 10, 255),
        stem_color=(80, 130, 40, 255),
        leaf_color=(120, 180, 60, 255))


def tulip():
    """Tulip — closed cup-shaped flower."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (140, 20, 40, 255)
    B  = (210, 40, 60, 255)
    HI = (240, 90, 110, 255)
    STEM = (80, 130, 40, 255)
    LEAF = (110, 170, 60, 255)
    OL = (60, 8, 20, 255)
    # Cup shape (more closed than rose)
    CUP = [
        "..OOOOOO..",
        ".OBHBBBSO.",
        "OBHHBBBSO.",
        "OBHHBBBSSO",
        "OBHBBBBSSO",
        "OBHBBBBSSO",
        ".OBBBBSSO.",
        "..OBBSSO..",
        "...OOOO...",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 8, CUP, CM)
    # Stem
    for y in range(18, 28):
        put(px, 16, y, STEM)
    # Leaf
    for x, y in [(13, 24), (14, 23), (12, 25)]:
        put(px, x, y, LEAF)
    return img


def poppy():
    return flower_helper(
        petal_colors=((130, 10, 10, 255), (220, 30, 30, 255), (250, 70, 70, 255)),
        center_color=(10, 10, 10, 255),
        stem_color=(80, 130, 40, 255),
        leaf_color=(100, 160, 50, 255))


def marigold():
    return flower_helper(
        petal_colors=((160, 70, 10, 255), (240, 130, 30, 255), (255, 180, 60, 255)),
        center_color=(130, 50, 10, 255),
        stem_color=(80, 130, 40, 255),
        leaf_color=(110, 170, 60, 255))


# Magical flowers
def moonflower():
    """Moonflower — pale blue-white with glowing center, night-bloomer."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 80, 100, 160, 255)
    B  = (160, 200, 240, 255)
    HI = (220, 240, 255, 255)
    GLOW = (255, 255, 200, 120)
    CENTER = (255, 255, 230, 255)
    STEM = (40, 80, 100, 255)
    OL = (30, 50, 100, 255)
    # Glow halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 16, y - 14
            d2 = dx * dx + dy * dy
            if 40 <= d2 <= 80 and (x + y) % 2 == 0:
                put(px, x, y, GLOW)
    # 5 petals
    img2 = flower_helper((DK, B, HI), CENTER, STEM, B)
    # Composite glow onto img2
    base_px = img.load()
    for x in range(W):
        for y in range(H):
            p = img2.getpixel((x, y))
            if p[3] > 0:
                base_px[x, y] = p
    return img


def sunflower_large():
    """Large sunflower (different from common) — more dramatic with bigger petals."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180, 130, 20, 255)
    B  = (240, 190, 40, 255)
    HI = (255, 220, 80, 255)
    CENTER_DK = (60, 30, 10, 255)
    CENTER_B  = (120, 70, 20, 255)
    STEM = (80, 130, 40, 255)
    OL = (80, 50, 10, 255)
    # 8 petals in a star pattern
    petals = []
    for ang_deg in range(0, 360, 45):
        rad = math.radians(ang_deg)
        cx = 16 + int(round(math.cos(rad) * 7))
        cy = 14 + int(round(math.sin(rad) * 7))
        petals.append((cx, cy))
    for cx, cy in petals:
        PETAL = [
            "OOO",
            "OHO",
            "OBO",
            "OOO",
        ]
        CM = {'O': OL, 'B': B, 'H': HI}
        stamp(px, cx - 1, cy - 1, PETAL, CM)
    # Big center
    for x in range(13, 20):
        for y in range(11, 17):
            put(px, x, y, CENTER_B)
    # Outline center
    for x in range(13, 20):
        put(px, x, 11, OL)
        put(px, x, 16, OL)
    for y in range(12, 16):
        put(px, 13, y, OL)
        put(px, 19, y, OL)
    # Texture dots
    for x, y in [(14, 13), (16, 13), (18, 13), (15, 15), (17, 15)]:
        put(px, x, y, CENTER_DK)
    # Stem
    for y in range(20, 28):
        put(px, 16, y, STEM)
    return img


def nightshade():
    """Nightshade — dark purple with black accents, dangerous look."""
    return flower_helper(
        petal_colors=((20, 10, 40, 255), (60, 20, 90, 255), (110, 50, 150, 255)),
        center_color=(220, 220, 60, 255),
        stem_color=(40, 60, 30, 255),
        leaf_color=(60, 100, 40, 255))


def phoenix_bloom():
    """Phoenix bloom — flame-colored flower with glow."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (160, 30, 10, 255)
    B  = (240, 100, 20, 255)
    HI = (255, 180, 40, 255)
    PEAK = (255, 240, 130, 255)
    STEM = (90, 70, 30, 255)
    GLOW = (255, 180, 60, 100)
    # Glow halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 16, y - 14
            d2 = dx * dx + dy * dy
            if 36 <= d2 <= 90 and (x + y) % 2 == 0:
                put(px, x, y, GLOW)
    # Layered flame petals
    OL = (60, 10, 5, 255)
    petals = [(13, 8), (19, 8), (10, 13), (22, 13), (16, 6)]
    for cx, cy in petals:
        FL = [
            "OOO",
            "OHO",
            "OBO",
            "OBO",
            "OOO",
        ]
        CM = {'O': OL, 'B': B, 'H': HI}
        stamp(px, cx - 1, cy - 1, FL, CM)
    # Center peak
    put(px, 16, 13, PEAK)
    put(px, 16, 14, HI)
    # Stem
    for y in range(19, 28):
        put(px, 16, y, STEM)
    return img


def mandrake():
    """Mandrake — tiny humanoid-shaped root with leaves on top."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    ROOT_DK = (130, 100, 60, 255)
    ROOT_B  = (200, 170, 110, 255)
    LEAF_DK = (40, 90, 30, 255)
    LEAF_B  = (90, 170, 60, 255)
    LEAF_HI = (140, 220, 100, 255)
    OL = (60, 40, 20, 255)
    # Leafy top (5 leaves)
    leaves = [(13, 7), (16, 5), (19, 7), (12, 10), (20, 10)]
    for cx, cy in leaves:
        LEAF = [
            ".OO.",
            "OBHO",
            "OBHO",
            ".OO.",
        ]
        CM = {'O': OL, 'B': LEAF_B, 'H': LEAF_HI}
        stamp(px, cx - 1, cy - 1, LEAF, CM)
    # Body (humanoid root)
    # Head
    BODY = [
        "..OOOO..",
        ".OBBBBO.",
        "OBBBBBBO",
        "OBBBBBBO",
        ".OOOOOO.",
        ".OBBBBO.",
        "OBBBBBBO",
        "OBBBBBBO",
        ".OBBBBO.",
        "OBO..OBO",
        "OBO..OBO",
        "OOO..OOO",
    ]
    CM = {'O': OL, 'B': ROOT_B}
    stamp(px, 12, 13, BODY, CM)
    # Tiny face (eyes + mouth)
    put(px, 15, 15, OL)
    put(px, 17, 15, OL)
    put(px, 16, 17, OL)
    return img


# Sacred flowers
def lily_of_valley():
    """Lily of the valley — white bell-shaped flowers on green stem."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    WHITE_DK = (200, 200, 200, 255)
    WHITE_B  = (240, 240, 240, 255)
    WHITE_HI = (255, 255, 255, 255)
    LEAF_DK = (40, 90, 30, 255)
    LEAF_B  = (90, 160, 60, 255)
    LEAF_HI = (140, 210, 90, 255)
    STEM = (70, 120, 40, 255)
    OL = (30, 60, 20, 255)
    # Curved stem
    for y in range(8, 28):
        put(px, 16, y, STEM)
    # 3 bell flowers on the stem
    bells = [(16, 10), (16, 14), (16, 18)]
    for cx, cy in bells:
        BELL = [
            ".OOO.",
            "OBHBO",
            "OBHBO",
            ".OOO.",
        ]
        CM = {'O': OL, 'B': WHITE_B, 'H': WHITE_HI}
        stamp(px, cx - 2, cy, BELL, CM)
    # Long broad leaves on the side
    for y in range(20, 27):
        put(px, 10, y, LEAF_B)
        put(px, 11, y, LEAF_HI)
        put(px, 12, y, LEAF_DK)
    for y in range(22, 28):
        put(px, 20, y, LEAF_DK)
        put(px, 21, y, LEAF_B)
        put(px, 22, y, LEAF_HI)
    return img


def hyssop():
    """Hyssop — small herb with blue-purple flower spike."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    FL_DK = (40, 30, 100, 255)
    FL_B  = (90, 80, 180, 255)
    FL_HI = (140, 130, 220, 255)
    STEM = (80, 130, 40, 255)
    LEAF = (110, 160, 60, 255)
    OL = (14, 10, 40, 255)
    # Tall vertical spike of small purple flowers
    for i in range(8):
        y = 8 + i
        put(px, 16, y, FL_DK)
        put(px, 15, y, FL_B if i % 2 == 0 else FL_DK)
        put(px, 17, y, FL_B if i % 2 == 1 else FL_DK)
        if i % 2 == 0:
            put(px, 16, y, FL_HI)
    # Stem and leaves below
    for y in range(17, 28):
        put(px, 16, y, STEM)
    # Pairs of small leaves
    for y in (19, 22, 25):
        put(px, 14, y, LEAF)
        put(px, 18, y, LEAF)
    return img


def cedar_sprig():
    """Cedar sprig — small evergreen branch with needles."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (20, 50, 20, 255)
    B  = (50, 100, 40, 255)
    HI = (90, 160, 60, 255)
    STEM = (90, 60, 20, 255)
    OL = (10, 30, 10, 255)
    # Central branch
    for y in range(8, 26):
        put(px, 16, y, STEM)
    # Needle clusters branching outward
    needles = [
        (13, 11), (19, 11), (11, 14), (21, 14),
        (12, 17), (20, 17), (13, 20), (19, 20),
        (14, 23), (18, 23),
    ]
    for nx, ny in needles:
        # 3-pixel needle line
        for i in range(3):
            offset = -i if nx < 16 else i
            put(px, nx + offset, ny + i, HI if i == 0 else B)
            put(px, nx + offset, ny + i + 1, DK)
    return img


# ===========================================================
# DRIVER
# ===========================================================
JOBS = [
    # Phase 7 — rare crops
    ("rare_saffron",      "saffron_raw",       saffron_raw),
    ("rare_saffron",      "saffron_threads",   saffron_threads),
    ("rare_truffle",      "truffle_raw",       truffle_raw),
    ("rare_truffle",      "truffle_shaved",    truffle_shaved),
    ("rare_vanilla",      "vanilla_pod",       vanilla_pod),
    ("rare_vanilla",      "vanilla_ground",    vanilla_ground),
    ("rare_cocoa",        "cocoa_pod",         cocoa_pod),
    ("rare_cocoa",        "cocoa_beans",       cocoa_beans),
    ("rare_coffee",       "coffee_cherry",     coffee_cherry),
    ("rare_coffee",       "coffee_beans",      coffee_beans),
    ("rare_tea",          "tea_leaves",        tea_leaves),
    ("rare_tea",          "tea_dried",         tea_dried),
    ("rare_mustard_seed", "mustard_seed_raw",      mustard_seed_raw),
    ("rare_mustard_seed", "mustard_seed_blessed",  mustard_seed_blessed),
    ("rare_ginseng",      "ginseng_root",      ginseng_root),
    ("rare_ginseng",      "ginseng_tonic",     ginseng_tonic),
    # Phase 8 — flowers
    ("flowers_common",    "rose",          rose),
    ("flowers_common",    "lavender",      lavender),
    ("flowers_common",    "daisy",         daisy),
    ("flowers_common",    "sunflower",     sunflower),
    ("flowers_common",    "tulip",         tulip),
    ("flowers_common",    "poppy",         poppy),
    ("flowers_common",    "marigold",      marigold),
    ("flowers_magical",   "moonflower",    moonflower),
    ("flowers_magical",   "sunflower_large", sunflower_large),
    ("flowers_magical",   "nightshade",    nightshade),
    ("flowers_magical",   "phoenix_bloom", phoenix_bloom),
    ("flowers_magical",   "mandrake",      mandrake),
    ("flowers_sacred",    "lily_of_valley", lily_of_valley),
    ("flowers_sacred",    "hyssop",        hyssop),
    ("flowers_sacred",    "cedar_sprig",   cedar_sprig),
]


if __name__ == "__main__":
    for folder, name, fn in JOBS:
        out = f"/home/sparky/ogrs/art/items/{folder}"
        os.makedirs(out, exist_ok=True)
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {folder}/{name}")
    print(f"\n=== Phase 7+8 complete: {len(JOBS)} sprites ===")
