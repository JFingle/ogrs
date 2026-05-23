#!/usr/bin/env python3
"""
Coins v2 — OSRS-style stacks.

Tier 1-4  : top-down view of small round coins (1, 2, 3, 4 coins)
Tier 5-6  : side view of vertical stack (coins seen edge-on, stacked up)
            5+ becomes a stack, height scales with quantity

Suggested thresholds:
  tier_1 :  1 coin       single round
  tier_2 :  2 coins      two side-by-side
  tier_3 :  3 coins      triangular cluster
  tier_4 :  4 coins      2x2 cluster
  tier_5 : 5-99 coins    small stack (~6 coins tall, side view)
  tier_6 : 100+ coins    tall overflowing stack
"""
import os
from PIL import Image

W = H = 32
TRANS = (0, 0, 0, 0)

OUTLINE   = ( 60,  38,   8, 255)
GOLD_SHAD = (138,  88,  12, 255)
GOLD_BASE = (208, 150,  28, 255)
GOLD_HI   = (250, 210,  60, 255)
GOLD_PEAK = (255, 240, 150, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def draw_round_coin(px, cx, cy, big=False):
    """Top-down view of a coin. Used for tiers 1-4."""
    if big:
        # 11×11 large coin (used for tier 1 hero shot)
        cells = {
            (-2, -5): OUTLINE, (-1, -5): OUTLINE, (0, -5): OUTLINE, (1, -5): OUTLINE, (2, -5): OUTLINE,
            (-3, -4): OUTLINE, (-2, -4): GOLD_PEAK, (-1, -4): GOLD_HI, (0, -4): GOLD_HI, (1, -4): GOLD_HI, (2, -4): GOLD_HI, (3, -4): OUTLINE,
            (-4, -3): OUTLINE, (-3, -3): GOLD_PEAK, (-2, -3): GOLD_HI, (-1, -3): GOLD_HI, (0, -3): GOLD_HI, (1, -3): GOLD_BASE, (2, -3): GOLD_BASE, (3, -3): GOLD_BASE, (4, -3): OUTLINE,
            (-5, -2): OUTLINE, (-4, -2): GOLD_PEAK, (-3, -2): GOLD_HI, (-2, -2): GOLD_HI, (-1, -2): GOLD_BASE, (0, -2): GOLD_BASE, (1, -2): GOLD_BASE, (2, -2): GOLD_BASE, (3, -2): GOLD_BASE, (4, -2): GOLD_SHAD, (5, -2): OUTLINE,
            (-5, -1): OUTLINE, (-4, -1): GOLD_HI, (-3, -1): GOLD_HI, (-2, -1): GOLD_BASE, (-1, -1): GOLD_BASE, (0, -1): GOLD_BASE, (1, -1): GOLD_BASE, (2, -1): GOLD_BASE, (3, -1): GOLD_SHAD, (4, -1): GOLD_SHAD, (5, -1): OUTLINE,
            (-5, 0): OUTLINE, (-4, 0): GOLD_HI, (-3, 0): GOLD_BASE, (-2, 0): GOLD_BASE, (-1, 0): GOLD_BASE, (0, 0): GOLD_BASE, (1, 0): GOLD_BASE, (2, 0): GOLD_SHAD, (3, 0): GOLD_SHAD, (4, 0): GOLD_SHAD, (5, 0): OUTLINE,
            (-5, 1): OUTLINE, (-4, 1): GOLD_BASE, (-3, 1): GOLD_BASE, (-2, 1): GOLD_BASE, (-1, 1): GOLD_BASE, (0, 1): GOLD_SHAD, (1, 1): GOLD_SHAD, (2, 1): GOLD_SHAD, (3, 1): GOLD_SHAD, (4, 1): GOLD_SHAD, (5, 1): OUTLINE,
            (-5, 2): OUTLINE, (-4, 2): GOLD_BASE, (-3, 2): GOLD_BASE, (-2, 2): GOLD_SHAD, (-1, 2): GOLD_SHAD, (0, 2): GOLD_SHAD, (1, 2): GOLD_SHAD, (2, 2): GOLD_SHAD, (3, 2): GOLD_SHAD, (4, 2): GOLD_SHAD, (5, 2): OUTLINE,
            (-4, 3): OUTLINE, (-3, 3): GOLD_SHAD, (-2, 3): GOLD_SHAD, (-1, 3): GOLD_SHAD, (0, 3): GOLD_SHAD, (1, 3): GOLD_SHAD, (2, 3): GOLD_SHAD, (3, 3): GOLD_SHAD, (4, 3): OUTLINE,
            (-3, 4): OUTLINE, (-2, 4): GOLD_SHAD, (-1, 4): GOLD_SHAD, (0, 4): GOLD_SHAD, (1, 4): GOLD_SHAD, (2, 4): GOLD_SHAD, (3, 4): OUTLINE,
            (-2, 5): OUTLINE, (-1, 5): OUTLINE, (0, 5): OUTLINE, (1, 5): OUTLINE, (2, 5): OUTLINE,
        }
    else:
        # 7×7 standard coin (for tiers 2-4 clusters)
        cells = {
            (-1, -3): OUTLINE, (0, -3): OUTLINE, (1, -3): OUTLINE,
            (-2, -2): OUTLINE, (-1, -2): GOLD_PEAK, (0, -2): GOLD_HI, (1, -2): GOLD_HI, (2, -2): OUTLINE,
            (-3, -1): OUTLINE, (-2, -1): GOLD_HI, (-1, -1): GOLD_HI, (0, -1): GOLD_HI, (1, -1): GOLD_BASE, (2, -1): GOLD_BASE, (3, -1): OUTLINE,
            (-3, 0): OUTLINE, (-2, 0): GOLD_HI, (-1, 0): GOLD_BASE, (0, 0): GOLD_BASE, (1, 0): GOLD_BASE, (2, 0): GOLD_SHAD, (3, 0): OUTLINE,
            (-3, 1): OUTLINE, (-2, 1): GOLD_BASE, (-1, 1): GOLD_BASE, (0, 1): GOLD_SHAD, (1, 1): GOLD_SHAD, (2, 1): GOLD_SHAD, (3, 1): OUTLINE,
            (-2, 2): OUTLINE, (-1, 2): GOLD_BASE, (0, 2): GOLD_SHAD, (1, 2): GOLD_SHAD, (2, 2): OUTLINE,
            (-1, 3): OUTLINE, (0, 3): OUTLINE, (1, 3): OUTLINE,
        }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)


def draw_stack_layer(px, cx, cy, w=14, gap_color=GOLD_SHAD):
    """Side view of a single coin in a stack — thin horizontal ellipse.
    Draws at y, occupying 2-3 rows."""
    # Top edge (highlight)
    for dx in range(-w//2 + 1, w//2):
        put(px, cx + dx, cy - 1, GOLD_HI)
    # Middle (base)
    put(px, cx - w//2, cy, OUTLINE)
    for dx in range(-w//2 + 1, w//2):
        put(px, cx + dx, cy, GOLD_BASE)
    put(px, cx + w//2 - 1, cy, GOLD_SHAD)
    put(px, cx + w//2, cy, OUTLINE)
    # Bottom (shadow line — separates from coin below)
    for dx in range(-w//2 + 1, w//2):
        put(px, cx + dx, cy + 1, GOLD_SHAD)
    # Outline ends
    put(px, cx - w//2, cy - 1, OUTLINE)
    put(px, cx + w//2, cy - 1, OUTLINE)
    put(px, cx - w//2, cy + 1, OUTLINE)
    put(px, cx + w//2, cy + 1, OUTLINE)


def draw_stack_top(px, cx, cy, w=14):
    """Top of stack — a coin face visible from above-side."""
    # Top arc (round-ish top)
    for dx in range(-w//2 + 1, w//2):
        put(px, cx + dx, cy, OUTLINE)
    for dx in range(-w//2 + 2, w//2 - 1):
        put(px, cx + dx, cy + 1, GOLD_PEAK)
    for dx in range(-w//2 + 1, w//2):
        put(px, cx + dx, cy + 2, GOLD_HI)


# ===========================================================
# TIERS
# ===========================================================

def tier1():
    """1 coin — big single coin centered."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_round_coin(px, 16, 16, big=True)
    return img


def tier2():
    """2 coins — side by side, slightly overlapping."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_round_coin(px, 12, 17, big=False)
    draw_round_coin(px, 20, 15, big=False)
    return img


def tier3():
    """3 coins — triangle cluster."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_round_coin(px, 11, 20, big=False)
    draw_round_coin(px, 21, 20, big=False)
    draw_round_coin(px, 16, 12, big=False)
    return img


def tier4():
    """Short stack — 4 coins side-view, the FIRST stack tier."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    base_y = 22
    # Stack of 4 coins
    for i in range(4):
        y = base_y - i * 2
        draw_stack_layer(px, 16, y, w=14)
    # Top
    draw_stack_top(px, 16, base_y - 4 * 2 - 1, w=14)
    return img


def tier5():
    """Medium stack — 7 coins, taller than tier 4."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    base_y = 25
    for i in range(7):
        y = base_y - i * 2
        draw_stack_layer(px, 16, y, w=14)
    draw_stack_top(px, 16, base_y - 7 * 2 - 1, w=14)
    return img


def tier6():
    """Tall stack — 11 coins + loose ones spilling around."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    base_y = 28
    for i in range(11):
        y = base_y - i * 2
        draw_stack_layer(px, 16, y, w=14)
    draw_stack_top(px, 16, base_y - 11 * 2 - 1, w=14)
    # Spilled coins around the base
    draw_round_coin(px, 6, 27, big=False)
    draw_round_coin(px, 26, 27, big=False)
    return img


TIERS = [
    ("tier_1_single",   1, tier1),
    ("tier_2_pair",     2, tier2),
    ("tier_3_three",    3, tier3),
    ("tier_4_four",     4, tier4),
    ("tier_5_stack",    5, tier5),
    ("tier_6_tall",     6, tier6),
]


if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/items/coins/tiers"
    os.makedirs(out, exist_ok=True)
    # Clear old tier files
    for old in os.listdir(out):
        if old.startswith('tier_'):
            os.remove(os.path.join(out, old))
    for name, _, fn in TIERS:
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"done: {name}")
