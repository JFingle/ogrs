#!/usr/bin/env python3
"""
Seed tiers v2 — loose handfuls, NO container.

Per Sparky feedback 2026-05-20: drop the pouch/bag concept. Seeds are
drawn as loose clusters at increasing density per tier — same approach
as coin tiers but with crop-distinct seed shapes.

12 crops × 4 tiers = 48 sprites at 32×32:
  - Tier 1 (qty 1)   : 1 seed centered
  - Tier 2 (qty 2-5) : ~5 seeds in a small cluster
  - Tier 3 (qty 10+) : ~15 seeds piled, slightly overlapping
  - Tier 4 (qty 50+) : ~35 seeds heaped, dense overlap
"""
import math, os
from PIL import Image

W = H = 32
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# Per-crop seed definitions: (palette, shape_function)
# shape_function(px, x, y, palette) draws ONE seed at the given center.

def shape_oval(px, x, y, dk, base, hi):
    """3-wide × 2-tall oval (potato, lettuce, cucumber)."""
    put(px, x - 1, y,     dk)
    put(px, x,     y,     hi)
    put(px, x + 1, y,     base)
    put(px, x,     y + 1, dk)


def shape_round(px, x, y, dk, base, hi):
    """Tiny 3×3 round (onion, cabbage, carrot)."""
    put(px, x,     y - 1, dk)
    put(px, x - 1, y,     dk)
    put(px, x,     y,     hi)
    put(px, x + 1, y,     base)
    put(px, x,     y + 1, dk)


def shape_drop(px, x, y, dk, base, hi):
    """2-wide × 3-tall teardrop (tomato, bellpepper)."""
    put(px, x,     y - 1, dk)
    put(px, x - 1, y,     base)
    put(px, x,     y,     hi)
    put(px, x + 1, y,     dk)
    put(px, x,     y + 1, dk)


def shape_kidney(px, x, y, dk, base, hi):
    """4-wide × 2-tall kidney bean shape (beans)."""
    put(px, x - 2, y,     dk)
    put(px, x - 1, y,     base)
    put(px, x,     y,     hi)
    put(px, x + 1, y,     base)
    put(px, x + 2, y,     dk)
    put(px, x - 1, y + 1, dk)
    put(px, x,     y + 1, dk)
    put(px, x + 1, y + 1, dk)


def shape_kernel(px, x, y, dk, base, hi):
    """Corn kernel — wider teardrop (corn)."""
    put(px, x,     y - 1, dk)
    put(px, x - 1, y,     dk)
    put(px, x,     y,     hi)
    put(px, x + 1, y,     base)
    put(px, x,     y + 1, base)
    put(px, x - 1, y + 1, dk)
    put(px, x + 1, y + 1, dk)


def shape_garlic_clove(px, x, y, dk, base, hi):
    """Pointed clove (garlic)."""
    put(px, x,     y - 2, dk)
    put(px, x - 1, y - 1, dk)
    put(px, x,     y - 1, hi)
    put(px, x + 1, y - 1, dk)
    put(px, x - 1, y,     base)
    put(px, x,     y,     hi)
    put(px, x + 1, y,     base)
    put(px, x,     y + 1, dk)


def shape_pea(px, x, y, dk, base, hi):
    """Small green sphere (peas)."""
    put(px, x - 1, y, dk)
    put(px, x,     y, hi)
    put(px, x + 1, y, base)
    put(px, x,     y + 1, dk)


CROPS = {
    'potato':     {'shape': shape_oval,   'palette': ((138, 108,  50), (200, 174, 100), (240, 220, 150))},
    'onion':      {'shape': shape_round,  'palette': (( 48,  20,  10), ( 96,  48,  16), (148,  90,  40))},
    'tomato':     {'shape': shape_drop,   'palette': ((140, 110,  20), (210, 170,  60), (255, 220, 110))},
    'cabbage':    {'shape': shape_round,  'palette': (( 30,  60,  20), ( 60, 100,  40), (110, 160,  70))},
    'lettuce':    {'shape': shape_oval,   'palette': (( 90,  70,  20), (170, 150,  70), (220, 210, 130))},
    'garlic':     {'shape': shape_garlic_clove, 'palette': ((120, 100,  60), (200, 190, 160), (250, 245, 230))},
    'beans':      {'shape': shape_kidney, 'palette': (( 90,  30,  20), (160,  70,  40), (210, 110,  70))},
    'peas':       {'shape': shape_pea,    'palette': (( 40,  90,  30), ( 90, 160,  60), (160, 220, 110))},
    'corn':       {'shape': shape_kernel, 'palette': ((180, 130,  20), (230, 190,  60), (255, 230, 130))},
    'carrot':     {'shape': shape_round,  'palette': ((130,  60,  10), (190,  90,  30), (240, 140,  70))},
    'cucumber':   {'shape': shape_oval,   'palette': (( 90, 110,  40), (140, 170,  70), (200, 220, 130))},
    'bellpepper': {'shape': shape_drop,   'palette': ((100,  20,  10), (180,  40,  20), (240,  90,  60))},
}


# Tier positions — clusters at increasing density
# Position is offset from the canvas center (CX=16, CY=16)
CX, CY = 16, 16

TIER1_POS = [(0, 0)]   # single centered seed

TIER2_POS = [
    (-2, -3), (3, -2), (-3, 2), (2, 3), (0, 0),
]

TIER3_POS = [
    # 15 seeds in a heart-ish cluster
    (-4, -5), (0, -5), (4, -5),
    (-5, -2), (-2, -2), (2, -2), (5, -2),
    (-4, 1), (0, 1), (4, 1),
    (-3, 4), (3, 4),
    (-1, 6), (2, 6), (0, 3),
]

TIER4_POS = [
    # ~35 seeds in a dense pile
    # Back row (smallest perspective)
    (-8, -8), (-4, -8), (0, -8), (4, -8), (8, -8),
    # Mid-back
    (-9, -5), (-5, -5), (-1, -5), (3, -5), (7, -5),
    # Middle layer
    (-10, -2), (-6, -2), (-2, -2), (2, -2), (6, -2), (10, -2),
    # Lower middle
    (-9, 2), (-5, 2), (-1, 2), (3, 2), (7, 2),
    # Front row (densest)
    (-10, 6), (-6, 6), (-2, 6), (2, 6), (6, 6), (10, 6),
    # Very front
    (-8, 9), (-4, 9), (0, 9), (4, 9), (8, 9),
]


def draw_tier(crop_name, tier):
    positions = {1: TIER1_POS, 2: TIER2_POS, 3: TIER3_POS, 4: TIER4_POS}[tier]
    cfg = CROPS[crop_name]
    shape_fn = cfg['shape']
    dk, base, hi = cfg['palette']
    dk = (*dk, 255); base = (*base, 255); hi = (*hi, 255)

    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    for (dx, dy) in positions:
        shape_fn(px, CX + dx, CY + dy, dk, base, hi)
    return img


if __name__ == "__main__":
    for crop in CROPS.keys():
        out = f"/home/sparky/ogrs/art/items/seeds/{crop}/tiers"
        # Clear old tier files first
        os.makedirs(out, exist_ok=True)
        for old in os.listdir(out):
            if old.startswith('tier_'):
                os.remove(os.path.join(out, old))
        for tier in (1, 2, 3, 4):
            img = draw_tier(crop, tier)
            img.save(f"{out}/tier_{tier}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/tier_{tier}_x8.png")
        print(f"done: {crop}")
    print("\n=== Seeds v2 complete: 12 crops × 4 tiers = 48 sprites ===")
