#!/usr/bin/env python3
"""
Phase 4 — Tier-4 cooked dishes (complex 6-7 ingredient dishes, 25-35 HP).

8 plated dishes at 32×32:
  Biryani, Pad Thai, Coq au Vin, Mole, Pho, Shepherd's Pie, Tagine, Kimchi Stew

Each should read as more complex than Tier-3 — extra colors, garnishes,
plates feel more loaded.
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


BOWL_O   = ( 30,  18,   8, 255)
BOWL_DK  = ( 70,  46,  24, 255)
BOWL_B   = (138,  90,  46, 255)
BOWL_HI  = (200, 150,  90, 255)
PLATE_DK = (180, 180, 190, 255)
PLATE_B  = (230, 230, 235, 255)


def draw_bowl(px, top_y=12, bottom_y=24):
    """Generic brown bowl outline."""
    rows = [
        "..OOOOOOOOOOOO..",
        ".OBHBBBBBBBBHBO.",
        "OBBBBBBBBBBBBBBO",
        "OBHBCCCCCCCCBHBO",  # C = content slot
        "OBHCCCCCCCCCCHBO",
        "OBBBCCCCCCCCCBBO",
        "OBBBCCCCCCCCCBBO",
        ".OBBCCCCCCCCBBO.",
        "..OBBBBBBBBBBO..",
        "...OOOOOOOOOO...",
    ]
    return rows


# ===========================================================
# Biryani — saffron rice with chicken + spice
# ===========================================================
def biryani():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    RICE_W = (250, 245, 230, 255)
    RICE_Y = (240, 220, 100, 255)
    RICE_O = (220, 180,  60, 255)
    CHICKEN = (200, 140,  60, 255)
    CHICKEN_HI = (240, 180, 100, 255)
    HERB = ( 90, 160,  50, 255)
    SPICE = (180,  40,  20, 255)
    PLATE = [
        "..OOOOOOOOOOOOOO..",
        ".OBHBBBBBBBBBBHBO.",
        "OBBBBBBBBBBBBBBBO",
        "OBHYWYWYWYWYWYWBO",  # mixed yellow + white rice
        "OBHWYWYWYWYWYWYBO",
        "OBHYYWYWYWWYWYWBO",
        "OBBWYWYYYYYWYWYBO",
        ".OBBYWYYYYWYWBBO.",
        "..OOBBBBBBBBBOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'Y': RICE_Y, 'W': RICE_W}
    stamp(px, 7, 11, PLATE, CM)
    # Chicken chunks
    for x, y in [(13, 16), (16, 17), (19, 16)]:
        put(px, x, y, CHICKEN)
        put(px, x + 1, y, CHICKEN_HI)
        put(px, x, y + 1, CHICKEN)
    # Spice flecks (cardamom, cloves)
    for x, y in [(11, 15), (15, 16), (21, 15), (14, 18)]:
        put(px, x, y, SPICE)
    # Herb garnish
    for x, y in [(15, 14), (18, 14), (12, 17)]:
        put(px, x, y, HERB)
    return img


# ===========================================================
# Pad Thai — noodles with shrimp, peanut, lime
# ===========================================================
def pad_thai():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    NOODLE = (240, 200, 100, 255)
    NOODLE_DK = (180, 140,  60, 255)
    SHRIMP = (240, 110,  90, 255)
    SHRIMP_HI = (255, 160, 140, 255)
    PEANUT = (220, 180, 110, 255)
    LIME   = (140, 200,  60, 255)
    EGG_Y  = (250, 200,  80, 255)
    HERB   = ( 90, 160,  50, 255)
    # Wider shallow plate
    PLATE = [
        ".OOOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBBHBO",
        "OBNNNNNNNNNNNNNBO",  # noodles
        "OBNDNDNDNDNDNDBNO",
        "OBNNNNNNNNNNNNNBO",
        "OBNDNDNDNDNDNDBNO",
        "OBNNNNNNNNNNNNNBO",
        ".OBBBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'N': NOODLE, 'D': NOODLE_DK}
    stamp(px, 7, 12, PLATE, CM)
    # Shrimp on top
    for x, y in [(12, 16), (19, 17)]:
        put(px, x, y, SHRIMP)
        put(px, x + 1, y, SHRIMP_HI)
        put(px, x, y + 1, SHRIMP)
    # Peanut crumbles scattered
    for x, y in [(14, 17), (17, 18), (21, 16)]:
        put(px, x, y, PEANUT)
    # Lime wedge
    put(px, 22, 17, LIME)
    put(px, 23, 17, LIME)
    # Cilantro
    put(px, 16, 15, HERB)
    put(px, 18, 16, HERB)
    return img


# ===========================================================
# Coq au Vin — chicken in red wine sauce with mushrooms
# ===========================================================
def coq_au_vin():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    WINE_DK = (100,  20,  30, 255)
    WINE_B  = (160,  30,  50, 255)
    WINE_HI = (200,  60,  80, 255)
    CHICKEN_DK = (140,  90,  40, 255)
    CHICKEN_B  = (210, 150,  80, 255)
    MUSH_DK = ( 80,  50,  30, 255)
    MUSH_B  = (140, 100,  60, 255)
    CARROT  = (240, 130,  40, 255)
    HERB    = ( 90, 160,  50, 255)
    BOWL = [
        ".OOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBHBO",
        "OBBWWWWWWWWWWBBO",  # wine sauce
        "OBWWWWWWWWWWWWBO",
        "OBWWWWWWWWWWWWBO",
        "OBWWWWWWWWWWWWBO",
        ".OBBWWWWWWWWWBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'W': WINE_B}
    stamp(px, 8, 13, BOWL, CM)
    # Wine highlights
    for x, y in [(12, 17), (18, 17), (15, 18)]:
        put(px, x, y, WINE_HI)
    # Chicken pieces
    for x, y in [(12, 16), (18, 16), (15, 17)]:
        put(px, x, y, CHICKEN_DK)
        put(px, x + 1, y, CHICKEN_B)
    # Mushrooms
    for x, y in [(14, 18), (20, 18)]:
        put(px, x, y, MUSH_DK)
        put(px, x + 1, y, MUSH_B)
    # Carrot bits
    for x, y in [(11, 18), (21, 17)]:
        put(px, x, y, CARROT)
    # Herb
    put(px, 16, 16, HERB)
    return img


# ===========================================================
# Mole — chocolate-chili sauce over chicken
# ===========================================================
def mole():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SAUCE_DK = ( 50,  20,  10, 255)
    SAUCE_B  = (100,  50,  20, 255)
    SAUCE_HI = (160,  90,  40, 255)
    CHICKEN_DK = (160, 100,  50, 255)
    CHICKEN_B  = (220, 160,  90, 255)
    SEED     = (250, 240, 200, 255)
    HERB     = ( 90, 160,  50, 255)
    SPICE    = (180,  40,  20, 255)
    BOWL = [
        ".OOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBHBO",
        "OBBSSSSSSSSSSBBO",
        "OBSSSSSSSSSSSSBO",
        "OBSSSSSSSSSSSSBO",
        ".OBBSSSSSSSSSBBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'S': SAUCE_B}
    stamp(px, 8, 14, BOWL, CM)
    # Sauce highlights (chocolate sheen)
    for x, y in [(13, 17), (18, 17), (15, 18)]:
        put(px, x, y, SAUCE_HI)
    # Chicken pieces visible through sauce
    for x, y in [(13, 16), (17, 16), (15, 17)]:
        put(px, x, y, CHICKEN_DK)
        put(px, x + 1, y, CHICKEN_B)
    # Sesame seeds garnish
    for x, y in [(14, 17), (18, 18), (12, 18), (20, 17)]:
        put(px, x, y, SEED)
    # Cilantro
    put(px, 16, 16, HERB)
    # Red chili fleck
    put(px, 19, 17, SPICE)
    return img


# ===========================================================
# Pho — Vietnamese noodle soup
# ===========================================================
def pho():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BROTH_DK = (140,  90,  40, 255)
    BROTH_B  = (200, 140,  60, 255)
    BROTH_HI = (240, 180,  80, 255)
    NOODLE = (250, 245, 230, 255)
    BEEF_DK = (130,  40,  30, 255)
    BEEF_B  = (200,  80,  60, 255)
    LIME = (140, 200,  60, 255)
    HERB = ( 90, 160,  50, 255)
    BASIL = ( 60, 130,  40, 255)
    BOWL = [
        "..OOOOOOOOOOOOOO..",
        ".OBHBBBBBBBBBBHBO.",
        "OBBHHHHHHHHHHHHBO",
        "OBHRRRRRRRRRRRHBO",  # R = broth
        "OBHRRRRRRRRRRRHBO",
        "OBHRRRRRRRRRRRHBO",
        "OBBRRRRRRRRRRRBBO",
        ".OBBRRRRRRRRRBBO.",
        "..OOOOOOOOOOOO...",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'R': BROTH_B}
    stamp(px, 7, 12, BOWL, CM)
    # Noodles floating
    for x in range(11, 22, 2):
        put(px, x, 18, NOODLE)
    for x in range(12, 21, 2):
        put(px, x, 17, NOODLE)
    # Beef slices
    for x, y in [(13, 16), (17, 16)]:
        put(px, x, y, BEEF_B)
        put(px, x + 1, y, BEEF_DK)
    # Lime wedge
    put(px, 21, 16, LIME)
    # Basil leaves
    put(px, 15, 15, BASIL)
    put(px, 19, 15, BASIL)
    # Broth highlights (steam glimmer)
    for x, y in [(14, 18), (18, 19)]:
        put(px, x, y, BROTH_HI)
    return img


# ===========================================================
# Shepherd's Pie — meat under mashed potato top
# ===========================================================
def shepherds_pie():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DISH_DK = ( 90,  60,  30, 255)
    DISH_B  = (160, 110,  60, 255)
    POTATO_DK = (200, 180, 120, 255)
    POTATO_B  = (250, 230, 170, 255)
    POTATO_HI = (255, 245, 200, 255)
    MEAT_DK = ( 90,  40,  20, 255)
    MEAT_B  = (160,  80,  40, 255)
    CARROT = (240, 130,  40, 255)
    PEAS   = (110, 180,  70, 255)
    # Square baking dish
    DISH = [
        "OOOOOOOOOOOOOOOO",
        "OPPPPPPPPPPPPPPO",  # P = potato top
        "OPHPPHPPHPPHPPPO",
        "OPMMMMMMMMMMMMPO",  # M = meat layer
        "OPMRMMMPMMRMMMPO",  # R = carrot, P/G visible
        "OPMMMGMMMGMMMMPO",  # G = peas
        "OBBMMMMMMMMMMBBO",
        ".OOOOOOOOOOOOOO.",
    ]
    CM = {'O': DISH_DK, 'B': DISH_B, 'P': POTATO_B, 'H': POTATO_HI, 'M': MEAT_B,
          'R': CARROT, 'G': PEAS}
    stamp(px, 8, 13, DISH, CM)
    # Fork ridges in potato top
    for x in range(9, 23, 2):
        put(px, x, 14, POTATO_DK)
    return img


# ===========================================================
# Tagine — Moroccan slow-cooked stew with apricots
# ===========================================================
def tagine():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    POT_DK = ( 90,  50,  20, 255)
    POT_B  = (160,  90,  40, 255)
    POT_HI = (210, 140,  70, 255)
    LID_DK = ( 70,  40,  10, 255)
    LID_B  = (140,  80,  30, 255)
    STEW = (200, 130,  50, 255)
    APRICOT = (240, 150,  60, 255)
    LAMB = (130,  60,  40, 255)
    OLIVE = ( 80,  60,  40, 255)
    HERB = ( 90, 160,  50, 255)
    # Tagine shape — distinctive cone-shaped lid + wide round base
    # Bottom dish
    DISH = [
        "...OOOOOOOOOOO...",
        "..OBHBBBBBBBBHBO..",
        ".OBBHBBBBBBBBBHBO.",
        "OBBSSSSSSSSSSSBBO",  # S = stew interior
        "OBSSSSSSSSSSSSSBO",
        ".OBBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOOO..",
    ]
    CM = {'O': POT_DK, 'B': POT_B, 'H': POT_HI, 'S': STEW}
    stamp(px, 7, 17, DISH, CM)
    # Conical lid above
    for y in range(11, 17):
        half_w = 8 - (16 - y)
        for x in range(16 - half_w, 17 + half_w):
            put(px, x, y, LID_B)
        put(px, 16 - half_w - 1, y, LID_DK)
        put(px, 17 + half_w, y, LID_DK)
    # Knob at top
    put(px, 16, 9, LID_DK)
    put(px, 15, 10, LID_DK)
    put(px, 17, 10, LID_DK)
    put(px, 16, 10, LID_B)
    # Visible chunks (since lid is open at this angle — stylized)
    for x, y in [(12, 19), (17, 19), (15, 20)]:
        put(px, x, y, LAMB)
    for x, y in [(13, 20), (19, 20), (16, 21)]:
        put(px, x, y, APRICOT)
    return img


# ===========================================================
# Kimchi Stew — bubbling red stew with kimchi, pork, tofu
# ===========================================================
def kimchi_stew():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    STEW_DK = (140,  20,  10, 255)
    STEW_B  = (210,  50,  30, 255)
    STEW_HI = (250,  90,  60, 255)
    KIM_DK = (140,  60,  20, 255)
    KIM_B  = (200, 110,  50, 255)
    TOFU = (250, 245, 220, 255)
    PORK = (130,  60,  40, 255)
    SCALL = ( 90, 160,  50, 255)
    BOWL = [
        ".OOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBHBO",
        "OBBSSSSSSSSSSBBO",
        "OBSSSSSSSSSSSSBO",
        "OBSSSSSSSSSSSSBO",
        "OBSSSSSSSSSSSSBO",
        ".OBBSSSSSSSSSBBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'S': STEW_B}
    stamp(px, 8, 13, BOWL, CM)
    # Steam/highlight bubbles
    for x, y in [(12, 16), (18, 17), (15, 18), (20, 16)]:
        put(px, x, y, STEW_HI)
    # Kimchi pieces (red-orange)
    for x, y in [(13, 16), (17, 16), (15, 17)]:
        put(px, x, y, KIM_B)
        put(px, x + 1, y, KIM_DK)
    # Tofu cubes (white)
    for x, y in [(11, 17), (19, 18)]:
        put(px, x, y, TOFU)
        put(px, x + 1, y, TOFU)
        put(px, x, y + 1, TOFU)
        put(px, x + 1, y + 1, TOFU)
    # Pork bits
    put(px, 15, 18, PORK)
    put(px, 20, 17, PORK)
    # Scallion garnish on top
    for x, y in [(13, 15), (18, 15), (16, 14)]:
        put(px, x, y, SCALL)
    return img


# ===========================================================
# DRIVER
# ===========================================================
DISHES = [
    ("biryani",         biryani),
    ("pad_thai",        pad_thai),
    ("coq_au_vin",      coq_au_vin),
    ("mole",            mole),
    ("pho",             pho),
    ("shepherds_pie",   shepherds_pie),
    ("tagine",          tagine),
    ("kimchi_stew",     kimchi_stew),
]

if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/dishes"
    os.makedirs(out, exist_ok=True)
    for name, fn in DISHES:
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {name}")
    print(f"\n=== Phase 4 complete: {len(DISHES)} Tier-4 dishes ===")
