#!/usr/bin/env python3
"""
Masterwork armor — proof of concept.

Demonstrates the "reshade existing sprite + add features" workflow:
  1. Draw a base platebody silhouette
  2. Recolor for each tier (bronze, steel, rune)
  3. Add masterwork features (gold trim, gem inlay, glow)

If this reads well, we apply the same pattern to all existing armor
sprites (or freshly draw base templates) and get full masterwork tier
coverage with minimal new art per piece.
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


# Generic platebody silhouette — chunky breastplate shape
# We define the template, then apply different palettes per tier.
PLATE_TEMPLATE = [
    "..OOOOOOOO..",
    ".OBHHHHHHBO.",
    "OBHHHHHHHHBO",
    "OBHHHBBBHHHBO",
    "OBHHBBBBBHHBO",
    "OBHHBBSBBHHBO",   # S = central feature slot (gem/etch)
    "OBHHBBBBBHHBO",
    "OBHHHBBBHHHBO",
    "OBHHHHHHHHHBO",
    "OBBHHHHHHHBBO",
    "OBBBHHHHHBBBO",
    "OBBBBHHHHBBBO",
    "OBBBBBBBBBBBO",
    ".OBBBBBBBBBO.",
    "..OOOOOOOOOO..",
]


def draw_plate(palette, gem_color=None, glow_color=None, trim_color=None):
    """Draw a platebody with the given palette.

    palette: dict with keys 'outline', 'base', 'highlight', 'shadow'
    gem_color: optional (r,g,b,a) for the central gem
    glow_color: optional (r,g,b,a) for an aura behind the plate (masterwork glow)
    trim_color: optional (r,g,b,a) for the trim accent line"""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()

    # Optional glow halo (drawn first, behind the plate)
    if glow_color:
        for x in range(W):
            for y in range(H):
                # Halo at radius slightly larger than the plate silhouette
                dx, dy = x - 15, y - 16
                d2 = dx * dx + dy * dy
                if 72 <= d2 <= 110:
                    if (x + y) % 2 == 0:
                        put(px, x, y, glow_color)

    # Plate body
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],  # gem slot if no gem
    }
    stamp(px, 10, 8, PLATE_TEMPLATE, CM)

    # Trim accent — horizontal line across the chest
    if trim_color:
        for x in range(13, 20):
            put(px, x, 11, trim_color)

    # Central gem
    if gem_color:
        # 3×3 gem cluster at center
        cx, cy = 15, 13
        cells = {
            (-1, -1): gem_color, (0, -1): gem_color, (1, -1): gem_color,
            (-1, 0):  gem_color, (0, 0):  (255, 255, 255, 255),  # white highlight
            (1, 0):   gem_color, (-1, 1): gem_color, (0, 1):  gem_color, (1, 1): gem_color,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)

    return img


# ===========================================================
# TIER PALETTES — start with vanilla then add masterwork
# ===========================================================

# Bronze (vanilla)
BRONZE = {
    'outline':   ( 70,  44,  20, 255),
    'base':      (180, 110,  50, 255),
    'highlight': (230, 160,  80, 255),
    'shadow':    (110,  70,  30, 255),
}

# Bronze Masterwork — bronze + gold trim + ruby gem + faint glow
BRONZE_MW = {
    'outline':   ( 60,  36,  16, 255),
    'base':      (200, 130,  60, 255),
    'highlight': (250, 190, 110, 255),
    'shadow':    (130,  80,  30, 255),
}

# Steel (vanilla)
STEEL = {
    'outline':   ( 40,  44,  56, 255),
    'base':      (150, 158, 172, 255),
    'highlight': (200, 210, 224, 255),
    'shadow':    ( 90,  98, 112, 255),
}

# Steel Masterwork — steel + silver-blue trim + sapphire + cool glow
STEEL_MW = {
    'outline':   ( 30,  34,  44, 255),
    'base':      (170, 180, 200, 255),
    'highlight': (220, 230, 250, 255),
    'shadow':    (100, 108, 130, 255),
}

# Rune (vanilla — RuneScape's classic dark blue-grey)
RUNE = {
    'outline':   ( 20,  30,  60, 255),
    'base':      ( 70, 100, 160, 255),
    'highlight': (130, 160, 220, 255),
    'shadow':    ( 40,  60, 100, 255),
}

# Rune Masterwork — rune + white-glowing rune etchings + emerald + radiant glow
RUNE_MW = {
    'outline':   ( 14,  20,  50, 255),
    'base':      ( 80, 120, 200, 255),
    'highlight': (160, 200, 255, 255),
    'shadow':    ( 50,  70, 130, 255),
}


# ===========================================================
# DRIVER — emit 6 plates: 3 vanilla, 3 masterwork
# ===========================================================
JOBS = [
    # (name, palette, gem, glow, trim)
    ("plate_bronze",        BRONZE,    None,                       None,                       None),
    ("plate_bronze_mw",     BRONZE_MW, (220,  30,  30, 255),       (255, 220, 130,  90),       (255, 220, 100, 255)),  # ruby + gold trim
    ("plate_steel",         STEEL,     None,                       None,                       None),
    ("plate_steel_mw",      STEEL_MW,  ( 30, 100, 220, 255),       (130, 180, 255,  90),       (220, 230, 250, 255)),  # sapphire + silver trim
    ("plate_rune",          RUNE,      None,                       None,                       None),
    ("plate_rune_mw",       RUNE_MW,   ( 40, 200, 100, 255),       (180, 240, 255, 110),       (240, 240, 255, 255)),  # emerald + white rune-etch trim
]


if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/armor"
    os.makedirs(out, exist_ok=True)
    for name, palette, gem, glow, trim in JOBS:
        img = draw_plate(palette, gem_color=gem, glow_color=glow, trim_color=trim)
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {name}")
    print(f"\n=== Masterwork PoC complete: {len(JOBS)} platebody sprites ===")
