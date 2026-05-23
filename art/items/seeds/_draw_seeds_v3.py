#!/usr/bin/env python3
"""
Seeds v3 — bigger, 3 tiers only, accurate per-crop shapes.

Iteration notes (Sparky 2026-05-20):
  - v2 seeds were too small (~2-3 px) — hard to read on the ground
  - v2 had 4 tiers; T4 (50+) too crowded — drop it
  - shapes should match real seeds so you can tell what's planted

NEW TIER SCHEME (3 tiers):
  T1 (qty 1)   : 1 big seed centered
  T2 (qty 2-9) : 5-7 seeds clustered
  T3 (qty 10+) : ~22 seeds heaped (new MAX, slightly more than v2 T3)

SEEDS NOW ~5-6 px EACH (up from 2-3 px) so they read on dropped-item icons.

Real seed reference research:
  potato     : pale tan oval (~2mm)  — flat ellipse with light fuzz
  onion      : black teardrop        — distinct curve, very dark
  tomato     : pale tan, fuzzy oval  — almost looks like flat lentil
  cabbage    : tiny dark brown round — small dark sphere
  lettuce    : pointed light tan oval — like rice but smaller
  garlic     : white wedge (clove)   — actually a clove not a seed, fine for game
  beans      : kidney shape, red-brown — ICONIC bean silhouette
  peas       : small green sphere    — basically a tiny pea
  corn       : yellow kernel         — teardrop with flat top
  carrot     : tan elongated         — very small, almost dust
  cucumber   : pale tan flat oval    — similar to tomato
  bell pep   : flat cream-yellow     — small flat disc

TIER-2 crops:
  mushroom   : brown spore dust      — tiny dark specks (mushrooms reproduce by spores)
  strawberry : red-brown speck       — like tomato but reddish
  blueberry  : dark blue oval        — small dark blue
  hot pepper : pale yellow drop      — similar to bell pepper but smaller
  rice       : long white grain      — distinctive long shape
  eggplant   : tan flat oval         — similar to cucumber
  zucchini   : pale flat oval        — similar to cucumber
  spinach    : dark brown angular    — small dark angular
  pumpkin    : large pale tan oval   — biggest seed of the set

"""
import os
from PIL import Image

W = H = 32
TRANS = (0, 0, 0, 0)
CX, CY = 16, 16


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# ===========================================================
# Bigger seed shape functions (each ~5-6 px)
# Each takes (px, cx, cy, dk, base, hi) and stamps a seed.
# ===========================================================

def shape_oval_big(px, cx, cy, dk, base, hi):
    """4×3 flat oval — potato, lettuce, cucumber, tomato, eggplant, zucchini.
    Pale flat seed look."""
    cells = {
        (-1, -1): dk, (0, -1): dk, (1, -1): dk,
        (-2, 0): dk, (-1, 0): hi, (0, 0): hi, (1, 0): base, (2, 0): dk,
        (-1, 1): dk, (0, 1): base, (1, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_teardrop_big(px, cx, cy, dk, base, hi):
    """3×4 teardrop — onion (dark), tomato variant."""
    cells = {
        (0, -2): dk,
        (-1, -1): dk, (0, -1): hi, (1, -1): dk,
        (-1, 0): dk, (0, 0): base, (1, 0): dk,
        (0, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_round_big(px, cx, cy, dk, base, hi):
    """4×4 round bead — cabbage, peas, blueberry."""
    cells = {
        (-1, -2): dk, (0, -2): dk,
        (-2, -1): dk, (-1, -1): hi, (0, -1): base, (1, -1): dk,
        (-2, 0): dk, (-1, 0): base, (0, 0): base, (1, 0): dk,
        (-1, 1): dk, (0, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_kidney_big(px, cx, cy, dk, base, hi):
    """6×3 kidney bean — iconic."""
    cells = {
        (-2, -1): dk, (-1, -1): dk, (0, -1): dk, (1, -1): dk, (2, -1): dk,
        (-2, 0): dk, (-1, 0): hi, (0, 0): hi, (1, 0): base, (2, 0): base, (3, 0): dk,
        (-2, 1): dk, (-1, 1): dk, (0, 1): dk, (1, 1): dk, (2, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_kernel_big(px, cx, cy, dk, base, hi):
    """3×4 corn kernel — rounded top, flat bottom."""
    cells = {
        (-1, -2): dk, (0, -2): dk,
        (-1, -1): hi, (0, -1): base, (1, -1): dk,
        (-1, 0): base, (0, 0): base, (1, 0): dk,
        (-1, 1): dk, (0, 1): dk, (1, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_clove_big(px, cx, cy, dk, base, hi):
    """3×4 pointed wedge — garlic clove."""
    cells = {
        (0, -2): dk,
        (-1, -1): dk, (0, -1): hi, (1, -1): dk,
        (-1, 0): dk, (0, 0): base, (1, 0): dk,
        (-1, 1): dk, (0, 1): dk, (1, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_grain_big(px, cx, cy, dk, base, hi):
    """5×2 long grain — rice."""
    cells = {
        (-2, 0): dk, (-1, 0): hi, (0, 0): base, (1, 0): base, (2, 0): dk,
        (-1, 1): dk, (0, 1): dk, (1, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_speck_big(px, cx, cy, dk, base, hi):
    """3×3 small speck — strawberry, carrot (small seeds)."""
    cells = {
        (0, -1): dk,
        (-1, 0): dk, (0, 0): hi, (1, 0): base,
        (0, 1): dk,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def shape_dot_big(px, cx, cy, dk, base, hi):
    """2×2 micro speck — mushroom spore dust."""
    cells = {
        (-1, -1): dk, (0, -1): hi,
        (-1, 0): dk, (0, 0): base,
    }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


# ===========================================================
# Per-crop registry — shape + palette
# Palette: (dark, base, highlight) RGB triples
# ===========================================================

CROPS = {
    # Phase 1 crops
    'potato':     {'shape': shape_oval_big,     'pal': ((140, 110,  70), (200, 175, 130), (240, 220, 180))},
    'onion':      {'shape': shape_teardrop_big, 'pal': (( 20,  18,  20), ( 50,  44,  48), ( 90,  78,  80))},
    'tomato':     {'shape': shape_oval_big,     'pal': ((180, 150,  90), (220, 200, 150), (245, 230, 195))},
    'cabbage':    {'shape': shape_round_big,    'pal': (( 40,  30,  20), ( 80,  60,  40), (130, 100,  70))},
    'lettuce':    {'shape': shape_oval_big,     'pal': ((120, 100,  60), (180, 160, 110), (225, 210, 170))},
    'garlic':     {'shape': shape_clove_big,    'pal': ((150, 140, 110), (220, 215, 195), (250, 248, 235))},
    'beans':      {'shape': shape_kidney_big,   'pal': (( 70,  20,  10), (140,  60,  40), (200, 110,  80))},
    'peas':       {'shape': shape_round_big,    'pal': (( 40,  90,  30), ( 90, 170,  60), (160, 220, 110))},
    'corn':       {'shape': shape_kernel_big,   'pal': ((160, 110,  20), (230, 190,  50), (255, 230, 110))},
    'carrot':     {'shape': shape_speck_big,    'pal': ((130,  90,  40), (180, 140,  80), (220, 190, 140))},
    'cucumber':   {'shape': shape_oval_big,     'pal': ((150, 130,  60), (200, 180, 110), (235, 220, 170))},
    'bellpepper': {'shape': shape_oval_big,     'pal': ((170, 150,  60), (220, 200, 110), (250, 235, 175))},
    # Phase 2 crops
    'mushroom':   {'shape': shape_dot_big,      'pal': (( 50,  30,  20), ( 90,  60,  40), (130,  90,  60))},
    'strawberry': {'shape': shape_speck_big,    'pal': ((120,  60,  20), (180, 100,  50), (220, 150,  90))},
    'blueberry':  {'shape': shape_round_big,    'pal': (( 20,  20,  60), ( 40,  40, 110), ( 80,  80, 170))},
    'hotpepper':  {'shape': shape_oval_big,     'pal': ((170, 140,  60), (220, 190, 110), (250, 230, 170))},
    'rice':       {'shape': shape_grain_big,    'pal': ((180, 170, 140), (230, 225, 210), (255, 255, 250))},
    'eggplant':   {'shape': shape_oval_big,     'pal': ((140, 120,  60), (190, 170, 110), (225, 210, 165))},
    'zucchini':   {'shape': shape_oval_big,     'pal': ((140, 130,  60), (200, 190, 120), (235, 225, 175))},
    'spinach':    {'shape': shape_speck_big,    'pal': (( 40,  30,  10), ( 90,  70,  30), (140, 110,  50))},
    'pumpkin':    {'shape': shape_oval_big,     'pal': ((130, 100,  50), (190, 160, 100), (230, 210, 160))},
}


# ===========================================================
# Tier layouts — at 5-6 px per seed, positions need more spacing
# ===========================================================

TIER1_POS = [(0, 0)]

# 5 seeds clustered — spacing 6 px to avoid overlap
TIER2_POS = [
    (-4, -4),
    (4, -3),
    (-5, 3),
    (3, 4),
    (0, 0),
]

# ~22 seeds piled — wider layout but still readable
TIER3_POS = [
    # Back row (smallest)
    (-9, -6), (-3, -7), (3, -7), (9, -6),
    # Mid-back
    (-11, -2), (-5, -3), (1, -3), (7, -3),
    # Middle layer
    (-9, 2), (-3, 1), (3, 1), (9, 2),
    # Lower middle
    (-11, 6), (-5, 5), (1, 5), (7, 5),
    # Front row (densest)
    (-9, 9), (-3, 8), (3, 8), (9, 9),
    # Loose front
    (-6, 11), (6, 11),
]


def draw_tier(crop_name, tier):
    cfg = CROPS[crop_name]
    shape_fn = cfg['shape']
    dk, base, hi = cfg['pal']
    dk = (*dk, 255); base = (*base, 255); hi = (*hi, 255)

    positions = {1: TIER1_POS, 2: TIER2_POS, 3: TIER3_POS}[tier]
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    for (dx, dy) in positions:
        shape_fn(px, CX + dx, CY + dy, dk, base, hi)
    return img


if __name__ == "__main__":
    for crop in CROPS.keys():
        out = f"/home/sparky/ogrs/art/items/seeds/{crop}/tiers"
        os.makedirs(out, exist_ok=True)
        # Clear old tier files
        for old in os.listdir(out):
            if old.startswith('tier_'):
                os.remove(os.path.join(out, old))
        for tier in (1, 2, 3):
            img = draw_tier(crop, tier)
            img.save(f"{out}/tier_{tier}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/tier_{tier}_x8.png")
        print(f"done: {crop}")
    print(f"\n=== Seeds v3 complete: {len(CROPS)} crops × 3 tiers = {len(CROPS)*3} sprites ===")
