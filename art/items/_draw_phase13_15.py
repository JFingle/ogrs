#!/usr/bin/env python3
"""
Phase 13-15 — Masterwork Armor Sets: Legs, Helm, Shield.

Reuses the tier palette + MW config system from Phase 12. 3 slots × 7 tiers × 2 (vanilla/MW) = 42 sprites.
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
# TEMPLATES
# ===========================================================

# Plate legs — wide hips tapering to two leg pieces
LEGS_TEMPLATE = [
    "OOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHO",
    "OHHBBBBBBBBBHO",
    "OHBBBBCBBBBBHO",  # C = belt/buckle slot
    "OBBBBBCBBBBBSO",
    "OBBBBBBBBBBSSO",
    "OBBBOOOOBBBSSO",  # legs split here
    "OBBOO..OOBBSSO",
    "OBBO....OBBSSO",
    "OBBO....OBBSSO",
    "OBBO....OBBSSO",
    "OBBO....OBBSSO",
    "OBBO....OBBSSO",
    "OBBO....OBBSSO",
    "OOOO....OOOOO.",
]


# Full helm — knight's helmet with visor slit
HELM_TEMPLATE = [
    "...OOOOOOOOO....",
    "..OHHHHHHHHHO...",
    ".OHHHHHHHHHHHO..",
    "OHHHHHHHHHHHHHO.",
    "OHHHBBBBBBBHHHO.",
    "OHHBBBBBBBBBBHO.",
    "OHBBBBBBBBBBBSO.",
    "OBBBOOOOOOOBBBSO",  # visor slit
    "OBBBBBBBBBBBBSO.",  # below visor
    "OBBBBBBBBBBBSSO.",
    "OBBBBBBBBBBSSSO.",
    ".OBBBBBBBBBSSO..",
    "..OBBBBBBBSSO...",
    "...OOOOOOOOO....",
]


# Kite shield — pointed bottom shield
KITE_TEMPLATE = [
    ".OOOOOOOOOOOOO.",
    "OHHHHHHHHHHHHHO",
    "OHHBBBBBBBBBHHO",
    "OHBBBBBCBBBBBHO",
    "OHBBBBBCBBBBBSO",  # C = central feature
    "OHBBBBBBBBBBBSO",
    "OHBBBBBBBBBBSSO",
    ".OBBBBBBBBBBSSO.",
    "..OBBBBBBBBSSO..",
    "...OBBBBBBSSO...",
    "....OBBBBSSO....",
    ".....OBBSSO.....",
    "......OBSO......",
    ".......OO.......",
]


# ===========================================================
# DRAW FUNCTIONS
# ===========================================================

def draw_legs(palette, gem_color=None, trim_color=None, glow_color=None, etching_color=None):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if glow_color:
        for x in range(W):
            for y in range(H):
                dx, dy = x - 15, y - 18
                d2 = dx * dx + dy * dy
                if 80 <= d2 <= 150 and (x + y) % 2 == 0:
                    put(px, x, y, glow_color)
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],
        'C': palette['base'],
    }
    stamp(px, 9, 9, LEGS_TEMPLATE, CM)
    # Belt line (trim accent)
    if trim_color:
        for x in range(11, 22):
            put(px, x, 12, trim_color)
    # Etchings on the leg fronts
    if etching_color:
        for x, y in [(11, 16), (11, 19), (20, 16), (20, 19)]:
            put(px, x, y, etching_color)
    # Belt buckle (gem replacement)
    if gem_color:
        for dx, dy in [(0, 0), (-1, 0), (1, 0)]:
            put(px, 16 + dx, 12 + dy, gem_color)
        put(px, 16, 12, (255, 255, 255, 255))
    return img


def draw_helm(palette, gem_color=None, trim_color=None, glow_color=None, etching_color=None, has_plume=False, plume_color=None):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if glow_color:
        for x in range(W):
            for y in range(H):
                dx, dy = x - 15, y - 15
                d2 = dx * dx + dy * dy
                if 80 <= d2 <= 150 and (x + y) % 2 == 0:
                    put(px, x, y, glow_color)
    # Plume on top (masterwork accent)
    if has_plume and plume_color:
        for y in (3, 4, 5):
            put(px, 15, y, plume_color)
            put(px, 16, y, plume_color)
        put(px, 14, 4, plume_color)
        put(px, 17, 4, plume_color)
        put(px, 15, 2, plume_color)
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],
    }
    stamp(px, 8, 8, HELM_TEMPLATE, CM)
    # Visor inner darkness
    for x in range(14, 21):
        put(px, x, 15, (10, 10, 14, 255))
    # Trim around the visor edge
    if trim_color:
        for x in range(13, 22):
            put(px, x, 14, trim_color)
            put(px, x, 16, trim_color)
    # Cheek etchings (sides of helm)
    if etching_color:
        for x, y in [(10, 16), (10, 18), (22, 16), (22, 18)]:
            put(px, x, y, etching_color)
    # Forehead gem
    if gem_color:
        cx, cy = 15, 12
        cells = {
            (-1, 0): gem_color, (0, 0): (255, 255, 255, 255), (1, 0): gem_color,
            (0, -1): gem_color, (0, 1): gem_color,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
    return img


def draw_shield(palette, gem_color=None, trim_color=None, glow_color=None, etching_color=None):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if glow_color:
        for x in range(W):
            for y in range(H):
                dx, dy = x - 15, y - 16
                d2 = dx * dx + dy * dy
                if 90 <= d2 <= 160 and (x + y) % 2 == 0:
                    put(px, x, y, glow_color)
    CM = {
        'O': palette['outline'],
        'B': palette['base'],
        'H': palette['highlight'],
        'S': palette['shadow'],
        'C': palette['base'],
    }
    stamp(px, 8, 9, KITE_TEMPLATE, CM)
    # Trim border tracing the shield edge
    if trim_color:
        # Trim follows the shield's outline 1 pixel in
        trim_cells = [
            (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10), (20, 10), (21, 10),
            (10, 11), (21, 11),
            (10, 14), (21, 14),
            (11, 18), (20, 18),
            (12, 20), (19, 20),
        ]
        for x, y in trim_cells:
            put(px, x, y, trim_color)
    # Etched cross or rune lines
    if etching_color:
        # Vertical cross arm
        for y in range(12, 21):
            put(px, 15, y, etching_color)
        # Horizontal cross arm
        for x in range(12, 20):
            put(px, x, 14, etching_color)
    # Central boss gem
    if gem_color:
        cx, cy = 15, 14
        cells = {
            (-1, -1): gem_color, (0, -1): gem_color, (1, -1): gem_color,
            (-1, 0):  gem_color, (0, 0):  (255, 255, 255, 255), (1, 0):   gem_color,
            (-1, 1):  gem_color, (0, 1):  gem_color, (1, 1): gem_color,
        }
        for (dx, dy), c in cells.items():
            put(px, cx + dx, cy + dy, c)
    return img


# ===========================================================
# REUSE TIER PALETTES + MW CONFIGS FROM PHASE 12
# ===========================================================
import sys
sys.path.insert(0, "/home/sparky/ogrs/art/items")
import _draw_phase12_platebodies as p12

TIERS = p12.TIERS
MW_CONFIGS = p12.MW_CONFIGS
mw_palette = p12.mw_palette


# ===========================================================
# DRIVER
# ===========================================================
if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/armor"
    os.makedirs(out, exist_ok=True)

    # Phase 13 — Legs
    print("--- Phase 13: Plate legs ---")
    for tier_name, palette in TIERS:
        img = draw_legs(palette)
        img.save(f"{out}/legs_{tier_name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/legs_{tier_name}_x8.png")

        cfg = MW_CONFIGS[tier_name]
        img_mw = draw_legs(
            mw_palette(palette),
            gem_color=cfg['gem'],
            trim_color=cfg['trim'],
            glow_color=cfg['glow'],
            etching_color=cfg['etching'],
        )
        img_mw.save(f"{out}/legs_{tier_name}_mw.png")
        img_mw.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/legs_{tier_name}_mw_x8.png")
        print(f"  done: legs_{tier_name} + mw")

    # Phase 14 — Helms (with optional plume on MW)
    print("--- Phase 14: Full helms ---")
    plume_colors = {
        'bronze':  (200,  60,  60, 255),
        'iron':    (200,  60,  60, 255),
        'steel':   (220,  60,  60, 255),
        'black':   (180,  20,  20, 255),
        'mithril': (220, 220, 240, 255),
        'adamant': (180, 220, 100, 255),
        'rune':    (180, 220, 255, 255),
    }
    for tier_name, palette in TIERS:
        img = draw_helm(palette)
        img.save(f"{out}/helm_{tier_name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/helm_{tier_name}_x8.png")

        cfg = MW_CONFIGS[tier_name]
        img_mw = draw_helm(
            mw_palette(palette),
            gem_color=cfg['gem'],
            trim_color=cfg['trim'],
            glow_color=cfg['glow'],
            etching_color=cfg['etching'],
            has_plume=True,
            plume_color=plume_colors[tier_name],
        )
        img_mw.save(f"{out}/helm_{tier_name}_mw.png")
        img_mw.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/helm_{tier_name}_mw_x8.png")
        print(f"  done: helm_{tier_name} + mw")

    # Phase 15 — Shields
    print("--- Phase 15: Kite shields ---")
    for tier_name, palette in TIERS:
        img = draw_shield(palette)
        img.save(f"{out}/shield_{tier_name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/shield_{tier_name}_x8.png")

        cfg = MW_CONFIGS[tier_name]
        img_mw = draw_shield(
            mw_palette(palette),
            gem_color=cfg['gem'],
            trim_color=cfg['trim'],
            glow_color=cfg['glow'],
            etching_color=cfg['etching'],
        )
        img_mw.save(f"{out}/shield_{tier_name}_mw.png")
        img_mw.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/shield_{tier_name}_mw_x8.png")
        print(f"  done: shield_{tier_name} + mw")

    print(f"\n=== Phase 13-15 complete: 42 armor sprites ===")
