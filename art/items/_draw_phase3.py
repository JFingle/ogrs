#!/usr/bin/env python3
"""
Phase 3 — Cooked dish icons (plated/served).

10 Tier-3 recipe outputs from FOOD_AND_FARMING.md:
  Pizza Margherita, Lasagna, Ramen, Sushi Roll, Tacos,
  Curry Bowl, Greek Salad, Borscht, Hummus + Pita, Tom Yum

All 32×32 inventory icons. Plate/bowl visible where appropriate so the
viewer reads "this is a finished dish" not "this is an ingredient."
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


# Shared palette pieces
PLATE_DK  = (180, 180, 190, 255)
PLATE_B   = (230, 230, 235, 255)
PLATE_HI  = (255, 255, 255, 255)
BOWL_DK   = ( 70,  46,  24, 255)
BOWL_B    = (138,  90,  46, 255)
BOWL_HI   = (200, 150,  90, 255)
OL        = ( 30,  18,   8, 255)


# ===========================================================
# Pizza Margherita
# ===========================================================
def pizza():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CRUST_DK = (140,  90,  40, 255)
    CRUST_B  = (200, 150,  80, 255)
    CRUST_HI = (240, 200, 130, 255)
    SAUCE_DK = (140,  20,  10, 255)
    SAUCE_B  = (210,  50,  30, 255)
    SAUCE_HI = (240,  90,  60, 255)
    CHEESE   = (255, 250, 220, 255)
    BASIL    = ( 80, 150,  50, 255)
    BASIL_HI = (140, 200,  90, 255)
    OUTLINE  = ( 40,  20,   8, 255)
    # Circular pizza
    PIZZA = [
        "....OOOOOOOO....",
        "..OOBBBBBBBBOO..",
        ".OBHCSSSSSSCHBO.",
        "OBHCSSSSSSSSCHBO",
        "OBHSSSSSSSSSSCHO",
        "OBHSSSSSSSSSSCHO",
        "OBHSSSSSSSSSSCHO",
        "OBHCSSSSSSSSSCHO",
        "OBHCSSSSSSSSCHBO",
        ".OBHCSSSSSSCHBO.",
        "..OOBBBBBBBBOO..",
        "....OOOOOOOO....",
    ]
    CM = {'O': OUTLINE, 'B': CRUST_B, 'H': CRUST_HI, 'S': SAUCE_B, 'C': CHEESE}
    stamp(px, 8, 10, PIZZA, CM)
    # Cheese dollops scattered on sauce
    for x, y in [(13, 14), (17, 14), (15, 16), (12, 17), (19, 17), (16, 19)]:
        put(px, x, y, CHEESE)
    # Sauce highlights
    for x, y in [(14, 15), (18, 16), (13, 18)]:
        put(px, x, y, SAUCE_HI)
    # Basil leaves
    for x, y in [(14, 13), (19, 15), (12, 18), (17, 19)]:
        put(px, x, y, BASIL)
        put(px, x + 1, y, BASIL_HI)
    return img


# ===========================================================
# Lasagna slice
# ===========================================================
def lasagna():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PASTA_DK = (160, 120,  60, 255)
    PASTA_B  = (220, 190, 130, 255)
    PASTA_HI = (250, 230, 180, 255)
    MEAT_DK  = ( 90,  40,  20, 255)
    MEAT_B   = (160,  70,  40, 255)
    CHEESE   = (255, 240, 180, 255)
    SAUCE    = (180,  30,  20, 255)
    OUTLINE  = ( 40,  20,   8, 255)
    # Side-view slice — 5 horizontal layers
    # Top (cheese crust)
    LASAGNA = [
        "OOOOOOOOOOOOOOOO",
        "OCCCCCCCCCCCCCCO",  # cheese top
        "OCHCHCCHCCHCHCCO",
        "OPPPPPPPPPPPPPPO",  # pasta sheet
        "OPHPHPHPHPHPHPPO",
        "OMSMSMSMSMSMSMSO",  # meat + sauce
        "OPPPPPPPPPPPPPPO",  # pasta
        "OPHPHPHPHPHPHPPO",
        "OMSMSMSMSMSMSMSO",  # meat + sauce
        "OPPPPPPPPPPPPPPO",  # pasta bottom
        "OOOOOOOOOOOOOOOO",
    ]
    CM = {'O': OUTLINE, 'P': PASTA_B, 'H': PASTA_HI, 'C': CHEESE, 'M': MEAT_B, 'S': SAUCE}
    stamp(px, 8, 10, LASAGNA, CM)
    return img


# ===========================================================
# Ramen bowl
# ===========================================================
def ramen():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BOWL_O = ( 30,  30,  50, 255)
    BOWL_B = ( 90, 110, 180, 255)
    BOWL_HI = (140, 180, 230, 255)
    BROTH  = (200, 140,  60, 255)
    BROTH_HI = (240, 180,  80, 255)
    NOODLE = (240, 220, 140, 255)
    NOODLE_DK = (180, 150,  70, 255)
    EGG_W  = (250, 250, 240, 255)
    EGG_Y  = (250, 200,  80, 255)
    NORI   = ( 30,  40,  30, 255)
    SCALL  = ( 80, 160,  60, 255)
    # Bowl shape
    BOWL = [
        "..OOOOOOOOOOOO..",
        ".OBHBBBBBBBBHBO.",
        "OBBBBBBBBBBBBBBO",
        "OBHBBBBBBBBBBBHO",
        "OBHBRRRRRRRRBBHO",
        "OBHBRRRRRRRRBBHO",
        ".OBBRRRRRRRRBBO.",
        "..OBRRRRRRRRBO..",
        "...OOBBBBBBOO...",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'R': BROTH}
    stamp(px, 8, 13, BOWL, CM)
    # Noodles squiggling on top of broth
    for x in range(11, 22):
        put(px, x, 18, NOODLE)
        put(px, x, 19, NOODLE_DK)
    for x in range(12, 21):
        put(px, x, 17, NOODLE)
    # Egg half (yellow yolk visible)
    put(px, 12, 19, EGG_W)
    put(px, 13, 19, EGG_W)
    put(px, 12, 20, EGG_Y)
    put(px, 13, 20, EGG_W)
    # Nori sheet (small dark green square)
    put(px, 17, 18, NORI)
    put(px, 18, 18, NORI)
    put(px, 17, 19, NORI)
    put(px, 18, 19, NORI)
    # Scallion bits
    for x, y in [(15, 17), (20, 17), (16, 20)]:
        put(px, x, y, SCALL)
    return img


# ===========================================================
# Sushi roll
# ===========================================================
def sushi():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    NORI_DK = ( 20,  40,  20, 255)
    NORI_B  = ( 40,  70,  40, 255)
    RICE    = (250, 245, 235, 255)
    RICE_DK = (200, 195, 180, 255)
    FISH_DK = (180,  60,  60, 255)
    FISH_B  = (240,  90,  90, 255)
    CUCUMBER= ( 80, 160,  60, 255)
    OUTLINE = ( 10,  20,  10, 255)
    # Two sushi rolls (cylindrical, viewed from end)
    rolls = [(10, 16), (22, 16)]
    for cx, cy in rolls:
        # Outer nori wrap (dark green circle)
        ROLL = [
            "..OOOOO..",
            ".OGGGGGO.",
            "OGRRRRRGO",
            "OGRFFFRGO",
            "OGRFFFRGO",
            "OGRRRRRGO",
            ".OGGGGGO.",
            "..OOOOO..",
        ]
        CM = {'O': OUTLINE, 'G': NORI_B, 'R': RICE, 'F': FISH_B}
        stamp(px, cx - 4, cy - 4, ROLL, CM)
        # Highlight on rice
        put(px, cx - 2, cy - 1, RICE)
        put(px, cx + 2, cy - 1, RICE_DK)
    # Tiny cucumber slice between
    put(px, 16, 16, CUCUMBER)
    put(px, 16, 17, CUCUMBER)
    return img


# ===========================================================
# Tacos
# ===========================================================
def tacos():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SHELL_DK = (180, 130,  50, 255)
    SHELL_B  = (230, 180,  90, 255)
    SHELL_HI = (255, 220, 140, 255)
    MEAT     = (160,  80,  40, 255)
    LETTUCE  = (110, 180,  70, 255)
    TOMATO   = (210,  50,  40, 255)
    CHEESE   = (255, 230, 100, 255)
    OUTLINE  = ( 40,  20,   8, 255)
    # U-shaped folded taco shell
    SHELL = [
        "OOO........OOO",
        "OBHO......OBHO",
        "OBHHOOOOOOBHHO",
        "OBHHHHHHHHHHHO",
        "OBHHHHHHHHHHHO",
        "OBBHHHHHHHHHBO",
        "OBBBHHHHHHHBBO",
        ".OBBBHHHHHBBBO",
        "..OOBBBBBBOOO.",
        ".....OOOOO....",
    ]
    CM = {'O': OUTLINE, 'B': SHELL_B, 'H': SHELL_HI}
    stamp(px, 9, 11, SHELL, CM)
    # Fillings on top — visible above the shell
    # Meat layer
    for x in range(13, 21):
        put(px, x, 14, MEAT)
    # Lettuce strands
    for x, y in [(12, 13), (14, 12), (17, 12), (20, 12), (22, 13)]:
        put(px, x, y, LETTUCE)
    # Tomato chunks
    for x, y in [(15, 13), (19, 13)]:
        put(px, x, y, TOMATO)
    # Cheese sprinkles
    for x, y in [(13, 13), (16, 12), (21, 13)]:
        put(px, x, y, CHEESE)
    return img


# ===========================================================
# Curry bowl
# ===========================================================
def curry():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CURRY_DK = (140,  80,  20, 255)
    CURRY_B  = (210, 140,  40, 255)
    CURRY_HI = (250, 180,  70, 255)
    RICE     = (250, 245, 235, 255)
    GARNISH  = (110, 180,  70, 255)
    # Bowl
    BOWL = [
        "..OOOOOOOOOOOOO..",
        ".OBHHBBBBBBBBHBO.",
        "OBBHHBBBBBBBBBHBO",
        "OBHHHCCCCCCBHHHBO",  # rice scoop
        "OBHHCCCCCCCCBHHBO",
        "OBHCKKCCCCCCBBHBO",  # curry
        "OBHKKKKKKCCCBHHBO",
        "OBBKKKKKKKKKBBHBO",
        ".OBBKKKKKKKKBBOO.",
        "..OBBKKKKKKBBO...",
        "...OOOOOOOOOO....",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'H': BOWL_HI, 'C': RICE, 'K': CURRY_B}
    stamp(px, 8, 11, BOWL, CM)
    # Curry highlights
    for x, y in [(14, 17), (17, 17), (16, 18)]:
        put(px, x, y, CURRY_HI)
    # Garnish (cilantro)
    for x, y in [(15, 14), (18, 14), (16, 13)]:
        put(px, x, y, GARNISH)
    return img


# ===========================================================
# Greek salad
# ===========================================================
def greek_salad():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    TOMATO   = (210,  50,  40, 255)
    CUCUMBER = ( 80, 160,  60, 255)
    CUCUMBER_HI = (140, 200, 100, 255)
    OLIVE_DK = ( 40,  30,  20, 255)
    OLIVE_B  = ( 80,  60,  40, 255)
    FETA     = (255, 250, 230, 255)
    ONION    = (200, 130, 180, 255)
    # Bowl
    BOWL = [
        "..OOOOOOOOOOOO..",
        ".OBBBBBBBBBBBBO.",
        "OBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOOO.",
    ]
    CM = {'O': OL, 'B': BOWL_B}
    stamp(px, 8, 23, BOWL, CM)
    # Random salad contents at varying positions
    # Tomato chunks
    for x, y in [(11, 13), (16, 11), (20, 12), (13, 17), (19, 18)]:
        put(px, x, y, TOMATO)
        put(px, x + 1, y, TOMATO)
    # Cucumber slices
    for x, y in [(14, 13), (18, 14), (12, 19), (21, 17)]:
        put(px, x, y, CUCUMBER)
        put(px, x + 1, y, CUCUMBER_HI)
    # Olives (black)
    for x, y in [(17, 16), (12, 14), (22, 19), (15, 19)]:
        put(px, x, y, OLIVE_DK)
        put(px, x, y - 1, OLIVE_B)
    # Feta cubes (white)
    for x, y in [(13, 15), (19, 13), (16, 17), (21, 14)]:
        put(px, x, y, FETA)
        put(px, x + 1, y, FETA)
    # Red onion slivers
    for x, y in [(14, 16), (20, 16)]:
        put(px, x, y, ONION)
    return img


# ===========================================================
# Borscht (red beet soup)
# ===========================================================
def borscht():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SOUP_DK = (110,  20,  30, 255)
    SOUP_B  = (170,  30,  50, 255)
    SOUP_HI = (210,  60,  80, 255)
    CREAM   = (250, 250, 240, 255)
    DILL    = (100, 180,  80, 255)
    # Bowl
    BOWL = [
        "..OOOOOOOOOOOOO..",
        ".OBHBBBBBBBBBHBO.",
        "OBHBSSSSSSSSSBHBO",
        "OBHSSSSSSSSSSSHBO",
        "OBHSSSSSSSSSSSHBO",
        "OBHSSSSSSSSSSSHBO",
        "OBBSSSSSSSSSSSBBO",
        ".OBBSSSSSSSSSBBO.",
        "..OOOOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'H': BOWL_HI, 'S': SOUP_B}
    stamp(px, 8, 13, BOWL, CM)
    # Soup highlights (reflections)
    for x, y in [(13, 16), (18, 17), (15, 18), (21, 16)]:
        put(px, x, y, SOUP_HI)
    # Sour cream dollop in center
    put(px, 15, 17, CREAM)
    put(px, 16, 17, CREAM)
    put(px, 15, 18, CREAM)
    put(px, 16, 18, CREAM)
    # Dill garnish
    put(px, 14, 17, DILL)
    put(px, 17, 18, DILL)
    return img


# ===========================================================
# Hummus + pita
# ===========================================================
def hummus_pita():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    HUMMUS_DK = (160, 120,  60, 255)
    HUMMUS_B  = (220, 180, 110, 255)
    HUMMUS_HI = (245, 215, 160, 255)
    OIL       = (220, 170,  20, 255)
    PARSLEY   = (100, 180,  80, 255)
    PITA_DK   = (160, 120,  60, 255)
    PITA_B    = (220, 180, 110, 255)
    PITA_HI   = (245, 215, 160, 255)
    # Small bowl of hummus on left
    BOWL = [
        ".OOOOOOOO.",
        "OBBBBBBBBO",
        "OBHHHHHHBO",
        "OBHHHHHHBO",
        "OBHHHHHHBO",
        ".OBBBBBBO.",
        "..OOOOOO..",
    ]
    CM = {'O': OL, 'B': BOWL_B, 'H': HUMMUS_B}
    stamp(px, 5, 13, BOWL, CM)
    # Hummus surface texture
    for x, y in [(8, 16), (10, 16), (12, 17)]:
        put(px, x, y, HUMMUS_HI)
    # Olive oil drizzle (golden line)
    put(px, 9, 16, OIL)
    put(px, 10, 16, OIL)
    # Parsley sprig
    put(px, 11, 16, PARSLEY)
    # Pita bread on right
    PITA = [
        "OOOOOOOO",
        "OBHHHHBO",
        "OBHHHHBO",
        "OBHBBHBO",
        "OBHHHHBO",
        ".OOOOOO.",
    ]
    CM = {'O': OL, 'B': PITA_B, 'H': PITA_HI}
    stamp(px, 18, 14, PITA, CM)
    return img


# ===========================================================
# Tom Yum (Thai hot-sour soup)
# ===========================================================
def tom_yum():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    SOUP_DK = (180,  50,  20, 255)
    SOUP_B  = (230,  90,  40, 255)
    SOUP_HI = (255, 140,  70, 255)
    SHRIMP_DK = (200,  70,  50, 255)
    SHRIMP_B  = (255, 130,  90, 255)
    LIME      = (180, 230,  90, 255)
    LIME_DK   = (110, 170,  50, 255)
    GALANGAL  = (220, 200, 150, 255)
    OL_DK     = ( 60,  20,   8, 255)
    # Wider, shallow bowl
    BOWL = [
        ".OOOOOOOOOOOOO.",
        "OBHBBBBBBBBBHBO",
        "OBSSSSSSSSSSSSO",
        "OBSSSSSSSSSSSSO",
        "OBSSSSSSSSSSSSO",
        ".OBSSSSSSSSSSO.",
        "..OOOOOOOOOOOO.",
    ]
    CM = {'O': OL_DK, 'B': BOWL_B, 'H': BOWL_HI, 'S': SOUP_B}
    stamp(px, 8, 14, BOWL, CM)
    # Soup highlights
    for x, y in [(13, 17), (18, 17), (15, 18), (20, 18)]:
        put(px, x, y, SOUP_HI)
    # Shrimp (curved C shape)
    for x, y in [(12, 16), (13, 16), (14, 16), (13, 17), (14, 17), (12, 17)]:
        put(px, x, y, SHRIMP_B)
    put(px, 13, 16, SHRIMP_DK)
    # Lime slice (small green circle with center)
    put(px, 18, 16, LIME_DK)
    put(px, 19, 16, LIME)
    put(px, 18, 17, LIME)
    put(px, 19, 17, LIME_DK)
    # Galangal/lemongrass piece (small tan stick)
    put(px, 21, 17, GALANGAL)
    put(px, 22, 17, GALANGAL)
    return img


# ===========================================================
# DRIVER
# ===========================================================
DISHES = [
    ("pizza_margherita",  pizza),
    ("lasagna",           lasagna),
    ("ramen",             ramen),
    ("sushi_roll",        sushi),
    ("tacos",             tacos),
    ("curry_bowl",        curry),
    ("greek_salad",       greek_salad),
    ("borscht",           borscht),
    ("hummus_pita",       hummus_pita),
    ("tom_yum",           tom_yum),
]

if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/dishes"
    os.makedirs(out, exist_ok=True)
    for name, fn in DISHES:
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {name}")
    print(f"\n=== Phase 3 complete: {len(DISHES)} cooked dishes ===")
