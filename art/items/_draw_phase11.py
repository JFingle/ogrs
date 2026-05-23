#!/usr/bin/env python3
"""
Phase 11 — Food/farming completion (15 sprites at 32×32).

Closes the remaining gaps to fully cover FOOD_AND_FARMING.md:

  A. Missing Tier-3 dishes: Caesar Salad, Spaghetti Bolognese
  B. Potions (9): Greenkeeper, Flower-based, Sacred
  C. Farming tools: Rake, Compost (replacing tinted fallbacks)
  D. Cookbooks: Basic, Master Chef Tome (recipe-discovery items)
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


BOWL_O = (30, 18, 8, 255)
BOWL_DK = (70, 46, 24, 255)
BOWL_B = (138, 90, 46, 255)
BOWL_HI = (200, 150, 90, 255)


# ===========================================================
# A. MISSING TIER-3 DISHES
# ===========================================================

def caesar_salad():
    """Caesar salad — lettuce + croutons + parmesan + dressing in bowl."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    LETTUCE_DK = (40, 90, 30, 255)
    LETTUCE_B  = (90, 160, 60, 255)
    LETTUCE_HI = (140, 220, 100, 255)
    CROUTON_DK = (140, 90, 40, 255)
    CROUTON_B  = (210, 160, 90, 255)
    PARMESAN = (255, 250, 220, 255)
    DRESSING = (240, 220, 160, 255)
    OL = (30, 18, 8, 255)
    # Wide shallow bowl
    BOWL = [
        ".OOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBHBO",
        "OBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI}
    stamp(px, 8, 21, BOWL, CM)
    # Lettuce leaves piled high
    leaves = [(11, 13), (15, 11), (19, 13), (13, 16), (17, 16), (12, 18), (20, 18), (15, 14), (18, 15)]
    for cx, cy in leaves:
        put(px, cx, cy, LETTUCE_DK)
        put(px, cx + 1, cy, LETTUCE_HI)
        put(px, cx + 2, cy, LETTUCE_B)
        put(px, cx, cy + 1, LETTUCE_B)
        put(px, cx + 1, cy + 1, LETTUCE_DK)
    # Croutons (golden cubes)
    for cx, cy in [(13, 15), (17, 14), (15, 18)]:
        put(px, cx, cy, CROUTON_B)
        put(px, cx + 1, cy, CROUTON_DK)
        put(px, cx, cy + 1, CROUTON_DK)
    # Parmesan shavings
    for x, y in [(12, 14), (16, 13), (20, 16)]:
        put(px, x, y, PARMESAN)
    # Dressing drizzle
    for x in range(13, 21):
        put(px, x, 19, DRESSING)
    return img


def spaghetti_bolognese():
    """Spaghetti Bolognese — pasta with red meat sauce, basil garnish."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PASTA_DK = (160, 120, 60, 255)
    PASTA_B  = (220, 190, 130, 255)
    PASTA_HI = (250, 230, 180, 255)
    SAUCE_DK = (110, 20, 10, 255)
    SAUCE_B  = (180, 40, 30, 255)
    SAUCE_HI = (220, 70, 50, 255)
    MEAT     = (140, 70, 40, 255)
    BASIL    = (90, 160, 50, 255)
    PARMESAN = (255, 250, 220, 255)
    OL = (30, 18, 8, 255)
    # Plate
    PLATE = [
        ".OOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBHBO",
        "OBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI}
    stamp(px, 8, 21, PLATE, CM)
    # Spaghetti nest (wavy yellow strands)
    for x in range(11, 22):
        wave = int(math.sin(x * 0.7) * 1)
        put(px, x, 16 + wave, PASTA_B)
        put(px, x, 15 + wave, PASTA_HI)
        put(px, x, 17 + wave, PASTA_DK)
    for x in range(12, 21):
        wave = int(math.cos(x * 0.5) * 1)
        put(px, x, 13 + wave, PASTA_B)
        put(px, x, 14 + wave, PASTA_HI)
    # Sauce mound on top (red blob)
    for cx, cy in [(13, 13), (15, 12), (18, 13), (16, 15), (19, 16)]:
        put(px, cx, cy, SAUCE_B)
        put(px, cx + 1, cy, SAUCE_DK)
        put(px, cx, cy + 1, SAUCE_HI)
    # Meat chunks visible
    for x, y in [(14, 14), (17, 14), (16, 16)]:
        put(px, x, y, MEAT)
    # Basil garnish
    put(px, 16, 11, BASIL)
    put(px, 17, 11, BASIL)
    # Parmesan shavings
    for x, y in [(13, 12), (20, 13), (15, 17)]:
        put(px, x, y, PARMESAN)
    return img


# ===========================================================
# B. POTIONS
# ===========================================================

def _vial_outline(px, cork_color=(90, 60, 20, 255)):
    """Draw the standard small potion vial shape. Caller fills the liquid."""
    OL = (30, 30, 50, 255)
    GLASS = (200, 220, 230, 255)
    # Cork
    put(px, 14, 8, cork_color); put(px, 15, 8, cork_color); put(px, 16, 8, cork_color); put(px, 17, 8, cork_color)
    put(px, 14, 9, cork_color); put(px, 17, 9, cork_color)
    # Neck
    put(px, 13, 10, OL); put(px, 14, 10, GLASS); put(px, 15, 10, GLASS); put(px, 16, 10, GLASS); put(px, 17, 10, GLASS); put(px, 18, 10, OL)
    put(px, 13, 11, OL); put(px, 14, 11, GLASS); put(px, 15, 11, GLASS); put(px, 16, 11, GLASS); put(px, 17, 11, GLASS); put(px, 18, 11, OL)
    # Shoulder transition
    put(px, 12, 12, OL); put(px, 13, 12, GLASS); put(px, 14, 12, GLASS); put(px, 15, 12, GLASS); put(px, 16, 12, GLASS); put(px, 17, 12, GLASS); put(px, 18, 12, GLASS); put(px, 19, 12, OL)
    # Body sides (rows 13-23)
    for y in range(13, 24):
        put(px, 12, y, OL)
        put(px, 19, y, OL)
    # Bottom
    put(px, 13, 24, OL); put(px, 18, 24, OL)
    for x in range(13, 19):
        put(px, x, 25, OL)


def _fill_vial(px, liquid_top_y, dk_color, base_color, hi_color, sparkle_color=None):
    """Fill the vial body with liquid."""
    # Body is x:13-18, y:liquid_top_y to 24
    for y in range(liquid_top_y, 24):
        for x in range(13, 19):
            if y == liquid_top_y:
                put(px, x, y, hi_color)
            elif x == 13:
                put(px, x, y, dk_color)
            elif x == 18:
                put(px, x, y, dk_color)
            else:
                put(px, x, y, base_color)
    if sparkle_color:
        # Add a small sparkle on the highlight side
        put(px, 14, liquid_top_y + 2, sparkle_color)


# --- Greenkeeper potions ---

def sturdy_tonic():
    """Sturdy Tonic — defense buff, brown rooty potion."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    _vial_outline(px)
    _fill_vial(px, liquid_top_y=14,
               dk_color=(90, 60, 20, 255),
               base_color=(140, 90, 30, 255),
               hi_color=(190, 130, 50, 255))
    return img


def hot_sauce_burner():
    """Hot Sauce Burner — attack/strength, red bubbling potion."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    _vial_outline(px)
    _fill_vial(px, liquid_top_y=14,
               dk_color=(130, 20, 10, 255),
               base_color=(220, 40, 30, 255),
               hi_color=(250, 90, 50, 255),
               sparkle_color=(255, 200, 100, 255))
    return img


def veggie_smoothie():
    """Veggie Smoothie — energy boost, green chunky."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    _vial_outline(px)
    _fill_vial(px, liquid_top_y=14,
               dk_color=(40, 90, 30, 255),
               base_color=(90, 160, 60, 255),
               hi_color=(140, 220, 100, 255))
    # Small chunks
    put(px, 15, 18, (110, 50, 20, 255))  # carrot chunk
    put(px, 16, 21, (220, 60, 60, 255))  # tomato chunk
    return img


# --- Flower potions ---

def moonlit_sight():
    """Moonlit Sight — night vision, pale silver-blue glow."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 15, y - 18
            d2 = dx * dx + dy * dy
            if 40 <= d2 <= 90 and (x + y) % 2 == 0:
                put(px, x, y, (200, 220, 255, 90))
    _vial_outline(px, cork_color=(80, 80, 100, 255))
    _fill_vial(px, liquid_top_y=14,
               dk_color=(80, 100, 160, 255),
               base_color=(160, 200, 240, 255),
               hi_color=(220, 240, 255, 255),
               sparkle_color=(255, 255, 255, 255))
    return img


def solar_charge():
    """Solar Charge — magic boost, golden glowing."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 15, y - 18
            d2 = dx * dx + dy * dy
            if 40 <= d2 <= 100 and (x + y) % 2 == 0:
                put(px, x, y, (255, 220, 100, 110))
    _vial_outline(px)
    _fill_vial(px, liquid_top_y=14,
               dk_color=(180, 130, 20, 255),
               base_color=(240, 190, 50, 255),
               hi_color=(255, 230, 100, 255),
               sparkle_color=(255, 255, 255, 255))
    return img


def mandrake_healing():
    """Mandrake Healing — full restore, deep red potion."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Halo (red)
    for x in range(W):
        for y in range(H):
            dx, dy = x - 15, y - 18
            d2 = dx * dx + dy * dy
            if 40 <= d2 <= 100 and (x + y) % 2 == 0:
                put(px, x, y, (255, 100, 100, 100))
    _vial_outline(px)
    _fill_vial(px, liquid_top_y=14,
               dk_color=(100, 10, 20, 255),
               base_color=(180, 20, 40, 255),
               hi_color=(240, 60, 80, 255),
               sparkle_color=(255, 200, 200, 255))
    return img


# --- Sacred potions (with golden halos) ---

def anointing_oil_vial():
    """Anointing oil — golden olive oil with cross stopper."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Golden halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 15, y - 18
            d2 = dx * dx + dy * dy
            if 40 <= d2 <= 100 and (x + y) % 2 == 0:
                put(px, x, y, (255, 240, 180, 110))
    _vial_outline(px, cork_color=(120, 80, 30, 255))
    _fill_vial(px, liquid_top_y=14,
               dk_color=(160, 110, 20, 255),
               base_color=(220, 170, 50, 255),
               hi_color=(250, 220, 110, 255))
    # Tiny cross on top of cork
    put(px, 15, 7, (255, 240, 200, 255))
    put(px, 16, 7, (255, 240, 200, 255))
    put(px, 15, 6, (255, 240, 200, 255))
    put(px, 16, 6, (255, 240, 200, 255))
    return img


def fig_honey_tonic():
    """Fig + Honey Tonic — amber sweet potion with fig leaf on side."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Golden halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 15, y - 18
            d2 = dx * dx + dy * dy
            if 50 <= d2 <= 95 and (x + y) % 2 == 0:
                put(px, x, y, (255, 240, 180, 90))
    _vial_outline(px, cork_color=(100, 60, 20, 255))
    _fill_vial(px, liquid_top_y=14,
               dk_color=(140, 90, 20, 255),
               base_color=(220, 150, 50, 255),
               hi_color=(255, 200, 90, 255))
    # Fig seed at bottom
    put(px, 15, 22, (140, 30, 60, 255))
    return img


def blessed_water():
    """Blessed Water — pure clear with sparkles."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Bright halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 15, y - 18
            d2 = dx * dx + dy * dy
            if 40 <= d2 <= 110 and (x + y) % 2 == 0:
                put(px, x, y, (255, 255, 230, 130))
    _vial_outline(px, cork_color=(200, 200, 200, 255))
    _fill_vial(px, liquid_top_y=14,
               dk_color=(180, 200, 230, 255),
               base_color=(220, 235, 250, 255),
               hi_color=(255, 255, 255, 255),
               sparkle_color=(255, 255, 200, 255))
    # Extra sparkles in liquid
    put(px, 16, 17, (255, 255, 255, 255))
    put(px, 14, 20, (255, 255, 255, 255))
    put(px, 17, 22, (255, 255, 255, 255))
    return img


# ===========================================================
# C. FARMING TOOLS (replace tinted fallbacks)
# ===========================================================

def rake():
    """Garden rake — long wooden handle + iron teeth."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    WOOD_DK = (90, 60, 30, 255)
    WOOD_B  = (160, 110, 60, 255)
    WOOD_HI = (220, 170, 100, 255)
    IRON_DK = (60, 60, 70, 255)
    IRON_B  = (140, 140, 150, 255)
    IRON_HI = (200, 200, 210, 255)
    OL = (30, 20, 10, 255)
    # Diagonal handle (upper-right to lower-left)
    for i in range(20):
        x = 6 + i
        y = 24 - i
        put(px, x, y, WOOD_B)
        put(px, x + 1, y, WOOD_HI)
        put(px, x, y + 1, WOOD_DK)
        put(px, x - 1, y - 1, OL)
        put(px, x + 1, y + 1, OL)
    # Top end (grip)
    put(px, 6, 24, WOOD_DK)
    put(px, 5, 25, OL)
    # Rake head at top
    for x in range(20, 28):
        put(px, x, 3, OL)
        put(px, x, 4, IRON_B)
        put(px, x, 5, IRON_HI)
        put(px, x, 6, IRON_DK)
        put(px, x, 7, OL)
    # Teeth (sticking down)
    for x in (20, 22, 24, 26):
        put(px, x, 8, IRON_DK)
        put(px, x, 9, OL)
    return img


def compost():
    """Compost — pile of dark earthy material with worm specks."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (40, 30, 10, 255)
    B  = (80, 60, 30, 255)
    HI = (130, 100, 60, 255)
    WORM = (180, 80, 80, 255)
    LEAF = (90, 130, 40, 255)
    OL = (20, 14, 8, 255)
    PILE = [
        "....OOOOOOOO....",
        "..OOBBBBBBBBOO..",
        ".OBBHHBBBBBBBSO.",
        ".OBHHBBBBBBBBSO.",
        "OBHHBBBBBBBBBSSO",
        "OBHBBBBBBBBBBSSO",
        "OBBBBBBBBBBBBSSO",
        "OBBBBBBBBBBBSSSO",
        ".OBBBBBBBBBBSSO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 8, 13, PILE, CM)
    # Worm visible (pink)
    for x, y in [(13, 17), (14, 17), (15, 18), (16, 18)]:
        put(px, x, y, WORM)
    # Decomposing leaves
    for x, y in [(11, 16), (19, 17), (16, 19)]:
        put(px, x, y, LEAF)
    return img


# ===========================================================
# D. COOKBOOKS
# ===========================================================

def cookbook_basic():
    """Basic Cookbook — small leather-bound book with recipe icon."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    COVER_DK = (90, 30, 20, 255)
    COVER_B  = (160, 60, 40, 255)
    COVER_HI = (210, 100, 70, 255)
    PAGES = (245, 230, 200, 255)
    SPINE = (50, 20, 10, 255)
    GOLD = (240, 200, 80, 255)
    OL = (30, 10, 8, 255)
    BOOK = [
        ".OOOOOOOOOOOOOO.",
        "OBHHHHHHHHHHHHBO",
        "OBHCBBBBBBBBBHBO",   # C = spine
        "OBHCBBBBBBBBBHBO",
        "OBHCBBBBBBBBBHBO",
        "OBHCBBBBBBBBBHBO",
        "OBHCBBBBBBBBBHBO",
        "OBHCBBBBBBBBBHBO",
        "OBHHHHHHHHHHHHBO",
        ".OOOOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': COVER_B, 'H': COVER_HI, 'C': SPINE}
    stamp(px, 8, 11, BOOK, CM)
    # Title etching (small fork+knife icon center)
    for x, y in [(15, 15), (15, 16), (16, 15), (16, 16), (17, 15), (17, 16)]:
        put(px, x, y, GOLD)
    put(px, 16, 14, GOLD)  # fork tip
    return img


def cookbook_master():
    """Master Chef Tome — bigger ornate book with gold trim + gem."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    COVER_DK = (40, 20, 80, 255)
    COVER_B  = (80, 50, 160, 255)
    COVER_HI = (140, 100, 220, 255)
    GOLD_DK = (160, 110, 20, 255)
    GOLD = (240, 200, 80, 255)
    GOLD_HI = (255, 230, 130, 255)
    GEM = (220, 30, 30, 255)
    SPINE = (30, 10, 50, 255)
    OL = (14, 8, 30, 255)
    BOOK = [
        "OOOOOOOOOOOOOOOO",
        "OHHHHHHHHHHHHHHO",
        "OHGBBBBBBBBBBGHO",
        "OHCBBBBBBBBBBCHO",
        "OHCBBBBBBBBBBCHO",
        "OHCBBBBSBBBBBCHO",   # S = gem slot
        "OHCBBBBBBBBBBCHO",
        "OHCBBBBBBBBBBCHO",
        "OHGBBBBBBBBBBGHO",
        "OHHHHHHHHHHHHHHO",
        "OOOOOOOOOOOOOOOO",
    ]
    CM = {'O': OL, 'B': COVER_B, 'H': COVER_HI, 'C': SPINE, 'G': GOLD, 'S': COVER_DK}
    stamp(px, 8, 10, BOOK, CM)
    # Central gem (ruby)
    put(px, 16, 15, GEM)
    put(px, 15, 15, GOLD_HI)
    put(px, 17, 15, GOLD_DK)
    # Gold corner ornaments
    for x, y in [(9, 11), (22, 11), (9, 19), (22, 19)]:
        put(px, x, y, GOLD)
    return img


# ===========================================================
# DRIVER
# ===========================================================
JOBS = [
    # A. Missing Tier-3 dishes
    ("dishes",          "caesar_salad",         caesar_salad),
    ("dishes",          "spaghetti_bolognese",  spaghetti_bolognese),
    # B. Potions — Greenkeeper
    ("potions",         "sturdy_tonic",         sturdy_tonic),
    ("potions",         "hot_sauce_burner",     hot_sauce_burner),
    ("potions",         "veggie_smoothie",      veggie_smoothie),
    # B. Potions — Flower
    ("potions",         "moonlit_sight",        moonlit_sight),
    ("potions",         "solar_charge",         solar_charge),
    ("potions",         "mandrake_healing",     mandrake_healing),
    # B. Potions — Sacred
    ("potions",         "anointing_oil_vial",   anointing_oil_vial),
    ("potions",         "fig_honey_tonic",      fig_honey_tonic),
    ("potions",         "blessed_water",        blessed_water),
    # C. Farming tools
    ("farming_tools",   "rake",                 rake),
    ("farming_tools",   "compost",              compost),
    # D. Cookbooks
    ("cookbooks",       "cookbook_basic",       cookbook_basic),
    ("cookbooks",       "cookbook_master",      cookbook_master),
]

if __name__ == "__main__":
    for folder, name, fn in JOBS:
        out = f"/home/sparky/ogrs/art/items/{folder}"
        os.makedirs(out, exist_ok=True)
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {folder}/{name}")
    print(f"\n=== Phase 11 complete: {len(JOBS)} sprites ===")
