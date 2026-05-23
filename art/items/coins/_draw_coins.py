#!/usr/bin/env python3
"""
Coin stack tiers — 6 sprites at 32×32.

Each tier shows progressively more coins so a glance tells the player
how much they're carrying. Engine work needed: pick tier by stack qty.

Suggested thresholds (typical RSC/OSRS convention):
  tier_1 :     1 coin
  tier_2 :  2-3 coins
  tier_3 :  4-9 coins
  tier_4 : 10-49 coins
  tier_5 : 50-249 coins
  tier_6 : 250+ coins
"""
import os
from PIL import Image

W = H = 32
TRANS = (0, 0, 0, 0)

# Classic RSC gold palette
OUTLINE   = ( 60,  38,   8, 255)
GOLD_SHAD = (138,  88,  12, 255)
GOLD_BASE = (208, 150,  28, 255)
GOLD_HI   = (250, 210,  60, 255)
GOLD_PEAK = (255, 240, 150, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def draw_coin(px, cx, cy, size='med'):
    """Draw a single coin centered at (cx, cy). size in {'small','med','large'}."""
    if size == 'small':
        # 5×5 simple disc
        cells = {
            (-1, -2): OUTLINE, (0, -2): OUTLINE, (1, -2): OUTLINE,
            (-2, -1): OUTLINE, (-1, -1): GOLD_HI, (0, -1): GOLD_HI, (1, -1): GOLD_BASE, (2, -1): OUTLINE,
            (-2, 0): OUTLINE, (-1, 0): GOLD_HI, (0, 0): GOLD_BASE, (1, 0): GOLD_BASE, (2, 0): OUTLINE,
            (-2, 1): OUTLINE, (-1, 1): GOLD_BASE, (0, 1): GOLD_SHAD, (1, 1): GOLD_SHAD, (2, 1): OUTLINE,
            (-1, 2): OUTLINE, (0, 2): OUTLINE, (1, 2): OUTLINE,
        }
    elif size == 'med':
        # 7×7 disc with proper shading
        cells = {
            (-1, -3): OUTLINE, (0, -3): OUTLINE, (1, -3): OUTLINE,
            (-2, -2): OUTLINE, (-1, -2): GOLD_PEAK, (0, -2): GOLD_HI, (1, -2): GOLD_HI, (2, -2): OUTLINE,
            (-3, -1): OUTLINE, (-2, -1): GOLD_HI, (-1, -1): GOLD_HI, (0, -1): GOLD_HI, (1, -1): GOLD_BASE, (2, -1): GOLD_BASE, (3, -1): OUTLINE,
            (-3, 0): OUTLINE, (-2, 0): GOLD_HI, (-1, 0): GOLD_BASE, (0, 0): GOLD_BASE, (1, 0): GOLD_BASE, (2, 0): GOLD_SHAD, (3, 0): OUTLINE,
            (-3, 1): OUTLINE, (-2, 1): GOLD_BASE, (-1, 1): GOLD_BASE, (0, 1): GOLD_SHAD, (1, 1): GOLD_SHAD, (2, 1): GOLD_SHAD, (3, 1): OUTLINE,
            (-2, 2): OUTLINE, (-1, 2): GOLD_BASE, (0, 2): GOLD_SHAD, (1, 2): GOLD_SHAD, (2, 2): OUTLINE,
            (-1, 3): OUTLINE, (0, 3): OUTLINE, (1, 3): OUTLINE,
        }
    else:  # large
        # 9×9 detailed coin (for tier 1 single-coin focus)
        cells = {
            (-2, -4): OUTLINE, (-1, -4): OUTLINE, (0, -4): OUTLINE, (1, -4): OUTLINE, (2, -4): OUTLINE,
            (-3, -3): OUTLINE, (-2, -3): GOLD_PEAK, (-1, -3): GOLD_PEAK, (0, -3): GOLD_HI, (1, -3): GOLD_HI, (2, -3): GOLD_HI, (3, -3): OUTLINE,
            (-4, -2): OUTLINE, (-3, -2): GOLD_PEAK, (-2, -2): GOLD_HI, (-1, -2): GOLD_HI, (0, -2): GOLD_HI, (1, -2): GOLD_BASE, (2, -2): GOLD_BASE, (3, -2): GOLD_BASE, (4, -2): OUTLINE,
            (-4, -1): OUTLINE, (-3, -1): GOLD_HI, (-2, -1): GOLD_HI, (-1, -1): GOLD_HI, (0, -1): GOLD_BASE, (1, -1): GOLD_BASE, (2, -1): GOLD_BASE, (3, -1): GOLD_SHAD, (4, -1): OUTLINE,
            (-4, 0): OUTLINE, (-3, 0): GOLD_HI, (-2, 0): GOLD_BASE, (-1, 0): GOLD_BASE, (0, 0): GOLD_BASE, (1, 0): GOLD_BASE, (2, 0): GOLD_SHAD, (3, 0): GOLD_SHAD, (4, 0): OUTLINE,
            (-4, 1): OUTLINE, (-3, 1): GOLD_BASE, (-2, 1): GOLD_BASE, (-1, 1): GOLD_BASE, (0, 1): GOLD_BASE, (1, 1): GOLD_SHAD, (2, 1): GOLD_SHAD, (3, 1): GOLD_SHAD, (4, 1): OUTLINE,
            (-4, 2): OUTLINE, (-3, 2): GOLD_BASE, (-2, 2): GOLD_BASE, (-1, 2): GOLD_SHAD, (0, 2): GOLD_SHAD, (1, 2): GOLD_SHAD, (2, 2): GOLD_SHAD, (3, 2): GOLD_SHAD, (4, 2): OUTLINE,
            (-3, 3): OUTLINE, (-2, 3): GOLD_SHAD, (-1, 3): GOLD_SHAD, (0, 3): GOLD_SHAD, (1, 3): GOLD_SHAD, (2, 3): GOLD_SHAD, (3, 3): OUTLINE,
            (-2, 4): OUTLINE, (-1, 4): OUTLINE, (0, 4): OUTLINE, (1, 4): OUTLINE, (2, 4): OUTLINE,
        }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


# ===========================================================
# 6 tier layouts
# ===========================================================

def tier1():
    """Single big coin centered."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_coin(px, 16, 16, size='large')
    # Sparkle
    put(px, 11, 11, GOLD_PEAK)
    return img


def tier2():
    """2 medium coins overlapping."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_coin(px, 12, 18, size='med')
    draw_coin(px, 20, 14, size='med')
    return img


def tier3():
    """3-4 coins in a small cluster."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_coin(px, 11, 20, size='med')
    draw_coin(px, 20, 20, size='med')
    draw_coin(px, 15, 13, size='med')
    return img


def tier4():
    """Small pile — coins stacked, 5-7 visible."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Back row (smaller appearing)
    draw_coin(px, 10, 16, size='small')
    draw_coin(px, 16, 14, size='small')
    draw_coin(px, 22, 16, size='small')
    # Front row
    draw_coin(px, 11, 22, size='med')
    draw_coin(px, 20, 22, size='med')
    draw_coin(px, 16, 19, size='med')
    return img


def tier5():
    """Larger pile — about a dozen coins."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Pile mound formed by overlapping small + medium coins
    # Back layer
    for cx, cy in [(8, 14), (14, 12), (20, 12), (26, 14), (17, 10)]:
        draw_coin(px, cx, cy, size='small')
    # Mid layer
    for cx, cy in [(10, 18), (16, 16), (22, 18)]:
        draw_coin(px, cx, cy, size='med')
    # Front layer
    for cx, cy in [(8, 24), (14, 23), (20, 23), (26, 24)]:
        draw_coin(px, cx, cy, size='med')
    return img


def tier6():
    """Overflowing pile + a few loose coins around the heap."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Heap interior — densely packed coins
    for cx, cy in [(8, 12), (14, 10), (20, 10), (26, 12), (17, 7), (11, 8), (23, 8)]:
        draw_coin(px, cx, cy, size='small')
    for cx, cy in [(10, 16), (16, 14), (22, 16), (8, 19), (24, 19)]:
        draw_coin(px, cx, cy, size='med')
    for cx, cy in [(8, 24), (14, 23), (20, 23), (26, 24), (16, 26)]:
        draw_coin(px, cx, cy, size='med')
    # Loose coins around
    put(px, 4, 26, GOLD_BASE); put(px, 3, 27, OUTLINE); put(px, 5, 27, OUTLINE); put(px, 4, 28, OUTLINE)
    put(px, 28, 27, GOLD_BASE); put(px, 27, 28, OUTLINE); put(px, 29, 28, OUTLINE)
    return img


TIERS = [
    ("tier_1_single",      1, tier1),
    ("tier_2_pair",        2, tier2),
    ("tier_3_cluster",     3, tier3),
    ("tier_4_pile",        4, tier4),
    ("tier_5_heap",        5, tier5),
    ("tier_6_overflow",    6, tier6),
]

if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/coins/tiers"
    os.makedirs(out, exist_ok=True)
    for name, _, fn in TIERS:
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {name}")
