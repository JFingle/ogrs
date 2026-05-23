#!/usr/bin/env python3
"""
FIRE element projectile — covers Fire Strike/Bolt/Blast/Wave + Iban Blast.
Flame-teardrop silhouette: tapered upward flame body, dark red base, hot
yellow-white core. Ember sparks flicker per frame.

Distinct from:
- MAGIC (ice diamond) — different shape, different palette
- ORB (wind/gold) — different shape, hot vs cool palette
- SKULL (cursed flames) — flame here is bigger and is the WHOLE sprite,
  not flames rising from a skull
"""
import os, math
from PIL import Image

W = H = 30
TRANS = (0, 0, 0, 0)

CORE_WHITE   = (255, 255, 255, 255)
CORE_HOT     = (255, 240, 180, 255)  # near-white center
CORE_YELLOW  = (255, 200,  80, 255)
CORE_ORANGE  = (255, 120,  40, 255)
CORE_RED     = (210,  50,  30, 255)
CORE_DEEP    = (130,  20,  20, 255)
EMBER_BRIGHT = (255, 220, 120, 255)
EMBER_DIM    = (180,  60,  20, 255)
SMOKE_LIGHT  = (110,  60,  50, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# Flame body — teardrop shape, tip up, wide at bottom.
# Define rows: each row is (left_x, right_x, [colors-by-band-from-outside-in])
# Center column = 14.
FLAME_BODY = {
    # row_y: list of (x, color) pairs
     6: [(14, CORE_HOT)],
     7: [(14, CORE_YELLOW), (13, CORE_ORANGE), (15, CORE_ORANGE)],
     8: [(14, CORE_HOT), (13, CORE_YELLOW), (15, CORE_YELLOW), (12, CORE_ORANGE), (16, CORE_ORANGE)],
     9: [(14, CORE_HOT), (13, CORE_HOT), (15, CORE_YELLOW), (12, CORE_YELLOW), (16, CORE_ORANGE), (11, CORE_ORANGE), (17, CORE_RED)],
    10: [(14, CORE_HOT), (13, CORE_HOT), (15, CORE_HOT), (12, CORE_YELLOW), (16, CORE_YELLOW), (11, CORE_ORANGE), (17, CORE_ORANGE), (10, CORE_RED), (18, CORE_RED)],
    11: [(14, CORE_HOT), (13, CORE_HOT), (15, CORE_HOT), (12, CORE_YELLOW), (16, CORE_YELLOW), (11, CORE_ORANGE), (17, CORE_ORANGE), (10, CORE_RED), (18, CORE_RED), (9, CORE_DEEP), (19, CORE_DEEP)],
    12: [(14, CORE_WHITE), (13, CORE_HOT), (15, CORE_HOT), (12, CORE_YELLOW), (16, CORE_YELLOW), (11, CORE_ORANGE), (17, CORE_ORANGE), (10, CORE_RED), (18, CORE_RED), (9, CORE_DEEP), (19, CORE_DEEP)],
    13: [(14, CORE_HOT), (13, CORE_HOT), (15, CORE_HOT), (12, CORE_YELLOW), (16, CORE_YELLOW), (11, CORE_ORANGE), (17, CORE_ORANGE), (10, CORE_RED), (18, CORE_RED), (9, CORE_DEEP), (19, CORE_DEEP), (8, SMOKE_LIGHT), (20, SMOKE_LIGHT)],
    14: [(14, CORE_HOT), (13, CORE_HOT), (15, CORE_HOT), (12, CORE_YELLOW), (16, CORE_YELLOW), (11, CORE_ORANGE), (17, CORE_ORANGE), (10, CORE_RED), (18, CORE_RED), (9, CORE_DEEP), (19, CORE_DEEP), (8, SMOKE_LIGHT), (20, SMOKE_LIGHT)],
    15: [(14, CORE_YELLOW), (13, CORE_YELLOW), (15, CORE_YELLOW), (12, CORE_ORANGE), (16, CORE_ORANGE), (11, CORE_RED), (17, CORE_RED), (10, CORE_DEEP), (18, CORE_DEEP), (9, SMOKE_LIGHT), (19, SMOKE_LIGHT)],
    16: [(14, CORE_ORANGE), (13, CORE_ORANGE), (15, CORE_ORANGE), (12, CORE_RED), (16, CORE_RED), (11, CORE_DEEP), (17, CORE_DEEP), (10, SMOKE_LIGHT), (18, SMOKE_LIGHT)],
    17: [(14, CORE_RED), (13, CORE_RED), (15, CORE_RED), (12, CORE_DEEP), (16, CORE_DEEP), (11, SMOKE_LIGHT), (17, SMOKE_LIGHT)],
    18: [(14, CORE_DEEP), (13, CORE_DEEP), (15, CORE_DEEP), (12, SMOKE_LIGHT), (16, SMOKE_LIGHT)],
}


def draw_flame_body(px, peak=False):
    for y, cells in FLAME_BODY.items():
        for x, color in cells:
            put(px, x, y, color)
    if peak:
        # peak — brighten the core 1 px wider in the middle
        put(px, 14, 10, CORE_WHITE)
        put(px, 14, 11, CORE_WHITE)


def draw_embers(px, frame):
    """Sparks flickering off the flame in various positions per frame."""
    sets = {
        0: [(11, 4, EMBER_BRIGHT), (17, 5, EMBER_DIM)],
        1: [(10, 3, EMBER_BRIGHT), (18, 4, EMBER_BRIGHT), (15, 2, EMBER_DIM)],
        2: [(13, 2, EMBER_BRIGHT), (16, 3, EMBER_BRIGHT), (10, 4, EMBER_BRIGHT),
            (19, 4, EMBER_DIM), (12, 1, EMBER_DIM)],
        3: [(11, 3, EMBER_DIM), (18, 5, EMBER_DIM), (15, 4, EMBER_BRIGHT)],
    }
    for x, y, c in sets.get(frame, []):
        put(px, x, y, c)


def draw_flame_lick(px, frame):
    """Per-frame variation on the flame tip — small tongue licking upward."""
    if frame == 1:
        put(px, 14, 5, CORE_YELLOW)
        put(px, 14, 4, CORE_ORANGE)
    elif frame == 2:
        put(px, 14, 5, CORE_HOT)
        put(px, 14, 4, CORE_YELLOW)
        put(px, 14, 3, CORE_ORANGE)
        put(px, 13, 4, CORE_ORANGE)
    elif frame == 3:
        put(px, 14, 5, CORE_YELLOW)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_flame_body(px, peak=(frame == 2))
    draw_flame_lick(px, frame)
    draw_embers(px, frame)
    return img


base = "/home/sparky/ogrs/art/projectiles/element_fire/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
print("done")
