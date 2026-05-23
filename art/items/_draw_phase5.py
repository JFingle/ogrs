#!/usr/bin/env python3
"""
Phase 5 — Tier-5 masterwork dishes (8-9 ingredients, 40-55 HP).

8 plated dishes at 32×32. These are the premium, special-occasion meals.
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


# ===========================================================
# Paella — Spanish saffron rice with seafood (large flat pan)
# ===========================================================
def paella():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PAN_DK = ( 40,  40,  50, 255)
    PAN_B  = (100, 100, 110, 255)
    PAN_HI = (160, 160, 170, 255)
    RICE_Y = (240, 210,  80, 255)
    RICE_O = (220, 180,  60, 255)
    SHRIMP = (240, 110,  90, 255)
    MUSSEL = ( 40,  30,  60, 255)
    MUSSEL_HI = ( 90,  70, 130, 255)
    PEPPER_R = (210,  50,  40, 255)
    PEAS = (110, 180,  70, 255)
    LEMON = (250, 200,  80, 255)
    # Wide shallow pan
    PAN = [
        "OOOOOOOOOOOOOOOOO",
        "OBHHHHHHHHHHHHHHO",
        "OBYYYYYYYYYYYYYBO",
        "OBYOYOYOYOYOYOYBO",
        "OBYYYYYYYYYYYYYBO",
        "OBYOYOYOYOYOYOYBO",
        "OBYYYYYYYYYYYYYBO",
        ".OBBBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOOOO..",
    ]
    CM = {'O': PAN_DK, 'B': PAN_B, 'H': PAN_HI, 'Y': RICE_Y}
    stamp(px, 7, 12, PAN, CM)
    # Toppings: shrimps, mussels, peppers, peas, lemon wedge
    # Shrimp 1 (curved)
    for x, y in [(10, 16), (11, 16), (12, 16), (11, 17)]:
        put(px, x, y, SHRIMP)
    # Mussel shells (black-purple)
    for x, y in [(14, 16), (15, 16), (14, 17)]:
        put(px, x, y, MUSSEL)
    put(px, 14, 16, MUSSEL_HI)
    # Red pepper strips
    put(px, 17, 17, PEPPER_R)
    put(px, 18, 17, PEPPER_R)
    # Peas scattered
    for x, y in [(13, 18), (19, 18), (16, 18)]:
        put(px, x, y, PEAS)
    # Lemon wedge
    put(px, 21, 16, LEMON)
    put(px, 22, 16, LEMON)
    # Second shrimp
    for x, y in [(19, 16), (20, 16)]:
        put(px, x, y, SHRIMP)
    return img


# ===========================================================
# Beef Bourguignon — beef in red wine sauce with bacon, mushroom, carrot
# ===========================================================
def beef_bourguignon():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    WINE_DK = ( 80,  20,  30, 255)
    WINE_B  = (140,  30,  50, 255)
    WINE_HI = (200,  60,  80, 255)
    BEEF_DK = ( 80,  40,  20, 255)
    BEEF_B  = (140,  70,  40, 255)
    BACON   = (200,  90,  60, 255)
    MUSH    = (120,  80,  40, 255)
    CARROT  = (240, 130,  40, 255)
    PARSLEY = ( 90, 170,  50, 255)
    BOWL = [
        ".OOOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBBHBO",
        "OBBWWWWWWWWWWWBBO",
        "OBHWWWWWWWWWWWHBO",
        "OBWWWWWWWWWWWWWBO",
        "OBWWWWWWWWWWWWWBO",
        "OBBWWWWWWWWWWWBBO",
        ".OBBBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'W': WINE_B}
    stamp(px, 7, 12, BOWL, CM)
    # Wine highlights
    for x, y in [(12, 16), (18, 17), (15, 18), (21, 16)]:
        put(px, x, y, WINE_HI)
    # Beef chunks (substantial cubes)
    for x, y in [(11, 16), (16, 16), (19, 17)]:
        put(px, x, y, BEEF_DK)
        put(px, x + 1, y, BEEF_B)
        put(px, x, y + 1, BEEF_DK)
        put(px, x + 1, y + 1, BEEF_DK)
    # Bacon bits
    for x, y in [(14, 17), (20, 18)]:
        put(px, x, y, BACON)
    # Mushroom
    for x, y in [(13, 18), (17, 18)]:
        put(px, x, y, MUSH)
    # Carrot
    put(px, 15, 18, CARROT)
    # Parsley garnish
    put(px, 16, 15, PARSLEY)
    put(px, 19, 16, PARSLEY)
    return img


# ===========================================================
# Bouillabaisse — Provençal seafood stew with saffron broth
# ===========================================================
def bouillabaisse():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BROTH_DK = (160,  90,  20, 255)
    BROTH_B  = (220, 130,  40, 255)
    BROTH_HI = (250, 170,  70, 255)
    FISH_DK = ( 60,  80, 100, 255)
    FISH_B  = (130, 150, 170, 255)
    FISH_HI = (200, 220, 240, 255)
    SHRIMP = (240, 110,  90, 255)
    MUSSEL = ( 40,  30,  60, 255)
    HERB = ( 90, 160,  50, 255)
    BOWL = [
        "..OOOOOOOOOOOOOO..",
        ".OBHBBBBBBBBBBHBO.",
        "OBBHHHHHHHHHHHHBO",
        "OBHRRRRRRRRRRRHBO",
        "OBHRRRRRRRRRRRHBO",
        "OBHRRRRRRRRRRRHBO",
        "OBBRRRRRRRRRRRBBO",
        ".OBBRRRRRRRRRBBO.",
        "..OOOOOOOOOOOO...",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'R': BROTH_B}
    stamp(px, 7, 12, BOWL, CM)
    # Broth highlights (saffron shimmer)
    for x, y in [(13, 17), (18, 18), (15, 18), (20, 17)]:
        put(px, x, y, BROTH_HI)
    # Fish chunks
    for x, y in [(12, 16), (16, 16)]:
        put(px, x, y, FISH_B)
        put(px, x + 1, y, FISH_HI)
        put(px, x, y + 1, FISH_DK)
    # Shrimp
    for x, y in [(19, 16), (20, 16), (21, 17)]:
        put(px, x, y, SHRIMP)
    # Mussel shells
    for x, y in [(14, 18), (17, 18)]:
        put(px, x, y, MUSSEL)
        put(px, x + 1, y, MUSSEL)
    # Herb sprig floating
    put(px, 16, 15, HERB)
    put(px, 19, 16, HERB)
    return img


# ===========================================================
# Peking Duck — golden duck pieces with pancake, scallion, plum sauce
# ===========================================================
def peking_duck():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DUCK_DK = (140,  70,  20, 255)
    DUCK_B  = (220, 140,  60, 255)
    DUCK_HI = (250, 190, 100, 255)
    SKIN    = (230, 110,  40, 255)
    PANCAKE = (240, 220, 170, 255)
    SCALLION = (110, 180,  70, 255)
    PLUM_SAUCE = (150,  40,  60, 255)
    CUCUMBER = ( 90, 170,  60, 255)
    OL = ( 60,  20,   8, 255)
    PLATE = [
        ".OOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBHBO",
        "OBBBBBBBBBBBBBBO",
        "OBHBBBBBBBBBBBBO",
        "OBHBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI}
    stamp(px, 8, 14, PLATE, CM)
    # Duck slices (golden brown rectangles)
    for x in range(11, 19):
        put(px, x, 16, DUCK_HI)
        put(px, x, 17, DUCK_B)
        put(px, x, 18, DUCK_DK)
    # Crispy skin highlights
    for x in [12, 14, 16, 18]:
        put(px, x, 15, SKIN)
    # Pancake roll on the side
    for x in range(20, 24):
        put(px, x, 16, PANCAKE)
        put(px, x, 17, PANCAKE)
    put(px, 23, 16, PANCAKE)
    # Scallion strips
    for x in (20, 21, 22):
        put(px, x, 15, SCALLION)
    # Plum sauce dollop
    put(px, 24, 17, PLUM_SAUCE)
    put(px, 24, 18, PLUM_SAUCE)
    # Cucumber slices
    put(px, 19, 19, CUCUMBER)
    put(px, 22, 19, CUCUMBER)
    return img


# ===========================================================
# Feijoada — Brazilian black bean stew with pork
# ===========================================================
def feijoada():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    BEAN_DK = ( 30,  20,  20, 255)
    BEAN_B  = ( 70,  40,  30, 255)
    BEAN_HI = (120,  70,  50, 255)
    PORK = (200, 130,  80, 255)
    SAUSAGE = (140,  70,  40, 255)
    ORANGE = (250, 150,  60, 255)
    RICE = (250, 245, 230, 255)
    HERB = ( 90, 160,  50, 255)
    BOWL = [
        ".OOOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBBHBO",
        "OBBKKKKKKKKKKKBBO",  # K = black beans
        "OBKKKKKKKKKKKKKBO",
        "OBKKKKKKKKKKKKKBO",
        "OBKKKKKKKKKKKKKBO",
        ".OBBKKKKKKKKKBBO.",
        "..OOOOOOOOOOOO...",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'K': BEAN_B}
    stamp(px, 7, 13, BOWL, CM)
    # Bean texture (individual bean dots)
    for x, y in [(11, 16), (14, 16), (17, 17), (20, 16), (12, 18), (16, 18), (19, 18), (13, 17)]:
        put(px, x, y, BEAN_HI)
    # Pork chunks
    for x, y in [(13, 16), (18, 17)]:
        put(px, x, y, PORK)
        put(px, x + 1, y, PORK)
    # Sausage slice
    put(px, 15, 18, SAUSAGE)
    put(px, 16, 18, SAUSAGE)
    # Orange wedge on the side (traditional)
    for x, y in [(21, 17), (22, 17)]:
        put(px, x, y, ORANGE)
    # Rice peek
    put(px, 11, 18, RICE)
    put(px, 21, 18, RICE)
    # Herb garnish
    put(px, 16, 15, HERB)
    return img


# ===========================================================
# Bibimbap — Korean rice bowl with many toppings
# ===========================================================
def bibimbap():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    RICE = (250, 245, 230, 255)
    BEEF = (140,  60,  40, 255)
    SPINACH = (60, 120, 40, 255)
    CARROT = (240, 130,  40, 255)
    MUSHROOM = (140,  90,  40, 255)
    EGG_Y = (250, 200,  80, 255)
    EGG_W = (250, 250, 240, 255)
    GOCHU = (200,  40,  20, 255)
    SESAME = (240, 230, 180, 255)
    BOWL = [
        "..OOOOOOOOOOOOOO..",
        ".OBHBBBBBBBBBBHBO.",
        "OBBRRRRRRRRRRRBBO",
        "OBRRRRRRRRRRRRRBO",
        "OBRRRRRRRRRRRRRBO",
        "OBRRRRRRRRRRRRRBO",
        ".OBBRRRRRRRRRBBO.",
        "..OOOOOOOOOOOO...",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'R': RICE}
    stamp(px, 7, 13, BOWL, CM)
    # Toppings arranged in sections around a central egg
    # Beef (top)
    put(px, 14, 15, BEEF); put(px, 15, 15, BEEF); put(px, 14, 16, BEEF)
    # Spinach (right)
    put(px, 18, 16, SPINACH); put(px, 19, 16, SPINACH); put(px, 19, 17, SPINACH)
    # Carrot (bottom right)
    put(px, 19, 18, CARROT); put(px, 18, 18, CARROT)
    # Mushroom (bottom left)
    put(px, 12, 18, MUSHROOM); put(px, 13, 18, MUSHROOM)
    # Spinach again (left)
    put(px, 11, 16, SPINACH); put(px, 12, 16, SPINACH)
    # Central egg (sunny side up)
    put(px, 15, 17, EGG_W); put(px, 16, 17, EGG_W); put(px, 17, 17, EGG_W)
    put(px, 16, 17, EGG_Y)
    # Gochujang dollop
    put(px, 14, 17, GOCHU)
    # Sesame seeds scattered
    for x, y in [(13, 15), (17, 16), (16, 18)]:
        put(px, x, y, SESAME)
    return img


# ===========================================================
# Jollof Rice — West African red tomato rice with chicken
# ===========================================================
def jollof():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    RICE_R = (220, 100,  40, 255)
    RICE_DK = (160,  60,  20, 255)
    RICE_HI = (250, 150,  70, 255)
    CHICKEN_DK = (140,  90,  40, 255)
    CHICKEN_B  = (210, 150,  80, 255)
    BELL_PEPPER = (210,  50,  40, 255)
    GREEN_BELL = (110, 180,  70, 255)
    ONION = (200, 130, 180, 255)
    HERB = ( 90, 170,  50, 255)
    PLATE = [
        ".OOOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBBHBO",
        "OBBRRRRRRRRRRRBBO",
        "OBRRRRRRRRRRRRRBO",
        "OBRRRRRRRRRRRRRBO",
        "OBRRRRRRRRRRRRRBO",
        ".OBBRRRRRRRRRBBO.",
        "..OOOOOOOOOOOO...",
    ]
    CM = {'O': BOWL_O, 'B': BOWL_B, 'H': BOWL_HI, 'R': RICE_R}
    stamp(px, 7, 13, PLATE, CM)
    # Rice texture (rice grain bumps)
    for x in range(11, 22, 2):
        put(px, x, 16, RICE_HI)
        put(px, x, 18, RICE_DK)
    for x in range(12, 21, 2):
        put(px, x, 17, RICE_HI)
    # Chicken pieces
    for x, y in [(12, 16), (16, 17), (19, 16)]:
        put(px, x, y, CHICKEN_DK)
        put(px, x + 1, y, CHICKEN_B)
    # Bell pepper bits
    for x, y in [(15, 18), (20, 18)]:
        put(px, x, y, BELL_PEPPER)
    # Green pepper
    for x, y in [(13, 17), (18, 16)]:
        put(px, x, y, GREEN_BELL)
    # Onion bits
    put(px, 14, 18, ONION)
    return img


# ===========================================================
# Sunday Roast — beef + potatoes + carrots + peas + gravy
# ===========================================================
def sunday_roast():
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    PLATE_DK = (180, 180, 190, 255)
    PLATE_B  = (230, 230, 235, 255)
    PLATE_HI = (255, 255, 255, 255)
    BEEF_DK = ( 90,  40,  20, 255)
    BEEF_B  = (140,  70,  40, 255)
    BEEF_HI = (200, 100,  60, 255)
    POTATO_DK = (200, 160,  80, 255)
    POTATO_B  = (250, 220, 130, 255)
    CARROT = (240, 130,  40, 255)
    PEAS = (110, 180,  70, 255)
    GRAVY = (140,  80,  30, 255)
    YORKSHIRE = (220, 180, 100, 255)
    OL = ( 80,  80, 100, 255)
    PLATE = [
        ".OOOOOOOOOOOOOO.",
        "OBHBBBBBBBBBBBHO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        "OBBBBBBBBBBBBBBO",
        ".OBBBBBBBBBBBBO.",
        "..OOOOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': PLATE_B, 'H': PLATE_HI}
    stamp(px, 8, 14, PLATE, CM)
    # Beef slice (the centerpiece)
    for x in range(11, 17):
        put(px, x, 16, BEEF_HI)
        put(px, x, 17, BEEF_B)
        put(px, x, 18, BEEF_DK)
    # Roast potatoes (3 visible)
    for cx, cy in [(18, 16), (21, 17), (19, 18)]:
        put(px, cx, cy, POTATO_DK)
        put(px, cx + 1, cy, POTATO_B)
        put(px, cx, cy + 1, POTATO_B)
    # Carrots
    put(px, 19, 19, CARROT)
    put(px, 22, 19, CARROT)
    # Peas
    for x, y in [(11, 19), (13, 19), (15, 19)]:
        put(px, x, y, PEAS)
    # Yorkshire pudding (gold puff)
    for x, y in [(23, 16), (24, 16)]:
        put(px, x, y, YORKSHIRE)
    # Gravy drizzle
    for x in range(12, 16):
        put(px, x, 19, GRAVY)
    return img


# ===========================================================
# DRIVER
# ===========================================================
DISHES = [
    ("paella",            paella),
    ("beef_bourguignon",  beef_bourguignon),
    ("bouillabaisse",     bouillabaisse),
    ("peking_duck",       peking_duck),
    ("feijoada",          feijoada),
    ("bibimbap",          bibimbap),
    ("jollof_rice",       jollof),
    ("sunday_roast",      sunday_roast),
]

if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/dishes"
    os.makedirs(out, exist_ok=True)
    for name, fn in DISHES:
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {name}")
    print(f"\n=== Phase 5 complete: {len(DISHES)} Tier-5 masterworks ===")
