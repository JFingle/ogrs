#!/usr/bin/env python3
"""
Phase 1 — Universal staples for cooking system.

Per FOOD_AND_FARMING.md draw-order recommendation, these are the highest-
ROI items: ingredients used across the most recipes.

GROUPS:
  A. Wheat chain     — wheat, flour, dough, bread
  B. Cheese          — block, shredded
  C. Meats           — chicken / beef / pork / fish (raw + cooked)
  D. Eggs            — raw, fried, boiled
  E. Tier-1 veg      — 9 new crops × (seed+crop+cooked), plus crop+cooked for existing potato/onion/tomato

All sprites are 32×32 PNG, transparent background, RSC inventory-icon style.
"""
import os
from PIL import Image

W = H = 32
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def fill_rect(px, x, y, w, h, c):
    for dx in range(w):
        for dy in range(h):
            put(px, x + dx, y + dy, c)


def outline_rect(px, x, y, w, h, c):
    """Just the outline of a rectangle."""
    for dx in range(w):
        put(px, x + dx, y, c)
        put(px, x + dx, y + h - 1, c)
    for dy in range(h):
        put(px, x, y + dy, c)
        put(px, x + w - 1, y + dy, c)


def shaded_rect(px, x, y, w, h, base, hi, shad, outline):
    """Rect with full shading: base fill, hi on upper-left, shad on lower-right, outline border."""
    # Base fill
    fill_rect(px, x + 1, y + 1, w - 2, h - 2, base)
    # Highlight rows (upper-left)
    for dx in range(1, w - 1):
        put(px, x + dx, y + 1, hi)
    for dy in range(1, h - 1):
        put(px, x + 1, y + dy, hi if dy <= 2 else base)
    # Shadow on right + bottom
    for dy in range(1, h - 1):
        put(px, x + w - 2, y + dy, shad)
    for dx in range(1, w - 1):
        put(px, x + dx, y + h - 2, shad)
    # Outline
    outline_rect(px, x, y, w, h, outline)


def stamp(px, ox, oy, rows, color_map):
    """Place a multi-line ASCII art at (ox, oy)."""
    for ty, row in enumerate(rows):
        for tx, ch in enumerate(row):
            if ch == '.':
                continue
            put(px, ox + tx, oy + ty, color_map.get(ch))


# ===========================================================
# A. WHEAT CHAIN — wheat / flour / dough / bread
# ===========================================================

WHEAT_DK   = ( 88,  62,  20, 255)
WHEAT_BASE = (188, 140,  48, 255)
WHEAT_HI   = (240, 200,  88, 255)
STEM_BASE  = (108,  80,  28, 255)
STEM_HI    = (170, 124,  56, 255)


def wheat():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Vertical wheat stalk in middle
    # Stem
    for y in range(8, 28):
        put(px, 16, y, STEM_BASE)
        put(px, 15, y, STEM_HI)
        put(px, 17, y, WHEAT_DK)
    # Wheat head — bundle of grains at top
    # 5 rows of 3 grains
    GRAIN = [
        ".X.",
        "XHX",
        "XBX",
        "XBX",
        "XDX",
        ".X.",
    ]
    CM = {'X': WHEAT_DK, 'H': WHEAT_HI, 'B': WHEAT_BASE, 'D': WHEAT_DK}
    # Center bundle
    stamp(px, 14, 6, GRAIN, CM)
    # Side stalks (3 grains)
    SIDE = [
        ".X.",
        "XBX",
        "XBX",
        ".X.",
    ]
    stamp(px, 11, 8, SIDE, CM)
    stamp(px, 17, 8, SIDE, CM)
    # Awn (bristles)
    for dx in (-2, 0, 2):
        put(px, 16 + dx, 4, WHEAT_DK)
        put(px, 16 + dx, 3, WHEAT_DK)
    # Roots/tied bottom
    for dx in (-2, -1, 0, 1, 2):
        put(px, 16 + dx, 28, WHEAT_DK)
    return img


def flour():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Cloth sack with flour spilling
    SACK_DK = ( 70,  56,  36, 255)
    SACK_B  = (148, 122,  82, 255)
    SACK_HI = (200, 178, 130, 255)
    FLOUR_DK = (190, 188, 180, 255)
    FLOUR_B  = (230, 228, 220, 255)
    FLOUR_HI = (255, 255, 255, 255)
    OUTLINE  = ( 38,  30,  18, 255)

    # Sack body
    SACK = [
        "..OOOOOOO...",
        ".OBBSBBBBO..",
        "OBHHBBBBBBO.",
        "OBHHBBBBBBO.",
        "OBHHBBBBBBO.",
        "OBBBBBBSSBO.",
        "OBBBBBBSSBO.",
        "OBBBBBSSSBO.",
        ".OBBBBBSSBO.",
        ".OBBBBBSSO..",
        "..OOOOOOO...",
    ]
    CM = {'O': OUTLINE, 'B': SACK_B, 'H': SACK_HI, 'S': SACK_DK}
    stamp(px, 9, 11, SACK, CM)
    # Tied top with string
    for x in (15, 16, 17):
        put(px, x, 10, OUTLINE)
    put(px, 16, 9, OUTLINE)
    # Two ear loops
    put(px, 14, 10, OUTLINE)
    put(px, 18, 10, OUTLINE)
    # Flour spilling out the top + a small pile
    for x, y in [(14, 9), (15, 8), (17, 9), (18, 8), (16, 7)]:
        put(px, x, y, FLOUR_B)
    for x, y in [(15, 7), (17, 7), (16, 6)]:
        put(px, x, y, FLOUR_HI)
    # Small flour pile at the bottom
    for x in range(10, 21):
        put(px, x, 23, FLOUR_DK)
    for x in (12, 14, 16, 18, 20):
        put(px, x, 22, FLOUR_B)
    return img


def dough():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DOUGH_DK = (160, 132,  88, 255)
    DOUGH_B  = (210, 188, 140, 255)
    DOUGH_HI = (240, 222, 178, 255)
    OUTLINE  = ( 90,  68,  40, 255)
    # Rounded dough ball
    BALL = [
        "...OOOOO...",
        "..OBBBHBO..",
        ".OBHHHBBBO.",
        "OBHHHBBBBBO",
        "OBHHBBBBBBO",
        "OBHBBBBBSBO",
        "OBBBBBBSSBO",
        ".OBBBBSSBO.",
        "..OBBSSBO..",
        "...OOOOO...",
    ]
    CM = {'O': OUTLINE, 'B': DOUGH_B, 'H': DOUGH_HI, 'S': DOUGH_DK}
    stamp(px, 10, 11, BALL, CM)
    return img


def bread():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CRUST_DK = ( 92,  56,  20, 255)
    CRUST_B  = (172, 116,  56, 255)
    CRUST_HI = (220, 166, 100, 255)
    CRUMB    = (240, 218, 168, 255)
    OUTLINE  = ( 40,  20,   8, 255)
    # Loaf — rounded rectangle with diagonal score marks
    LOAF = [
        "..OOOOOOOOOO..",
        ".OBHHHHHHHHBO.",
        "OBHCCCCCCHBHBO",
        "OBHCCCCCCCHHBO",
        "OBCCCCCCCCCSBO",
        "OBCCCCCCCCSSBO",
        "OBBCCCCCCSBSBO",
        "OBBBCCCCSSBSBO",
        ".OBBBBSSBBBBO.",
        "..OOOOOOOOOO..",
    ]
    CM = {'O': OUTLINE, 'B': CRUST_B, 'H': CRUST_HI, 'C': CRUMB, 'S': CRUST_DK}
    stamp(px, 9, 11, LOAF, CM)
    # Score marks (3 diagonal slashes on top)
    for dx, dy in [(11, 13), (15, 13), (19, 13)]:
        put(px, dx, dy, CRUST_DK)
        put(px, dx + 1, dy - 1, CRUST_DK)
    return img


# ===========================================================
# B. CHEESE — block, shredded
# ===========================================================

CHEESE_DK = (160, 110,  20, 255)
CHEESE_B  = (240, 200,  60, 255)
CHEESE_HI = (255, 230, 130, 255)
CHEESE_O  = ( 90,  62,  10, 255)


def cheese_block():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Wedge of cheese — triangle with depth
    # Front face (visible)
    WEDGE = [
        ".......O....",
        "......OBO...",
        ".....OHBBO..",
        "....OHHBBBO.",
        "...OHHBBBBSO",
        "..OHHBBBBBSO",
        ".OHBBBBBBBSO",
        ".OBBBBBBBSSO",
        ".OBBBBBBSSSO",
        ".OBBBBSSSSO.",
        ".OBBSSSSSO..",
        ".OBSSSSO....",
        ".OOOOOO.....",
    ]
    CM = {'O': CHEESE_O, 'B': CHEESE_B, 'H': CHEESE_HI, 'S': CHEESE_DK}
    stamp(px, 8, 9, WEDGE, CM)
    # Holes in the cheese
    for x, y in [(13, 14), (17, 17), (15, 20)]:
        put(px, x, y, CHEESE_O)
    return img


def cheese_shredded():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Pile of shredded cheese strands
    # Multiple thin curved strands stacked
    strands = [
        # x_start, y, length
        (8, 22, 8),
        (12, 24, 9),
        (8, 18, 10),
        (14, 19, 8),
        (10, 16, 7),
        (16, 17, 8),
        (12, 14, 6),
        (10, 21, 5),
        (18, 22, 5),
        (15, 13, 5),
        (8, 26, 6),
        (14, 27, 7),
    ]
    for x, y, length in strands:
        for dx in range(length):
            put(px, x + dx, y, CHEESE_B)
            put(px, x + dx, y + 1, CHEESE_DK)
            if dx % 2 == 0:
                put(px, x + dx, y, CHEESE_HI)
    return img


# ===========================================================
# C. MEATS — chicken / beef / pork / fish (raw + cooked)
# ===========================================================

OUTLINE = ( 40,  24,  16, 255)


def chicken_raw():
    """Whole raw chicken — pink-tan plucked bird shape."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SKIN_DK = (200, 156, 130, 255)
    SKIN_B  = (240, 200, 174, 255)
    SKIN_HI = (255, 230, 210, 255)
    # Drumstick-and-thigh shape — round body with bone stub at one end
    BODY = [
        "...OOOO...",
        "..OBBBBO..",
        ".OHHBBBBO.",
        "OHHBBBBBSO",
        "OHHBBBBBSO",
        "OHBBBBBSSO",
        "OBBBBBSSOO",
        ".OBBBSSO..",
        "..OOSO....",
        "...OOO....",
    ]
    CM = {'O': OUTLINE, 'B': SKIN_B, 'H': SKIN_HI, 'S': SKIN_DK}
    stamp(px, 9, 9, BODY, CM)
    # Exposed bone stub
    for x, y in [(15, 22), (16, 22), (14, 23), (15, 23), (16, 23), (15, 24)]:
        put(px, x, y, (250, 230, 200, 255))
    put(px, 15, 21, OUTLINE)
    put(px, 16, 21, OUTLINE)
    return img


def chicken_cooked():
    """Roasted chicken — golden brown skin."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CRISP_DK = ( 96,  56,  20, 255)
    CRISP_B  = (188, 124,  48, 255)
    CRISP_HI = (240, 184,  88, 255)
    BODY = [
        "...OOOO...",
        "..OBBBBO..",
        ".OHHBBBBO.",
        "OHHBBBBBSO",
        "OHHBBBBBSO",
        "OHBBBBBSSO",
        "OBBBBBSSOO",
        ".OBBBSSO..",
        "..OOSO....",
        "...OOO....",
    ]
    CM = {'O': OUTLINE, 'B': CRISP_B, 'H': CRISP_HI, 'S': CRISP_DK}
    stamp(px, 9, 9, BODY, CM)
    # Crispy spots (dark dots scattered)
    for x, y in [(13, 12), (16, 15), (12, 17), (17, 18)]:
        put(px, x, y, CRISP_DK)
    # Bone stub
    for x, y in [(15, 22), (16, 22), (15, 23), (16, 23)]:
        put(px, x, y, (250, 230, 200, 255))
    return img


def beef_raw():
    """Red raw beef cut — slab of red meat with white fat marbling."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    MEAT_DK = (140,  30,  30, 255)
    MEAT_B  = (200,  60,  60, 255)
    MEAT_HI = (240, 110, 100, 255)
    FAT     = (250, 240, 220, 255)
    SLAB = [
        ".OOOOOOOOOO.",
        "OBHHBBBBBBSO",
        "OBHHBBFBBSSO",
        "OBHBBBFBBSSO",
        "OBBBFBBBBSSO",
        "OBBBFBBSBSSO",
        "OBBBBBBSSBSO",
        "OBBBBBBSSSSO",
        ".OOOOOOOOOO.",
    ]
    CM = {'O': OUTLINE, 'B': MEAT_B, 'H': MEAT_HI, 'S': MEAT_DK, 'F': FAT}
    stamp(px, 10, 11, SLAB, CM)
    return img


def beef_cooked():
    """Cooked beef — dark brown sear with hint of red inside."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SEAR_DK = ( 50,  24,  12, 255)
    SEAR_B  = (110,  60,  30, 255)
    SEAR_HI = (160,  96,  50, 255)
    PINK    = (180,  80,  60, 255)
    SLAB = [
        ".OOOOOOOOOO.",
        "OBHHBBBBBBSO",
        "OBHBBPPPBSSO",
        "OBHBPPPPPBSO",
        "OBBBPPPPPBSO",
        "OBBBPPPPPBSO",
        "OBBBBPPPBBSO",
        "OBBBBBBBBSSO",
        ".OOOOOOOOOO.",
    ]
    CM = {'O': OUTLINE, 'B': SEAR_B, 'H': SEAR_HI, 'S': SEAR_DK, 'P': PINK}
    stamp(px, 10, 11, SLAB, CM)
    return img


def pork_raw():
    """Pink raw pork — lighter than beef, more pink-white."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PORK_DK = (180, 110,  90, 255)
    PORK_B  = (230, 170, 150, 255)
    PORK_HI = (250, 210, 200, 255)
    FAT     = (250, 240, 220, 255)
    SLAB = [
        ".OOOOOOOOOO.",
        "OFFFFBBBBBBO",
        "OFFFFBBBBBSO",
        "OBHHBBBBBSSO",
        "OBHBBBBBBSSO",
        "OBBBBBSBBSSO",
        "OBBBBBSSBBSO",
        "OFFFFBBBSSSO",
        ".OOOOOOOOOO.",
    ]
    CM = {'O': OUTLINE, 'B': PORK_B, 'H': PORK_HI, 'S': PORK_DK, 'F': FAT}
    stamp(px, 10, 11, SLAB, CM)
    return img


def pork_cooked():
    """Cooked pork — light golden brown."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PORK_DK = (130,  74,  36, 255)
    PORK_B  = (200, 138,  82, 255)
    PORK_HI = (244, 200, 144, 255)
    FAT     = (240, 220, 180, 255)
    SLAB = [
        ".OOOOOOOOOO.",
        "OFFFFBBBBBBO",
        "OFFFFBBBBBSO",
        "OBHHBBBBBSSO",
        "OBHBBBBBBSSO",
        "OBBBBBSBBSSO",
        "OBBBBBSSBBSO",
        "OFFFFBBBSSSO",
        ".OOOOOOOOOO.",
    ]
    CM = {'O': OUTLINE, 'B': PORK_B, 'H': PORK_HI, 'S': PORK_DK, 'F': FAT}
    stamp(px, 10, 11, SLAB, CM)
    return img


def fish_raw():
    """Raw fish — silvery side view with fin and tail."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SILVER_DK = ( 78, 100, 120, 255)
    SILVER_B  = (148, 170, 190, 255)
    SILVER_HI = (220, 230, 240, 255)
    BELLY     = (240, 242, 244, 255)
    EYE       = ( 20,  20,  30, 255)
    FISH = [
        "....OOOO........",
        "...OBHHHHO......",
        "..OBHBBBHHO.....",
        "OOBHBBBBBHHHO...",
        "OBSBBBBBBBHHHOOO",
        "OBSBBEBBBBBHHHHO",
        "OBSBBBBBBBBBBHHO",
        "OBSBBBBBBBBBBSOO",
        "OBSBSSSSBBBBSOO.",
        ".OBBSSSSBBBSO...",
        "..OOOOSSSOO.....",
        ".....OOOO.......",
    ]
    CM = {'O': OUTLINE, 'B': SILVER_B, 'H': SILVER_HI, 'S': SILVER_DK, 'E': EYE}
    stamp(px, 8, 10, FISH, CM)
    return img


def fish_cooked():
    """Cooked fish — golden cooked appearance."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    GOLD_DK   = (130,  84,  20, 255)
    GOLD_B    = (210, 160,  68, 255)
    GOLD_HI   = (244, 210, 130, 255)
    EYE       = ( 30,  20,  16, 255)
    FISH = [
        "....OOOO........",
        "...OBHHHHO......",
        "..OBHBBBHHO.....",
        "OOBHBBBBBHHHO...",
        "OBSBBBBBBBHHHOOO",
        "OBSBBEBBBBBHHHHO",
        "OBSBBBBBBBBBBHHO",
        "OBSBBBBBBBBBBSOO",
        "OBSBSSSSBBBBSOO.",
        ".OBBSSSSBBBSO...",
        "..OOOOSSSOO.....",
        ".....OOOO.......",
    ]
    CM = {'O': OUTLINE, 'B': GOLD_B, 'H': GOLD_HI, 'S': GOLD_DK, 'E': EYE}
    stamp(px, 8, 10, FISH, CM)
    # Crispy spots
    for x, y in [(13, 14), (17, 15), (15, 17)]:
        put(px, x, y, GOLD_DK)
    return img


# ===========================================================
# D. EGGS — raw, fried, boiled
# ===========================================================

def egg_raw():
    """Single white egg with subtle shading."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SHELL_DK = (200, 196, 184, 255)
    SHELL_B  = (240, 236, 224, 255)
    SHELL_HI = (255, 255, 250, 255)
    SHELL_O  = ( 90,  82,  60, 255)
    EGG = [
        "...OOOO...",
        "..OHHBBO..",
        ".OHHBBBBO.",
        "OHHHBBBBSO",
        "OHHBBBBBBSO",
        "OHBBBBBBBSO",
        "OBBBBBBBSSO",
        "OBBBBBBSSSO",
        ".OBBBBSSSO.",
        "..OOOOOOO..",
    ]
    CM = {'O': SHELL_O, 'B': SHELL_B, 'H': SHELL_HI, 'S': SHELL_DK}
    stamp(px, 11, 10, EGG, CM)
    return img


def egg_fried():
    """Sunny side up — white circle with yellow yolk."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    WHITE_DK = (220, 218, 212, 255)
    WHITE_B  = (250, 248, 240, 255)
    YOLK_DK  = (200, 140,  20, 255)
    YOLK_B   = (250, 200,  60, 255)
    YOLK_HI  = (255, 230, 120, 255)
    OL       = ( 90,  80,  60, 255)
    # Outer white blob (irregular)
    WHITE = [
        "..OOOOOOOOO..",
        ".OBBBBBBBBBO.",
        "OBBBBBBBBBBO.",
        "OBBBYYYYBBBBO",
        "OBBYYHYYYBBBO",
        "OBBYHHYYYBBBO",
        "OBBYYYYYBBBBO",
        "OBBBBBBBBBBBO",
        ".OBBBBBBBBBO.",
        "..OOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': WHITE_B, 'Y': YOLK_B, 'H': YOLK_HI}
    stamp(px, 9, 11, WHITE, CM)
    return img


def egg_boiled():
    """Boiled and halved — visible yolk."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    WHITE_DK = (200, 196, 184, 255)
    WHITE_B  = (250, 248, 240, 255)
    YOLK_B   = (250, 220, 110, 255)
    YOLK_HI  = (255, 240, 160, 255)
    OL       = ( 70,  60,  40, 255)
    # Two halves side by side
    HALF1 = [
        ".OOOOO.",
        "OBBBBSO",
        "OBYYYBSO",
        "OBYHYBSO",
        "OBYYYBSO",
        "OBBBBSSO",
        ".OOOOOO.",
    ]
    HALF2 = [
        ".OOOOO.",
        "OBBBBSO",
        "OBYYYBSO",
        "OBYHYBSO",
        "OBYYYBSO",
        "OBBBBSSO",
        ".OOOOOO.",
    ]
    CM = {'O': OL, 'B': WHITE_B, 'S': WHITE_DK, 'Y': YOLK_B, 'H': YOLK_HI}
    stamp(px, 5, 12, HALF1, CM)
    stamp(px, 18, 12, HALF2, CM)
    return img


# ===========================================================
# E. TIER-1 VEGETABLES
# Each crop has: seed, harvested crop (raw), cooked variant
# We already have seed tiers for potato/onion/tomato.
# This pass adds the harvest+cooked versions for those 3,
# plus seed+crop+cooked for 9 new vegetables.
# ===========================================================

def potato_raw():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    P_DK = (120,  80,  30, 255)
    P_B  = (180, 130,  60, 255)
    P_HI = (220, 180,  90, 255)
    P_O  = ( 60,  36,  10, 255)
    P_EYE= ( 40,  20,  10, 255)
    SHAPE = [
        "..OOOOOO..",
        ".OBHHBBSO.",
        "OBHHHBBBBSO",
        "OBHBBBBBBSO",
        "OBBBBBBBBSO",
        "OBBBBBSSBSO",
        "OBBBBBSSSSO",
        ".OBBBSSSSO.",
        "..OOOOOOO..",
    ]
    CM = {'O': P_O, 'B': P_B, 'H': P_HI, 'S': P_DK}
    stamp(px, 10, 11, SHAPE, CM)
    # Eyes (potato sprouts)
    for x, y in [(14, 14), (17, 16), (15, 18)]:
        put(px, x, y, P_EYE)
    return img


def potato_cooked():
    """Baked potato — split open with fluffy interior."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SKIN_DK = ( 80,  44,  16, 255)
    SKIN_B  = (140,  90,  40, 255)
    FLESH_B = (244, 230, 178, 255)
    FLESH_HI= (255, 245, 210, 255)
    BUTTER  = (255, 220,  80, 255)
    P_O     = ( 40,  20,   8, 255)
    SHAPE = [
        "..OOOOOOOO..",
        ".OBBBBBBBBO.",
        "OBBFFHHFFBSO",
        "OBFHHHHHHFBO",
        "OBFFYYYFFFBO",
        "OBFFHHHHFFBO",
        "OBBFFFFFFBBO",
        ".OBBBBBBBBO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': P_O, 'B': SKIN_B, 'F': FLESH_B, 'H': FLESH_HI, 'Y': BUTTER, 'S': SKIN_DK}
    stamp(px, 10, 11, SHAPE, CM)
    return img


def onion_raw():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    O_DK = (160, 100,  20, 255)
    O_B  = (220, 170,  60, 255)
    O_HI = (250, 220, 130, 255)
    O_O  = ( 60,  30,   0, 255)
    GR   = ( 80, 120,  40, 255)
    BULB = [
        "...OOOOOO...",
        "..OBHHBBSO..",
        ".OBHHHBBBSO.",
        "OBHHHBBBBBSO",
        "OBHHBBBBBBSO",
        "OBHBBBBBBSSO",
        "OBBBBBBBSSSO",
        "OBBBBBSSSSSO",
        ".OBBBBSSSSO.",
        "..OBBSSSSO..",
        "...OOOOOO...",
    ]
    CM = {'O': O_O, 'B': O_B, 'H': O_HI, 'S': O_DK}
    stamp(px, 10, 11, BULB, CM)
    # Green sprout from top
    for y in (8, 9, 10):
        put(px, 16, y, GR)
    put(px, 15, 9, GR)
    put(px, 17, 8, GR)
    return img


def onion_cooked():
    """Sautéed onion — translucent golden."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    OUTLINE = ( 80,  50,  10, 255)
    GOLD_DK = (160, 110,  40, 255)
    GOLD_B  = (220, 180,  90, 255)
    GOLD_HI = (250, 220, 140, 255)
    # Pile of cooked onion rings
    rings = [
        (8, 18), (16, 19), (12, 20), (20, 20),
        (10, 22), (18, 22), (14, 24)
    ]
    for cx, cy in rings:
        # Small ring
        put(px, cx, cy, GOLD_DK)
        put(px, cx + 1, cy, GOLD_B)
        put(px, cx + 2, cy, GOLD_HI)
        put(px, cx + 3, cy, GOLD_B)
        put(px, cx + 4, cy, GOLD_DK)
        put(px, cx, cy + 1, GOLD_DK)
        put(px, cx + 4, cy + 1, GOLD_DK)
        put(px, cx, cy + 2, GOLD_DK)
        put(px, cx + 1, cy + 2, GOLD_B)
        put(px, cx + 2, cy + 2, GOLD_HI)
        put(px, cx + 3, cy + 2, GOLD_B)
        put(px, cx + 4, cy + 2, GOLD_DK)
    return img


def tomato_raw():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    R_DK = (120,  16,   8, 255)
    R_B  = (200,  40,  20, 255)
    R_HI = (240, 100,  60, 255)
    R_O  = ( 60,   8,   4, 255)
    GR   = ( 60, 100,  30, 255)
    GR_HI= (110, 160,  60, 255)
    TOM = [
        "...OOOOOO...",
        "..OBBHHBBSO..",
        ".OBHHHHBBBSO.",
        "OBHHHBBBBBBSO",
        "OBHHBBBBBBBSO",
        "OBHBBBBBBBSSO",
        "OBBBBBBBBSSSO",
        ".OBBBBBBBSSO.",
        "..OOOOOOOOO..",
    ]
    CM = {'O': R_O, 'B': R_B, 'H': R_HI, 'S': R_DK}
    stamp(px, 9, 12, TOM, CM)
    # Green leaves on top
    for x, y in [(15, 9), (16, 9), (17, 9), (14, 10), (18, 10), (16, 10)]:
        put(px, x, y, GR)
    put(px, 16, 10, GR_HI)
    put(px, 13, 10, R_O)
    put(px, 19, 10, R_O)
    return img


def tomato_cooked():
    """Tomato sauce — bowl of red sauce with herbs."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 70,  46,  24, 255)
    BOWL_B  = (138,  90,  46, 255)
    SAUCE_DK = (140,  20,  10, 255)
    SAUCE_B  = (200,  50,  30, 255)
    SAUCE_HI = (240,  90,  50, 255)
    HERB     = ( 80, 140,  50, 255)
    # Bowl rim + body
    BOWL = [
        "OOOOOOOOOO",
        "OSSSSSSSSO",
        "OBSSSSSSBO",
        "OBBBSSBBBO",
        ".OOBBBBOO.",
        "..OOOOOO..",
    ]
    CM = {'O': BOWL_DK, 'B': BOWL_B, 'S': SAUCE_B}
    stamp(px, 11, 16, BOWL, CM)
    # Sauce surface bubbles
    put(px, 14, 17, SAUCE_HI)
    put(px, 18, 17, SAUCE_HI)
    put(px, 16, 18, SAUCE_HI)
    # Herbs scattered
    put(px, 14, 18, HERB)
    put(px, 19, 18, HERB)
    put(px, 16, 17, HERB)
    return img


# Generic vegetable seed (small handful of seeds in palette of the crop)
def seed_generic(color_dk, color_b, color_hi):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    OUT = ( 40,  24,  10, 255)
    POUCH_B  = (148, 100,  40, 255)
    POUCH_HI = (200, 150,  78, 255)
    POUCH_OUT= ( 50,  30,  10, 255)
    # Small pouch
    POUCH = [
        ".OOOOOOOO.",
        "OBHHBBBBSO",
        "OBHHBBBBSO",
        "OBHBBBBBSO",
        "OBBBBBBBSO",
        ".OOOOOOOO.",
    ]
    CM = {'O': POUCH_OUT, 'B': POUCH_B, 'H': POUCH_HI, 'S': POUCH_OUT}
    stamp(px, 11, 19, POUCH, CM)
    # Tie
    put(px, 16, 18, POUCH_OUT)
    put(px, 15, 18, POUCH_OUT)
    put(px, 17, 18, POUCH_OUT)
    # 3-4 seeds peeking out, colored per crop
    for x, y in [(13, 17), (16, 16), (19, 17)]:
        put(px, x, y, color_hi)
        put(px, x + 1, y, color_b)
        put(px, x, y + 1, color_dk)
    return img


# ---- 9 new vegetables, each with seed/crop/cooked ----

VEGGIES = [
    # (name, seed_color, crop_func, cooked_func)
]


def cabbage_crop():
    """Round cabbage — many layered green leaves."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  70,  20, 255)
    B  = ( 80, 140,  50, 255)
    HI = (130, 200,  80, 255)
    PALE = (180, 220, 130, 255)
    OL = ( 14,  40,  10, 255)
    SHAPE = [
        "...OOOOOOO...",
        "..OBHPPHBBO..",
        ".OBHPPHHBBSO.",
        "OBHPPHHBBBSSO",
        "OBHHHBBBBBSSO",
        "OBHBBBBBBBSSO",
        "OBBBBBBBBSSSO",
        ".OBBBBBBBSSO.",
        "..OBBBSSSSO..",
        "...OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK, 'P': PALE}
    stamp(px, 9, 11, SHAPE, CM)
    # Vein details
    for x, y in [(15, 13), (15, 14), (15, 15), (15, 16)]:
        put(px, x, y, PALE)
    return img


def cabbage_cooked():
    """Sauerkraut / coleslaw — shredded cabbage pile."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PALE = (200, 230, 170, 255)
    MID  = (140, 200, 100, 255)
    DK   = ( 70, 130,  40, 255)
    strands = [(8, 16), (12, 18), (16, 16), (20, 18), (10, 20), (14, 21), (18, 20)]
    for x, y in strands:
        for dx in range(6):
            put(px, x + dx, y, MID if dx % 2 == 0 else PALE)
            put(px, x + dx, y + 1, DK)
    return img


def lettuce_crop():
    """Head of lettuce — ruffled green leaves."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 40,  80,  30, 255)
    B  = (110, 160,  60, 255)
    HI = (170, 210, 100, 255)
    PALE = (210, 230, 140, 255)
    OL = ( 20,  44,  10, 255)
    SHAPE = [
        "..OOOOOOOOO..",
        ".OHHHPPPHHHO.",
        "OBHHPPPPHHBSO",
        "OBHHPPHHBBBSO",
        "OBHHHBBBBBSSO",
        "OBHBBBBBBSSSO",
        ".OBBBBBBSSSO.",
        "..OBBBSSSSO..",
        "...OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK, 'P': PALE}
    stamp(px, 9, 11, SHAPE, CM)
    return img


def lettuce_cooked():
    """Salad bowl — bowl with lettuce leaves on top."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 90,  60,  30, 255)
    BOWL_B  = (160, 110,  60, 255)
    LEAF_DK = ( 40,  80,  30, 255)
    LEAF_B  = (130, 180,  80, 255)
    LEAF_HI = (180, 220, 120, 255)
    # Bowl
    BOWL = [
        "OOOOOOOOOO",
        "OBSSSSSSSO",
        "OBBSSSSSSO",
        ".OOSSSSOO.",
        "..OOOOOO..",
    ]
    CM = {'O': BOWL_DK, 'B': BOWL_B, 'S': BOWL_B}
    stamp(px, 11, 17, BOWL, CM)
    # Lettuce leaves piled
    leaves = [(12, 14), (15, 13), (18, 14), (13, 16), (17, 16), (15, 15)]
    for x, y in leaves:
        put(px, x, y, LEAF_DK)
        put(px, x + 1, y, LEAF_B)
        put(px, x + 2, y, LEAF_HI)
        put(px, x + 3, y, LEAF_B)
        put(px, x, y + 1, LEAF_DK)
        put(px, x + 3, y + 1, LEAF_DK)
    return img


def garlic_crop():
    """Garlic bulb — white papery skin with cloves visible."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PAPER_DK = (180, 170, 150, 255)
    PAPER_B  = (230, 220, 200, 255)
    PAPER_HI = (255, 250, 235, 255)
    STEM     = (140, 130, 100, 255)
    OL       = ( 80,  70,  50, 255)
    BULB = [
        "....OOOOO....",
        "...OHHHHHO...",
        "..OHHBBBHHO..",
        ".OHBBBBBHHHO.",
        "OBHBBBSSBBHHO",
        "OBHBBBSSBBSSO",
        "OBHBBBSSBSSSO",
        ".OBBBSSSSSO..",
        "..OBBSSSSO...",
        "...OOOOOO....",
    ]
    CM = {'O': OL, 'B': PAPER_B, 'H': PAPER_HI, 'S': PAPER_DK}
    stamp(px, 9, 11, BULB, CM)
    # Stem at top
    for y in (8, 9, 10):
        put(px, 15, y, STEM)
        put(px, 16, y, STEM)
    return img


def garlic_cooked():
    """Roasted garlic — golden roasted bulb."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    ROAST_DK = (120,  80,  20, 255)
    ROAST_B  = (200, 160,  80, 255)
    ROAST_HI = (240, 210, 140, 255)
    OL       = ( 60,  40,  10, 255)
    BULB = [
        "....OOOOO....",
        "...OHHHHHO...",
        "..OHHBBBHHO..",
        ".OHBBBBBHHHO.",
        "OBHBBBSSBBHHO",
        "OBHBBBSSBBSSO",
        ".OBBBSSSSSO..",
        "..OBBSSSSO...",
        "...OOOOOO....",
    ]
    CM = {'O': OL, 'B': ROAST_B, 'H': ROAST_HI, 'S': ROAST_DK}
    stamp(px, 9, 11, BULB, CM)
    return img


def beans_crop():
    """Green beans — pods."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  80,  30, 255)
    B  = ( 80, 150,  60, 255)
    HI = (130, 200, 100, 255)
    OL = ( 14,  40,  10, 255)
    # 3 pods bundled
    pods = [(10, 18), (13, 14), (18, 16)]
    for cx, cy in pods:
        for dy in range(10):
            put(px, cx, cy + dy, OL)
            put(px, cx + 1, cy + dy, B)
            put(px, cx + 2, cy + dy, HI if dy % 3 == 1 else B)
            put(px, cx + 3, cy + dy, DK)
            put(px, cx + 4, cy + dy, OL)
    return img


def beans_cooked():
    """Bean stew — bowl with beans visible."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_DK = ( 70,  46,  24, 255)
    BOWL_B  = (138,  90,  46, 255)
    BROTH   = (180, 110,  60, 255)
    BEAN_DK = ( 50,  90,  30, 255)
    BEAN_B  = (110, 170,  80, 255)
    OL      = ( 30,  16,   8, 255)
    BOWL = [
        "OOOOOOOOOO",
        "OBBBBBBBBO",
        "OBLLLLLLBO",
        "OBLLLLLLBO",
        ".OOBBBBOO.",
        "..OOOOOO..",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'L': BROTH}
    stamp(px, 11, 16, BOWL, CM)
    # Beans visible in broth
    for x, y in [(13, 18), (16, 18), (19, 18), (14, 19), (18, 19), (16, 19)]:
        put(px, x, y, BEAN_DK)
        put(px, x + 1, y, BEAN_B)
    return img


def peas_crop():
    """Pea pod — green with peas inside."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 40,  90,  30, 255)
    B  = (100, 170,  70, 255)
    HI = (160, 220, 110, 255)
    OL = ( 16,  44,  10, 255)
    # Curved pod silhouette
    POD = [
        "....OOOO....",
        "...OHHBBO...",
        "..OHHBBBBO..",
        ".OHBBBBBBO..",
        "OHHBBBBBBSO.",
        "OHBBBBBBBSO.",
        "OBBBBBBBBSO.",
        ".OBBBBBBSO..",
        "..OBBBBSO...",
        "...OOOOO....",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 10, 11, POD, CM)
    # 3 peas bumps inside the pod
    for x, y in [(14, 14), (16, 15), (18, 14)]:
        put(px, x, y, HI)
    return img


def peas_cooked():
    """Pile of cooked peas."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 50, 100,  30, 255)
    B  = (110, 170,  70, 255)
    HI = (170, 220, 120, 255)
    OL = ( 16,  44,  10, 255)
    peas = [
        (10, 18), (13, 18), (16, 18), (19, 18), (22, 18),
        (8, 20), (11, 20), (14, 20), (17, 20), (20, 20),
        (12, 22), (15, 22), (18, 22),
        (14, 24), (17, 24),
    ]
    for x, y in peas:
        put(px, x, y, OL)
        put(px, x + 1, y, B)
        put(px, x, y + 1, B)
        put(px, x + 1, y + 1, HI)
    return img


def corn_crop():
    """Ear of corn with husk."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    KERNEL_DK = (200, 160,  20, 255)
    KERNEL_B  = (250, 220,  60, 255)
    KERNEL_HI = (255, 240, 140, 255)
    HUSK_DK   = ( 80, 120,  40, 255)
    HUSK_B    = (140, 180,  60, 255)
    OL        = ( 60,  40,  10, 255)
    # Ear of corn vertical with husk peeled back
    EAR = [
        "....OOOOO....",
        "...OYYYYO....",
        "..OYKKKKHO...",
        ".OYKKKKKHHO..",
        ".OYKKKKKKHO..",
        ".OYKKKKKKHO..",
        ".OYKKKKKKHO..",
        ".OYKKKKKKHO..",
        ".OYKKKKKKHO..",
        ".OYKKKKKHO...",
        "..OYKKKKHO...",
        "...OYYYYO....",
        "....OOOOO....",
    ]
    CM = {'O': OL, 'K': KERNEL_B, 'Y': KERNEL_DK, 'H': KERNEL_HI}
    stamp(px, 9, 9, EAR, CM)
    # Husk leaves peeled back at bottom
    for x, y in [(11, 24), (12, 25), (13, 26), (19, 24), (20, 25), (21, 26)]:
        put(px, x, y, HUSK_B)
    for x, y in [(10, 26), (22, 26)]:
        put(px, x, y, HUSK_DK)
    return img


def corn_cooked():
    """Buttered corn on cob."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    KERNEL_DK = (200, 150,  20, 255)
    KERNEL_B  = (250, 215,  70, 255)
    KERNEL_HI = (255, 240, 130, 255)
    BUTTER    = (255, 255, 200, 255)
    OL        = ( 70,  44,  10, 255)
    # Same shape, slightly more golden
    EAR = [
        "..OOOOOO..",
        ".OYKKKKO..",
        ".OYKKKKHO.",
        ".OYKKKKHO.",
        ".OYKKKKHO.",
        ".OYKKKKHO.",
        ".OYKKKKHO.",
        ".OYKKKKHO.",
        ".OYKKKKO..",
        "..OOOOOO..",
    ]
    CM = {'O': OL, 'K': KERNEL_B, 'Y': KERNEL_DK, 'H': KERNEL_HI}
    stamp(px, 11, 11, EAR, CM)
    # Butter drip
    for x, y in [(14, 12), (16, 14), (15, 18)]:
        put(px, x, y, BUTTER)
    return img


def carrot_crop():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180,  60,  10, 255)
    B  = (240, 110,  30, 255)
    HI = (255, 160,  80, 255)
    GR_DK = ( 30,  80,  20, 255)
    GR_B  = ( 90, 160,  50, 255)
    GR_HI = (140, 210,  80, 255)
    OL    = ( 80,  30,   8, 255)
    # Carrot — long triangle pointing down
    CAR = [
        "OOOOO",
        "OBHBO",
        "OBHHBO",
        "OBHHBO",
        "OBHHBSO",
        "OBHBBSO",
        "OBBBSSO",
        "OBBSSSO",
        ".OBSSO.",
        "..OSSO.",
        "...OSO.",
        "....OO.",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 12, 14, CAR, CM)
    # Green leaves on top
    for x, y in [(13, 11), (14, 10), (15, 9), (16, 10), (17, 11), (16, 12)]:
        put(px, x, y, GR_B)
    for x, y in [(14, 11), (15, 10), (16, 11)]:
        put(px, x, y, GR_HI)
    return img


def carrot_cooked():
    """Sliced carrot rounds."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180,  80,  20, 255)
    B  = (240, 130,  40, 255)
    HI = (255, 180, 100, 255)
    OL = ( 80,  40,  10, 255)
    rings = [(10, 16), (15, 14), (20, 16), (12, 20), (17, 20), (14, 22), (19, 22)]
    for cx, cy in rings:
        cells = {
            (-1, -1): OL, (0, -1): OL, (1, -1): OL,
            (-2, 0): OL, (-1, 0): B, (0, 0): HI, (1, 0): B, (2, 0): OL,
            (-1, 1): OL, (0, 1): B, (1, 1): OL,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
    return img


def cucumber_crop():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 30,  80,  30, 255)
    B  = ( 80, 150,  60, 255)
    HI = (140, 200,  90, 255)
    PALE = (190, 230, 130, 255)
    OL = ( 16,  44,  10, 255)
    # Horizontal cucumber
    CUC = [
        ".OOOOOOOOOOOOO.",
        "OHHHBBBBBBBSSSO",
        "OPPHHBBBBSSSSSO",
        "OPPHHBBBBSSSSSO",
        "OHHHBBBBBBSSSSO",
        ".OOOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'P': PALE, 'S': DK}
    stamp(px, 8, 13, CUC, CM)
    # Bumpy texture dots
    for x in (12, 16, 20):
        put(px, x, 15, DK)
        put(px, x, 16, DK)
    return img


def cucumber_cooked():
    """Pickled cucumber slices."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = ( 60, 110,  30, 255)
    B  = (130, 180,  70, 255)
    HI = (180, 220, 110, 255)
    OL = ( 30,  60,  10, 255)
    SEED = (220, 220, 160, 255)
    rounds = [(10, 14), (16, 14), (22, 14), (13, 18), (19, 18), (16, 22)]
    for cx, cy in rounds:
        cells = {
            (-2, -2): OL, (-1, -2): OL, (0, -2): OL, (1, -2): OL,
            (-3, -1): OL, (-2, -1): B, (-1, -1): HI, (0, -1): HI, (1, -1): B, (2, -1): OL,
            (-3, 0): OL, (-2, 0): HI, (-1, 0): SEED, (0, 0): SEED, (1, 0): HI, (2, 0): OL,
            (-3, 1): OL, (-2, 1): B, (-1, 1): B, (0, 1): B, (1, 1): B, (2, 1): OL,
            (-2, 2): OL, (-1, 2): OL, (0, 2): OL, (1, 2): OL,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
    return img


def bellpepper_crop():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (140,  20,   8, 255)
    B  = (210,  40,  30, 255)
    HI = (240,  80,  50, 255)
    GR = ( 50, 110,  30, 255)
    GR_HI = (110, 170,  60, 255)
    OL = ( 60,   8,   4, 255)
    # Bell pepper shape
    PEP = [
        "...OOO....",
        "..OHBBO...",
        ".OHHBBSO..",
        "OBHHBBBSO.",
        "OBHHBBBSSO",
        "OBHBBBBSSO",
        "OBHBBBBSSO",
        "OBBBBBBSSO",
        "OBBBBBBSSO",
        ".OBBBBBSO.",
        "..OBBBSO..",
        "...OOOO...",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 10, 12, PEP, CM)
    # Stem
    for x, y in [(15, 9), (16, 9), (15, 10)]:
        put(px, x, y, GR)
    put(px, 15, 8, GR_HI)
    return img


def bellpepper_cooked():
    """Roasted pepper strips."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (120,  20,  10, 255)
    B  = (180,  50,  30, 255)
    HI = (220,  90,  50, 255)
    OL = ( 50,   8,   4, 255)
    strips = [(8, 18), (12, 16), (16, 18), (20, 16), (10, 22), (16, 22)]
    for x, y in strips:
        for dx in range(6):
            put(px, x + dx, y, OL)
            put(px, x + dx, y + 1, B)
            put(px, x + dx, y + 2, OL)
    return img


# Per-crop seed colors for the generic seed helper
SEED_COLORS = {
    'cabbage':    ((30, 70, 20), (80, 140, 50), (130, 200, 80)),
    'lettuce':    ((40, 80, 30), (110, 160, 60), (170, 210, 100)),
    'garlic':     ((100, 90, 70), (180, 170, 150), (230, 220, 200)),
    'beans':      ((30, 80, 30), (80, 150, 60), (130, 200, 100)),
    'peas':       ((40, 90, 30), (100, 170, 70), (160, 220, 110)),
    'corn':       ((200, 160, 20), (250, 220, 60), (255, 240, 140)),
    'carrot':     ((180, 60, 10), (240, 110, 30), (255, 160, 80)),
    'cucumber':   ((30, 80, 30), (80, 150, 60), (140, 200, 90)),
    'bellpepper': ((140, 20, 8), (210, 40, 30), (240, 80, 50)),
}


# ===========================================================
# DRIVER — emit everything
# ===========================================================

JOBS = [
    # (folder, name, draw_fn)
    # A — Wheat chain
    ("wheat_chain", "wheat",  wheat),
    ("wheat_chain", "flour",  flour),
    ("wheat_chain", "dough",  dough),
    ("wheat_chain", "bread",  bread),
    # B — Cheese
    ("cheese",      "block",     cheese_block),
    ("cheese",      "shredded",  cheese_shredded),
    # C — Meats
    ("meat",        "chicken_raw",    chicken_raw),
    ("meat",        "chicken_cooked", chicken_cooked),
    ("meat",        "beef_raw",       beef_raw),
    ("meat",        "beef_cooked",    beef_cooked),
    ("meat",        "pork_raw",       pork_raw),
    ("meat",        "pork_cooked",    pork_cooked),
    ("meat",        "fish_raw",       fish_raw),
    ("meat",        "fish_cooked",    fish_cooked),
    # D — Eggs
    ("eggs",        "egg_raw",     egg_raw),
    ("eggs",        "egg_fried",   egg_fried),
    ("eggs",        "egg_boiled",  egg_boiled),
    # E — Tier-1 veg (existing crops get crop+cooked)
    ("veg_potato",   "potato_crop",   potato_raw),
    ("veg_potato",   "potato_cooked", potato_cooked),
    ("veg_onion",    "onion_crop",    onion_raw),
    ("veg_onion",    "onion_cooked",  onion_cooked),
    ("veg_tomato",   "tomato_crop",   tomato_raw),
    ("veg_tomato",   "tomato_cooked", tomato_cooked),
    # E continued — 9 new vegetables
    ("veg_cabbage",  "cabbage_crop",   cabbage_crop),
    ("veg_cabbage",  "cabbage_cooked", cabbage_cooked),
    ("veg_lettuce",  "lettuce_crop",   lettuce_crop),
    ("veg_lettuce",  "lettuce_cooked", lettuce_cooked),
    ("veg_garlic",   "garlic_crop",    garlic_crop),
    ("veg_garlic",   "garlic_cooked",  garlic_cooked),
    ("veg_beans",    "beans_crop",     beans_crop),
    ("veg_beans",    "beans_cooked",   beans_cooked),
    ("veg_peas",     "peas_crop",      peas_crop),
    ("veg_peas",     "peas_cooked",    peas_cooked),
    ("veg_corn",     "corn_crop",      corn_crop),
    ("veg_corn",     "corn_cooked",    corn_cooked),
    ("veg_carrot",   "carrot_crop",    carrot_crop),
    ("veg_carrot",   "carrot_cooked", carrot_cooked),
    ("veg_cucumber", "cucumber_crop", cucumber_crop),
    ("veg_cucumber", "cucumber_cooked", cucumber_cooked),
    ("veg_bellpepper","bellpepper_crop", bellpepper_crop),
    ("veg_bellpepper","bellpepper_cooked", bellpepper_cooked),
]

if __name__ == "__main__":
    for folder, name, fn in JOBS:
        out = f"/home/sparky/ogrs/art/items/{folder}"
        os.makedirs(out, exist_ok=True)
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {folder}/{name}")

    # Also generate seeds for new crops
    for crop in ('cabbage', 'lettuce', 'garlic', 'beans', 'peas', 'corn', 'carrot', 'cucumber', 'bellpepper'):
        dk, b, hi = SEED_COLORS[crop]
        img = seed_generic((*dk, 255), (*b, 255), (*hi, 255))
        out = f"/home/sparky/ogrs/art/items/veg_{crop}"
        os.makedirs(out, exist_ok=True)
        img.save(f"{out}/{crop}_seed.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{crop}_seed_x8.png")
        print(f"done: veg_{crop}/{crop}_seed")

    print("\n=== Phase 1 complete ===")
