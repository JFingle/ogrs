#!/usr/bin/env python3
"""
Magic items batch 2 — robes, spellbooks, runecrafting essentials, tiaras, pouches, magic capes.

~28 sprites at 32×32. Skips runes (vanilla is fine).
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
# MAGIC ROBES — wizard hat, robe top, robe bottom per tier
# ===========================================================

# Hat template — pointed wizard hat
HAT = [
    ".......OO.......",
    "......OBBO......",
    ".....OBBBBO.....",
    "....OBHBBBSO....",
    "...OBHHBBBSSO...",
    "...OBHHBBBSSO...",
    "..OBHHBBBBSSSO..",
    "..OBBBBBBBSSSO..",
    "OOBBBBBBBBBBSSOO",
    "OBBBBBBBBBBBBBSO",
    "OOOOOOOOOOOOOOOO",
]


# Robe top — V-neck robed body
ROBE_TOP = [
    "..OOOOOOOOOO..",
    ".OBHHBBBBBBSO.",
    "OBHHBBBBBBBSO.",
    "OBHBBBBBBBSSSO",
    "OBHBBOBOBBBSSO",
    "OBBBOOBOOBBSSO",
    "OBBBBOBOBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBSSSSO",
    "OBBBBBBBBSSSSO",
    "OBBBBBBBSSSSSO",
    "OBBBBBBSSSSSSO",
    ".OOOOOOOOOOOO.",
]


# Robe bottom — long skirt
ROBE_BOTTOM = [
    ".OOOOOOOOOOOO.",
    "OBHHBBBBBBBBSO",
    "OBHBBBBBBBBSSO",
    "OBHBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBSSSSO",
    "OBBBBBBSSSSSSO",
    "OBBBBBSSSSSSSO",
    "OBBBBSSSSSSSSO",
    "OBBBSSSSSSSSSO",
    "OBBSSSSSSSSSSO",
    "OOOOOOOOOOOOOO",
]


def draw_hat(palette, trim_color=None):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],
    }
    stamp(px, 8, 10, HAT, CM)
    # Optional trim band (around hat brim base)
    if trim_color:
        for x in range(8, 24):
            put(px, x, 18, trim_color)
    return img


def draw_robe_top(palette, trim_color=None):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],
    }
    stamp(px, 9, 9, ROBE_TOP, CM)
    # Trim along the V-neck and waist
    if trim_color:
        # V-neck
        put(px, 14, 12, trim_color); put(px, 15, 12, trim_color); put(px, 17, 12, trim_color); put(px, 18, 12, trim_color)
        put(px, 15, 13, trim_color); put(px, 17, 13, trim_color)
        put(px, 16, 14, trim_color)
        # Waist sash
        for x in range(11, 21):
            put(px, x, 20, trim_color)
    return img


def draw_robe_bottom(palette, trim_color=None):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],
    }
    stamp(px, 9, 10, ROBE_BOTTOM, CM)
    # Hem trim along the bottom
    if trim_color:
        for x in range(9, 22):
            put(px, x, 20, trim_color)
    return img


# Robe tier palettes
ROBE_TIERS = {
    'wizard': {
        'outline': (10, 30, 80, 255),
        'base':    (40, 80, 180, 255),
        'highlight':(80, 130, 230, 255),
        'shadow':  (20, 50, 130, 255),
        'trim':    (240, 200, 60, 255),    # gold trim
    },
    'mystic_blue': {
        'outline': (20, 30, 100, 255),
        'base':    (60, 100, 200, 255),
        'highlight':(120, 170, 250, 255),
        'shadow':  (40, 60, 140, 255),
        'trim':    (255, 240, 100, 255),
    },
    'mystic_dark': {
        'outline': (20, 10, 30, 255),
        'base':    (60, 30, 80, 255),
        'highlight':(120, 80, 160, 255),
        'shadow':  (35, 20, 50, 255),
        'trim':    (255, 200, 60, 255),
    },
    'infinity': {
        'outline': (8, 10, 40, 255),
        'base':    (30, 50, 130, 255),
        'highlight':(120, 160, 240, 255),
        'shadow':  (15, 30, 80, 255),
        'trim':    (255, 240, 180, 255),   # platinum/white trim
    },
}


# ===========================================================
# SPELLBOOKS
# ===========================================================

def draw_spellbook(cover_palette, gem_color, gold_corners=True, has_runes=False):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    OL = (20, 10, 8, 255)
    PAGES = (245, 230, 200, 255)
    PAGES_DK = (200, 180, 140, 255)
    SPINE = tuple(max(0, c - 40) for c in cover_palette['base'][:3]) + (255,)

    BOOK = [
        ".OOOOOOOOOOOOO.",
        "OPPPPPPPPPPPPPO",
        "OBHHHHHHHHHHHBO",
        "OBHCHHHHHHHHHBO",
        "OBHCHHHHGHHHHBO",
        "OBHCHHHGGGHHHBO",
        "OBHCHHHHGHHHHBO",
        "OBHCHHHHHHHHHBO",
        "OBHCHHHHHHHHHBO",
        "OBHCHHHHHHHHHBO",
        "OBHHHHHHHHHHHBO",
        "OPPPPPPPPPPPPPO",
        ".OOOOOOOOOOOOO.",
    ]
    CM = {
        'O': OL,
        'P': PAGES,
        'B': cover_palette['base'],
        'H': cover_palette['highlight'],
        'C': SPINE,
        'G': cover_palette.get('emblem_dk', cover_palette['shadow']),
    }
    stamp(px, 9, 10, BOOK, CM)
    # Central gem on cover
    if gem_color:
        put(px, 16, 16, gem_color)
        put(px, 16, 15, gem_color)  # vertical highlight
    # Gold corners (decorative)
    if gold_corners:
        GOLD = (240, 200, 60, 255)
        for x, y in [(10, 11), (22, 11), (10, 20), (22, 20)]:
            put(px, x, y, GOLD)
    # Runes on the cover (etched dots)
    if has_runes:
        ETCH = cover_palette.get('etch', (200, 200, 200, 255))
        for x, y in [(13, 13), (19, 13), (13, 19), (19, 19)]:
            put(px, x, y, ETCH)
    return img


SPELLBOOKS = [
    ('spellbook_standard', {
        'base': (140, 90, 40, 255),
        'highlight': (200, 150, 80, 255),
        'shadow': (100, 60, 20, 255),
        'emblem_dk': (60, 40, 10, 255),
    }, (220, 60, 60, 255), True, False),   # brown leather + gold corners + ruby gem
    ('spellbook_ancient', {
        'base': (40, 30, 60, 255),
        'highlight': (90, 70, 130, 255),
        'shadow': (20, 14, 30, 255),
        'emblem_dk': (10, 8, 20, 255),
        'etch': (180, 160, 220, 255),
    }, (140, 50, 200, 255), True, True),   # dark purple + violet gem + etched runes
    ('spellbook_yahwist', {                # OGRS-specific
        'base': (200, 180, 100, 255),
        'highlight': (240, 220, 150, 255),
        'shadow': (140, 110, 50, 255),
        'emblem_dk': (90, 60, 20, 255),
        'etch': (255, 255, 220, 255),
    }, (240, 200, 60, 255), True, True),   # gold + amber gem + golden etched runes
]


# ===========================================================
# RUNECRAFTING ESSENCE + TIARAS
# ===========================================================

def rune_essence_rock():
    """Mined essence — looks like an unmined rock with crystal hints."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (60, 60, 80, 255)
    B = (110, 110, 130, 255)
    HI = (160, 160, 180, 255)
    CRYSTAL = (180, 180, 240, 255)
    OL = (20, 20, 30, 255)
    ROCK = [
        "...OOOOOO...",
        "..OBHHBBSO..",
        ".OBHHHBBBSO.",
        "OBHHHBBBBSO.",
        "OBHHBBBBBBSO",
        "OBHBBBBBBSSO",
        "OBBBBBBBSSSO",
        ".OBBBBBSSSO.",
        "..OOOOOOOO..",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 10, 12, ROCK, CM)
    # Tiny crystal vein peek
    for x, y in [(14, 16), (17, 18)]:
        put(px, x, y, CRYSTAL)
    return img


def rune_essence_mined():
    """Small chunk of mined essence."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (80, 70, 100, 255)
    B = (140, 120, 170, 255)
    HI = (190, 170, 220, 255)
    SHEEN = (240, 230, 255, 255)
    OL = (40, 30, 60, 255)
    CHUNK = [
        "...OOOOO...",
        "..OBHHBSO..",
        ".OBHHHBBSO.",
        "OBHHHBBBSO.",
        "OBHBBBBSSO.",
        "OBBBBBSSSO.",
        ".OBBBSSSO..",
        "..OOOOOO...",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 13, CHUNK, CM)
    put(px, 14, 15, SHEEN)
    return img


def pure_essence():
    """Pure essence — brighter / clearer crystal."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    DK = (180, 200, 240, 255)
    B = (220, 230, 250, 255)
    HI = (255, 255, 255, 255)
    GLOW = (200, 220, 255, 110)
    OL = (100, 130, 180, 255)
    # Halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 16, y - 17
            d2 = dx * dx + dy * dy
            if 30 <= d2 <= 70 and (x + y) % 2 == 0:
                put(px, x, y, GLOW)
    CHUNK = [
        "...OOOOO...",
        "..OHHHHBO..",
        ".OHHHHBBSO.",
        "OHHHHBBBBO.",
        "OBHHBBBBSO.",
        "OBBBBBSSSO.",
        ".OBBBSSSO..",
        "..OOOOOO...",
    ]
    CM = {'O': OL, 'B': B, 'H': HI, 'S': DK}
    stamp(px, 11, 13, CHUNK, CM)
    return img


def tiara(stone_color, glow_color):
    """Runecrafting tiara — small circlet headband with colored stone."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    METAL_DK = (130, 100, 30, 255)
    METAL_B = (200, 170, 80, 255)
    METAL_HI = (250, 230, 130, 255)
    OL = (60, 40, 10, 255)
    # Halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 16, y - 17
            d2 = dx * dx + dy * dy
            if 30 <= d2 <= 70 and (x + y) % 2 == 0:
                put(px, x, y, glow_color)
    # Curved circlet band
    BAND = [
        "...OOOOOOOO...",
        "..OBHHHHHHBO..",
        ".OBHHHHHHHHBO.",
        ".OBBBBBBBBBBO.",
        "..OOOOOOOOOO..",
    ]
    CM = {'O': OL, 'B': METAL_B, 'H': METAL_HI}
    stamp(px, 9, 14, BAND, CM)
    # Central stone (raised gem in the front of the circlet)
    cx, cy = 16, 13
    sh = tuple(stone_color) + (255,)
    hi = tuple(min(255, c + 50) for c in stone_color[:3]) + (255,)
    dk = tuple(max(0, c - 40) for c in stone_color[:3]) + (255,)
    cells = {
        (-1, -1): METAL_DK, (0, -1): METAL_DK, (1, -1): METAL_DK,
        (-1, 0): hi, (0, 0): sh, (1, 0): dk,
        (-1, 1): METAL_DK, (0, 1): METAL_DK, (1, 1): METAL_DK,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)
    return img


TIARAS = [
    ('air',     (220, 220, 200), (255, 250, 220, 120)),
    ('water',   (60, 130, 220),  (140, 200, 255, 120)),
    ('earth',   (130, 90, 40),   (160, 110, 50, 100)),
    ('fire',    (220, 60, 20),   (255, 130, 40, 120)),
    ('mind',    (160, 180, 220), (180, 200, 240, 110)),
    ('body',    (200, 140, 80),  (220, 160, 90, 110)),
    ('cosmic',  (140, 90, 200),  (180, 130, 240, 130)),
    ('chaos',   (160, 20, 20),   (200, 50, 50, 130)),
]


# ===========================================================
# RUNE POUCHES (3 sizes)
# ===========================================================

def rune_pouch(size):
    """Leather pouch — small/medium/large. Rune-shaped runic accent on flap."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    OL = (40, 20, 10, 255)
    POUCH_DK = (90, 60, 30, 255)
    POUCH_B = (160, 110, 60, 255)
    POUCH_HI = (220, 170, 100, 255)
    DRAW = (50, 30, 10, 255)
    RUNE_GLOW = (140, 200, 250, 255)

    sizes = {
        'small':  (10, 8),
        'medium': (12, 10),
        'large':  (14, 12),
    }
    pw, ph = sizes[size]
    pox, poy = (W - pw) // 2, 12

    # Pouch body
    for dy in range(ph):
        for dx in range(pw):
            x = pox + dx; y = poy + dy
            if (dx == 0 and dy == 0) or (dx == pw - 1 and dy == 0) or \
               (dx == 0 and dy == ph - 1) or (dx == pw - 1 and dy == ph - 1):
                continue   # round corners
            if dy == 0 or dy == ph - 1 or dx == 0 or dx == pw - 1:
                put(px, x, y, OL)
            elif dx <= 2:
                put(px, x, y, POUCH_HI)
            elif dx >= pw - 3:
                put(px, x, y, POUCH_DK)
            else:
                put(px, x, y, POUCH_B)
    # Drawstring tie at top
    cx_tie = pox + pw // 2
    put(px, cx_tie, poy - 1, DRAW)
    put(px, cx_tie - 1, poy - 1, DRAW)
    put(px, cx_tie + 1, poy - 1, DRAW)
    put(px, cx_tie, poy - 2, OL)
    # Runic glow rune symbol on the front
    rx, ry = pox + pw // 2, poy + ph // 2
    put(px, rx, ry, RUNE_GLOW)
    put(px, rx - 1, ry, RUNE_GLOW)
    put(px, rx + 1, ry, RUNE_GLOW)
    put(px, rx, ry - 1, RUNE_GLOW)
    put(px, rx, ry + 1, RUNE_GLOW)
    return img


# ===========================================================
# MAGIC CAPES
# ===========================================================

def magic_cape(cape_palette, has_hood=True, trim_color=None):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    OL = (20, 10, 30, 255)
    # Cape body (trapezoid)
    CAPE = [
        "..OOOOOOOOOO..",
        ".OBHHBBBBBBSO.",
        "OBHHBBBBBBBSO.",
        "OBHBBBBBBBBSSO",
        "OBHBBBBBBBBSSO",
        "OBHBBBBBBBSSSO",
        "OBBBBBBBBBSSSO",
        "OBBBBBBBBBSSSO",
        "OBBBBBBBBSSSSO",
        "OBBBBBBBSSSSSO",
        "OBBBBBBSSSSSSO",
        "OBBBBBSSSSSSSO",
        "OBBBBSSSSSSSSO",
        "OBBBSSSSSSSSSO",
        "OOOOOOOOOOOOOO",
    ]
    CM = {
        'O': OL,
        'B': cape_palette['base'],
        'H': cape_palette['highlight'],
        'S': cape_palette['shadow'],
    }
    stamp(px, 9, 9, CAPE, CM)
    # Hood pinned at the neck top
    if has_hood:
        for dx in range(-2, 3):
            put(px, 16 + dx, 7, OL)
            put(px, 16 + dx, 8, cape_palette['base'])
        put(px, 16, 6, OL)
    # Trim along bottom hem
    if trim_color:
        for x in range(11, 22):
            put(px, x, 22, trim_color)
    return img


MAGIC_CAPES = [
    ('cape_magic_skill', {
        'base': (140, 80, 200, 255),
        'highlight': (200, 140, 240, 255),
        'shadow': (90, 50, 140, 255),
    }, (255, 240, 100, 255)),   # purple cape + gold trim
    ('cape_runecraft_skill', {
        'base': (180, 130, 200, 255),
        'highlight': (220, 180, 240, 255),
        'shadow': (130, 90, 150, 255),
    }, (255, 240, 100, 255)),
    ('cape_magic_master', {
        'base': (80, 50, 150, 255),
        'highlight': (140, 100, 220, 255),
        'shadow': (50, 30, 100, 255),
    }, (255, 240, 200, 255)),   # darker purple + platinum trim
]


# ===========================================================
# DRIVER
# ===========================================================
if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/items/magic"

    # Robes
    out = f"{base}/robes"
    os.makedirs(out, exist_ok=True)
    for tier_name, palette in ROBE_TIERS.items():
        for fn, name in [(draw_hat, 'hat'), (draw_robe_top, 'top'), (draw_robe_bottom, 'bottom')]:
            img = fn(palette, palette.get('trim'))
            f = f"{out}/{tier_name}_{name}"
            img.save(f"{f}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{f}_x8.png")
        print(f"  robes: {tier_name}")

    # Spellbooks
    out = f"{base}/spellbooks"
    os.makedirs(out, exist_ok=True)
    for name, palette, gem, corners, runes in SPELLBOOKS:
        img = draw_spellbook(palette, gem, corners, runes)
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"  spellbook: {name}")

    # Runecrafting essentials
    out = f"{base}/runecraft"
    os.makedirs(out, exist_ok=True)
    for name, fn in [('essence_rock', rune_essence_rock), ('essence_mined', rune_essence_mined), ('pure_essence', pure_essence)]:
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"  essence: {name}")

    # Tiaras
    out = f"{base}/tiaras"
    os.makedirs(out, exist_ok=True)
    for element, stone, glow in TIARAS:
        img = tiara(stone, glow)
        img.save(f"{out}/tiara_{element}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/tiara_{element}_x8.png")
        print(f"  tiara: {element}")

    # Pouches
    out = f"{base}/pouches"
    os.makedirs(out, exist_ok=True)
    for size in ('small', 'medium', 'large'):
        img = rune_pouch(size)
        img.save(f"{out}/pouch_{size}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/pouch_{size}_x8.png")
        print(f"  pouch: {size}")

    # Magic capes
    out = f"{base}/capes"
    os.makedirs(out, exist_ok=True)
    for name, palette, trim in MAGIC_CAPES:
        img = magic_cape(palette, has_hood=True, trim_color=trim)
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"  cape: {name}")

    total = len(ROBE_TIERS) * 3 + len(SPELLBOOKS) + 3 + len(TIARAS) + 3 + len(MAGIC_CAPES)
    print(f"\n=== Magic items batch 2 complete: {total} sprites ===")
