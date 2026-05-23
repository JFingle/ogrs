#!/usr/bin/env python3
"""
Seed item tiers — 3 crops × 4 stack tiers = 12 sprites at 32×32.

Each crop has a distinct seed shape and palette so the player can
tell what they're carrying:
  POTATO  : small pale-yellow oval seeds (the 'eyes' of a potato)
  ONION   : small dark-brown round seeds
  TOMATO  : tiny flat amber-yellow seeds (drop-shape)

Tier thresholds (4 per crop):
  tier_1 :    1 seed   — single seed shown
  tier_2 :  2-9        — small handful (3-4 seeds)
  tier_3 : 10-49       — small pouch / dozen seeds
  tier_4 : 50+         — bursting pouch / heap

The 'pouch' variant is a small brown cloth bag with seeds peeking out
the top — RSC's classic stackable-seed visual.
"""
import os, math
from PIL import Image

W = H = 32
TRANS = (0, 0, 0, 0)

# Shared palette pieces
OUTLINE     = ( 38,  24,  10, 255)
SHADOW      = ( 70,  46,  18, 255)

# Pouch (brown cloth bag)
POUCH_OUT   = ( 50,  30,  10, 255)
POUCH_SHAD  = ( 92,  56,  20, 255)
POUCH_BASE  = (148, 100,  40, 255)
POUCH_HI    = (200, 150,  78, 255)
POUCH_TIE   = ( 70,  44,  18, 255)


# Per-crop palette
CROPS = {
    'potato': {
        'seed_dk':   (138, 108,  50, 255),
        'seed_base': (200, 174, 100, 255),
        'seed_hi':   (240, 220, 150, 255),
    },
    'onion': {
        'seed_dk':   ( 48,  20,  10, 255),
        'seed_base': ( 96,  48,  16, 255),
        'seed_hi':   (148,  90,  40, 255),
    },
    'tomato': {
        'seed_dk':   (140, 110,  20, 255),
        'seed_base': (210, 170,  60, 255),
        'seed_hi':   (255, 220, 110, 255),
    },
}


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def draw_seed(px, x, y, crop_pal, shape='oval'):
    """Draw a single small seed at (x, y). shape determines silhouette."""
    dk = crop_pal['seed_dk']
    base = crop_pal['seed_base']
    hi = crop_pal['seed_hi']
    if shape == 'oval':
        # 3×2 oval seed
        put(px, x - 1, y, dk); put(px, x, y, base); put(px, x + 1, y, base)
        put(px, x - 1, y + 1, dk); put(px, x, y + 1, dk); put(px, x + 1, y + 1, dk)
        put(px, x, y - 1, hi)
    elif shape == 'round':
        # 3×3 round seed
        put(px, x, y - 1, dk); put(px, x - 1, y, dk); put(px, x, y, hi); put(px, x + 1, y, base)
        put(px, x, y + 1, dk)
    elif shape == 'drop':
        # 2×3 small drop seed (teardrop)
        put(px, x, y - 1, dk)
        put(px, x - 1, y, dk); put(px, x, y, hi); put(px, x + 1, y, base)
        put(px, x, y + 1, dk)


def draw_pouch(px, size='med', overflow=False):
    """Draw a brown cloth pouch with drawstring."""
    if size == 'small':
        # 11×9 pouch
        body_x, body_y = 11, 18   # top-left of pouch body
        bw, bh = 10, 9
    else:
        # 15×11 pouch
        body_x, body_y = 9, 16
        bw, bh = 14, 12

    # Body — rounded shape
    for dy in range(bh):
        for dx in range(bw):
            x = body_x + dx
            y = body_y + dy
            # Round corners
            corner_skip = (dx in (0, bw - 1) and dy in (0, bh - 1))
            if corner_skip:
                continue
            # Outline edge
            if dx == 0 or dx == bw - 1 or dy == bh - 1:
                put(px, x, y, POUCH_OUT)
            elif dy == 0:
                put(px, x, y, POUCH_TIE)   # drawstring band
            elif dx <= 2:
                put(px, x, y, POUCH_SHAD)
            elif dx >= bw - 3:
                put(px, x, y, POUCH_BASE)
            else:
                # Body interior — slight highlight upper-left
                if dy <= bh // 2 and dx <= bw // 2:
                    put(px, x, y, POUCH_HI)
                else:
                    put(px, x, y, POUCH_BASE)

    # Drawstring tie at top
    tie_x = body_x + bw // 2
    tie_y = body_y - 1
    put(px, tie_x, tie_y, POUCH_TIE)
    put(px, tie_x - 1, tie_y, POUCH_TIE)
    put(px, tie_x + 1, tie_y, POUCH_TIE)
    put(px, tie_x, tie_y - 1, POUCH_OUT)
    # Two ear loops sticking up
    put(px, tie_x - 2, tie_y - 1, POUCH_OUT)
    put(px, tie_x + 2, tie_y - 1, POUCH_OUT)


def tier1(crop_pal, shape):
    """Single seed centered."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Bigger single seed — show detail
    cx, cy = 16, 16
    # Larger version: 5×4
    base = crop_pal['seed_base']
    dk = crop_pal['seed_dk']
    hi = crop_pal['seed_hi']
    if shape in ('oval', 'drop'):
        cells = {
            (-2, -1): OUTLINE, (-1, -1): hi, (0, -1): base, (1, -1): base, (2, -1): OUTLINE,
            (-2, 0): OUTLINE, (-1, 0): hi, (0, 0): base, (1, 0): base, (2, 0): OUTLINE,
            (-2, 1): OUTLINE, (-1, 1): base, (0, 1): base, (1, 1): dk, (2, 1): OUTLINE,
            (-1, 2): OUTLINE, (0, 2): OUTLINE, (1, 2): OUTLINE,
            (-1, -2): OUTLINE, (0, -2): OUTLINE, (1, -2): OUTLINE,
        }
    else:  # round
        cells = {
            (-1, -2): OUTLINE, (0, -2): OUTLINE, (1, -2): OUTLINE,
            (-2, -1): OUTLINE, (-1, -1): hi, (0, -1): hi, (1, -1): base, (2, -1): OUTLINE,
            (-2, 0): OUTLINE, (-1, 0): hi, (0, 0): base, (1, 0): base, (2, 0): OUTLINE,
            (-2, 1): OUTLINE, (-1, 1): base, (0, 1): dk, (1, 1): dk, (2, 1): OUTLINE,
            (-1, 2): OUTLINE, (0, 2): OUTLINE, (1, 2): OUTLINE,
        }
    for (dx, dy), c in cells.items():
        put(px, cx + dx, cy + dy, c)
    return img


def tier2(crop_pal, shape):
    """3-4 small seeds clustered."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    positions = [(13, 14), (19, 14), (16, 19), (14, 22)]
    for x, y in positions:
        draw_seed(px, x, y, crop_pal, shape=shape)
    return img


def tier3(crop_pal, shape):
    """Pouch with a handful of seeds visible at top."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_pouch(px, size='small')
    # 3 seeds peeking out the top
    for x, y in [(13, 19), (16, 18), (19, 19)]:
        draw_seed(px, x, y, crop_pal, shape=shape)
    return img


def tier4(crop_pal, shape):
    """Bigger pouch overflowing with seeds spilling out."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_pouch(px, size='med')
    # Many seeds — some inside the open top, some spilling out
    positions = [
        (12, 18), (15, 17), (18, 17), (21, 18),    # at the lip of the pouch
        (10, 22), (24, 22),                         # spilled to the sides
        (16, 14), (14, 12), (18, 12),               # above (pouring out)
        (8, 26), (26, 26),                          # spilled below
    ]
    for x, y in positions:
        draw_seed(px, x, y, crop_pal, shape=shape)
    return img


SHAPES = {'potato': 'oval', 'onion': 'round', 'tomato': 'drop'}

if __name__ == "__main__":
    for crop in ('potato', 'onion', 'tomato'):
        out = f"/home/sparky/ogrs/art/items/seeds/{crop}/tiers"
        os.makedirs(out, exist_ok=True)
        pal = CROPS[crop]
        shape = SHAPES[crop]
        for tier_num, tier_fn in [(1, tier1), (2, tier2), (3, tier3), (4, tier4)]:
            img = tier_fn(pal, shape)
            img.save(f"{out}/tier_{tier_num}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/tier_{tier_num}_x8.png")
        print(f"done: {crop}")
