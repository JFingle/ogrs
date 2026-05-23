#!/usr/bin/env python3
"""
Phase 12 — Masterwork Platebody Set.

7 vanilla tiers (bronze → rune) + 7 masterwork variants = 14 sprites at 32×32.

Each tier uses a palette (outline / base / highlight / shadow).
Masterwork variants add:
  - Central gem (color matches the tier theme)
  - Trim accent across chest
  - Subtle glow halo behind the silhouette
  - Shoulder pauldron studs for higher tiers
"""
import os
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
# PLATE TEMPLATE — chunky breastplate, 12 wide × 15 tall
# ===========================================================
# O = outline  B = base  H = highlight (upper-left)  S = shadow (lower-right)
# C = central feature slot (gem on MW, base on vanilla)
PLATE_TEMPLATE = [
    "..OOOOOOOO..",
    ".OHHHHHHHHO.",
    "OHHHHHHHHHHO",
    "OHHBBBCBBHHO",
    "OHHBBBCBBHHO",
    "OHBBBBCBBBHO",
    "OHBBBBBBBBSO",
    "OBBBBBBBBBSO",
    "OBBBBBBBBSSO",
    "OBBBBBBBBSSO",
    "OBBBBBBBSSSO",
    "OBBBBBBBSSSO",
    ".OBBBBBBBSSO.",
    "..OBBBBBBSSO.",
    "...OOOOOOOO..",
]


def draw_plate(palette, gem_color=None, trim_color=None, glow_color=None, pauldron_studs=False, etching_color=None):
    """Draw a platebody using the given palette.

    palette dict keys: outline, base, highlight, shadow, white
    Optional masterwork features layered on top.
    """
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()

    # Optional glow halo (drawn first, behind the plate)
    if glow_color:
        for x in range(W):
            for y in range(H):
                dx, dy = x - 15, y - 16
                d2 = dx * dx + dy * dy
                if 72 <= d2 <= 130:
                    if (x + y) % 2 == 0:
                        put(px, x, y, glow_color)

    # Plate silhouette
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],
        'C': palette['base'],  # central pixels stay base on vanilla
    }
    stamp(px, 10, 8, PLATE_TEMPLATE, CM)

    # Trim accent — horizontal line across the chest
    if trim_color:
        for x in range(13, 20):
            put(px, x, 11, trim_color)
        # Vertical center divider (gold/silver line down the middle)
        for y in range(12, 22):
            put(px, 15, y, trim_color)

    # Etched rune patterns (higher tiers)
    if etching_color:
        for x, y in [(13, 14), (17, 14), (12, 17), (18, 17), (13, 20), (17, 20)]:
            put(px, x, y, etching_color)

    # Shoulder pauldron studs
    if pauldron_studs:
        put(px, 10, 10, palette['outline'])
        put(px, 11, 10, palette.get('white', (255, 255, 255, 255)))
        put(px, 20, 10, palette['outline'])
        put(px, 21, 10, palette.get('white', (255, 255, 255, 255)))

    # Central gem (3×3 cluster)
    if gem_color:
        cx, cy = 15, 12
        cells = {
            (-1, -1): gem_color, (0, -1): gem_color, (1, -1): gem_color,
            (-1, 0):  gem_color, (0, 0):  (255, 255, 255, 255),  # bright center
            (1, 0):   gem_color, (-1, 1): gem_color, (0, 1):  gem_color, (1, 1): gem_color,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)

    return img


# ===========================================================
# TIER PALETTES (vanilla)
# ===========================================================

BRONZE = {
    'outline':   ( 60,  36,  16, 255),
    'base':      (180, 110,  50, 255),
    'highlight': (230, 160,  80, 255),
    'shadow':    (110,  70,  30, 255),
}
IRON = {
    'outline':   ( 30,  30,  35, 255),
    'base':      (130, 130, 140, 255),
    'highlight': (180, 180, 190, 255),
    'shadow':    ( 90,  90, 100, 255),
}
STEEL = {
    'outline':   ( 40,  44,  56, 255),
    'base':      (150, 158, 172, 255),
    'highlight': (200, 210, 224, 255),
    'shadow':    ( 90,  98, 112, 255),
}
BLACK = {
    'outline':   ( 10,  10,  15, 255),
    'base':      ( 50,  50,  55, 255),
    'highlight': ( 90,  90,  95, 255),
    'shadow':    ( 25,  25,  30, 255),
}
MITHRIL = {
    'outline':   ( 20,  30,  60, 255),
    'base':      ( 90, 130, 200, 255),
    'highlight': (140, 180, 240, 255),
    'shadow':    ( 60,  90, 140, 255),
}
ADAMANT = {
    'outline':   ( 20,  60,  40, 255),
    'base':      ( 80, 140, 100, 255),
    'highlight': (130, 200, 150, 255),
    'shadow':    ( 50, 100,  70, 255),
}
RUNE = {
    'outline':   ( 14,  20,  50, 255),
    'base':      ( 70, 110, 180, 255),
    'highlight': (140, 180, 230, 255),
    'shadow':    ( 40,  70, 130, 255),
}

# Masterwork palette slight intensification of base
def mw_palette(base_pal):
    out = dict(base_pal)
    out['highlight'] = tuple(min(255, c + 20) for c in base_pal['highlight'][:3]) + (255,)
    return out


# ===========================================================
# MASTERWORK CONFIG PER TIER
# ===========================================================
# Each MW tier picks a gem, trim, glow, and optional features.

MW_CONFIGS = {
    'bronze': {
        'gem':     (220,  30,  30, 255),   # ruby
        'trim':    (255, 220, 100, 255),   # gold
        'glow':    (255, 200, 100,  90),   # warm halo
        'studs':   False,
        'etching': None,
    },
    'iron': {
        'gem':     (240, 180,  40, 255),   # amber/topaz
        'trim':    (200, 160,  60, 255),   # brass
        'glow':    (230, 200, 130,  80),   # warm halo
        'studs':   False,
        'etching': None,
    },
    'steel': {
        'gem':     ( 30, 100, 220, 255),   # sapphire
        'trim':    (220, 230, 250, 255),   # silver
        'glow':    (130, 180, 255,  90),   # cool halo
        'studs':   True,
        'etching': None,
    },
    'black': {
        'gem':     (140,   0, 200, 255),   # purple obsidian
        'trim':    (200,  40,  60, 255),   # crimson
        'glow':    (180,  40,  60, 110),   # crimson glow
        'studs':   True,
        'etching': (120,   0,  60, 255),   # dark crimson runes
    },
    'mithril': {
        'gem':     (240, 240, 255, 255),   # diamond
        'trim':    (220, 230, 250, 255),   # silver
        'glow':    (160, 200, 255, 110),   # ice glow
        'studs':   True,
        'etching': (255, 255, 255, 255),   # white runes
    },
    'adamant': {
        'gem':     ( 40, 220, 100, 255),   # emerald
        'trim':    (255, 220, 100, 255),   # gold
        'glow':    (100, 220, 130, 110),   # green glow
        'studs':   True,
        'etching': (220, 250, 180, 255),   # pale-green runes
    },
    'rune': {
        'gem':     (200,  60, 220, 255),   # amethyst / dragonstone
        'trim':    (255, 255, 255, 255),   # white-glowing rune-etch
        'glow':    (180, 220, 255, 130),   # radiant blue-white
        'studs':   True,
        'etching': (255, 255, 255, 255),   # white runes
    },
}


TIERS = [
    ('bronze',   BRONZE),
    ('iron',     IRON),
    ('steel',    STEEL),
    ('black',    BLACK),
    ('mithril',  MITHRIL),
    ('adamant',  ADAMANT),
    ('rune',     RUNE),
]


if __name__ != "__main__":
    pass  # importable as a module for Phase 13-15

if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/armor"
    os.makedirs(out, exist_ok=True)

    for tier_name, palette in TIERS:
        # Vanilla
        img = draw_plate(palette)
        img.save(f"{out}/plate_{tier_name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/plate_{tier_name}_x8.png")
        print(f"done: plate_{tier_name}")

        # Masterwork
        cfg = MW_CONFIGS[tier_name]
        img_mw = draw_plate(
            mw_palette(palette),
            gem_color=cfg['gem'],
            trim_color=cfg['trim'],
            glow_color=cfg['glow'],
            pauldron_studs=cfg['studs'],
            etching_color=cfg['etching'],
        )
        img_mw.save(f"{out}/plate_{tier_name}_mw.png")
        img_mw.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/plate_{tier_name}_mw_x8.png")
        print(f"done: plate_{tier_name}_mw")

    print(f"\n=== Phase 12 complete: 14 platebody sprites ===")
