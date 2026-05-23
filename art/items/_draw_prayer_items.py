#!/usr/bin/env python3
"""
OGRS Prayer / Sacred items batch — Yahwist-flavored ritual implements.

Excludes anything already drawn:
  - Sacred crops (sacred/) — blessed_grapes, blessed_wheat, faith_mustard_seed,
    manna, olive_tree_fruit, pomegranate, sacred_fig — already done
  - Sacred flowers (flowers_sacred/) — cedar_sprig, hyssop, lily_of_valley — already done

This batch covers ritual implements and prayer-XP items only.

Phases:
  1. Bones (7)        — bones for Prayer XP
  2. Holy implements (7) — vials, censer, horn, symbol, incense
  3. Communion (4)    — bread + wine + presence + candle
  4. Priest garments (4) — robes, mitre, stole
  5. Books & scrolls (3) — scripture, sealed scroll, open prayer
  6. Special (2)      — cherubim seal, demonic ashes

Total: 27 sprites at 32x32 native, 256x256 x8 preview.
"""
import os
from PIL import Image, ImageDraw

OUT = "/home/sparky/ogrs/art/items/prayer"
os.makedirs(OUT, exist_ok=True)

SIZE = 32
SCALE = 8


def new_canvas():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def save(img, name):
    img.save(f"{OUT}/{name}.png")
    img.resize((SIZE * SCALE, SIZE * SCALE), Image.NEAREST).save(f"{OUT}/{name}_x8.png")


def px(img, x, y, color):
    if 0 <= x < SIZE and 0 <= y < SIZE:
        img.putpixel((x, y), color)


def fill_rect(img, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(SIZE, y1 + 1)):
        for x in range(max(0, x0), min(SIZE, x1 + 1)):
            img.putpixel((x, y), color)


def line(img, x0, y0, x1, y1, color):
    dx = abs(x1 - x0); dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        px(img, x0, y0, color)
        if x0 == x1 and y0 == y1: break
        e2 = err * 2
        if e2 > -dy:
            err -= dy; x0 += sx
        if e2 < dx:
            err += dx; y0 += sy


def ellipse_fill(img, cx, cy, rx, ry, color):
    for y in range(-ry, ry + 1):
        for x in range(-rx, rx + 1):
            if (x * x) / (rx * rx) + (y * y) / (ry * ry) <= 1.0:
                px(img, cx + x, cy + y, color)


# ============================================================
# PHASE 1 — BONES (7)
# ============================================================

BONE_HI = (240, 232, 210, 255)
BONE_MID = (216, 204, 168, 255)
BONE_LO = (168, 152, 112, 255)
BONE_SHADOW = (108, 92, 68, 255)


def draw_bone_shape(img, cx, cy, length, thickness, knob_radius, hi, mid, lo, shadow):
    """Generic femur-style bone with two knobs on each end."""
    half = length // 2
    # Shaft
    for y in range(cy - thickness // 2, cy + thickness // 2 + 1):
        for x in range(cx - half + knob_radius, cx + half - knob_radius + 1):
            t = abs(y - cy)
            if t < thickness // 2:
                px(img, x, y, hi if y == cy - thickness // 2 + 1 else mid)
            else:
                px(img, x, y, lo)
    # Left knobs (two bumps)
    ellipse_fill(img, cx - half + knob_radius, cy - thickness // 2 - 1, knob_radius, knob_radius, lo)
    ellipse_fill(img, cx - half + knob_radius, cy - thickness // 2 - 1, knob_radius - 1, knob_radius - 1, mid)
    ellipse_fill(img, cx - half + knob_radius, cy + thickness // 2 + 1, knob_radius, knob_radius, lo)
    ellipse_fill(img, cx - half + knob_radius, cy + thickness // 2 + 1, knob_radius - 1, knob_radius - 1, mid)
    # Right knobs
    ellipse_fill(img, cx + half - knob_radius, cy - thickness // 2 - 1, knob_radius, knob_radius, lo)
    ellipse_fill(img, cx + half - knob_radius, cy - thickness // 2 - 1, knob_radius - 1, knob_radius - 1, mid)
    ellipse_fill(img, cx + half - knob_radius, cy + thickness // 2 + 1, knob_radius, knob_radius, lo)
    ellipse_fill(img, cx + half - knob_radius, cy + thickness // 2 + 1, knob_radius - 1, knob_radius - 1, mid)
    # Highlights on top of knobs
    px(img, cx - half + knob_radius, cy - thickness // 2 - knob_radius, hi)
    px(img, cx + half - knob_radius, cy - thickness // 2 - knob_radius, hi)


def draw_bones():
    # Regular bones — single femur, modest size
    img = new_canvas()
    draw_bone_shape(img, 16, 17, 22, 4, 3, BONE_HI, BONE_MID, BONE_LO, BONE_SHADOW)
    # Subtle shadow streak
    fill_rect(img, 8, 22, 24, 22, (60, 50, 30, 90))
    save(img, "bones")

    # Big bones — thicker shaft, larger knobs
    img = new_canvas()
    draw_bone_shape(img, 16, 17, 26, 6, 4, BONE_HI, BONE_MID, BONE_LO, BONE_SHADOW)
    fill_rect(img, 5, 24, 27, 24, (60, 50, 30, 90))
    save(img, "big_bones")

    # Wolf bones — longer, slimmer
    img = new_canvas()
    draw_bone_shape(img, 16, 17, 28, 3, 3, BONE_HI, BONE_MID, BONE_LO, BONE_SHADOW)
    # Slight bend marker
    px(img, 16, 18, BONE_LO)
    save(img, "wolf_bones")

    # Babydragon bones — thicker, with greenish tinge
    BD_HI = (220, 230, 205, 255)
    BD_MID = (185, 200, 165, 255)
    BD_LO = (140, 160, 115, 255)
    img = new_canvas()
    draw_bone_shape(img, 16, 17, 24, 5, 4, BD_HI, BD_MID, BD_LO, BONE_SHADOW)
    save(img, "babydragon_bones")

    # Dragon bones — much larger, prominent ridges
    D_HI = (235, 230, 200, 255)
    D_MID = (195, 185, 150, 255)
    D_LO = (130, 115, 80, 255)
    img = new_canvas()
    draw_bone_shape(img, 16, 17, 28, 7, 5, D_HI, D_MID, D_LO, BONE_SHADOW)
    # Ridge details on shaft
    for x in range(9, 24, 3):
        px(img, x, 15, D_LO)
        px(img, x, 19, D_LO)
    save(img, "dragon_bones")

    # Burnt bones — charred dark
    BURN_HI = (90, 70, 50, 255)
    BURN_MID = (60, 45, 30, 255)
    BURN_LO = (30, 20, 12, 255)
    img = new_canvas()
    draw_bone_shape(img, 16, 17, 22, 4, 3, BURN_HI, BURN_MID, BURN_LO, BONE_SHADOW)
    # Small flame remnants
    px(img, 14, 12, (220, 140, 40, 200))
    px(img, 18, 11, (200, 100, 30, 180))
    save(img, "burnt_bones")

    # Ashes — pile of gray powder
    img = new_canvas()
    ASH_LO = (95, 88, 80, 255)
    ASH_MID = (140, 132, 122, 255)
    ASH_HI = (180, 172, 160, 255)
    # Mound shape
    for y in range(22, 28):
        width = 28 - y
        for x in range(16 - width, 16 + width):
            d = abs(x - 16)
            if d < width - 4:
                px(img, x, y, ASH_HI)
            elif d < width - 2:
                px(img, x, y, ASH_MID)
            else:
                px(img, x, y, ASH_LO)
    # Stray flakes
    px(img, 9, 24, ASH_MID)
    px(img, 24, 25, ASH_MID)
    px(img, 11, 27, ASH_LO)
    px(img, 22, 27, ASH_LO)
    save(img, "ashes")


# ============================================================
# PHASE 2 — HOLY IMPLEMENTS (7)
# ============================================================

def draw_holy_water_vial():
    img = new_canvas()
    # Glass vial
    GLASS_HI = (220, 235, 250, 255)
    GLASS_MID = (180, 200, 230, 255)
    GLASS_LO = (130, 155, 195, 255)
    # Body (rounded flask)
    fill_rect(img, 11, 16, 20, 26, GLASS_MID)
    fill_rect(img, 12, 14, 19, 16, GLASS_MID)
    # Highlight stripe
    fill_rect(img, 12, 17, 13, 25, GLASS_HI)
    # Edge shadow
    fill_rect(img, 20, 17, 20, 25, GLASS_LO)
    # Bottom
    fill_rect(img, 12, 26, 19, 27, GLASS_LO)
    # Neck
    fill_rect(img, 14, 10, 17, 14, GLASS_MID)
    px(img, 14, 11, GLASS_HI)
    # Cork
    CORK = (140, 100, 60, 255)
    fill_rect(img, 13, 7, 18, 10, CORK)
    fill_rect(img, 13, 7, 13, 9, (175, 130, 80, 255))
    # Holy water (luminous blue-white)
    WATER_HI = (220, 240, 255, 255)
    WATER_MID = (170, 210, 240, 255)
    fill_rect(img, 13, 18, 18, 25, WATER_MID)
    fill_rect(img, 14, 18, 17, 19, WATER_HI)
    # Cross etched on front
    CROSS = (240, 220, 130, 255)
    fill_rect(img, 15, 20, 16, 23, CROSS)
    fill_rect(img, 14, 21, 17, 21, CROSS)
    # Faint glow halo
    for x, y in [(10, 12), (21, 12), (10, 28), (21, 28)]:
        img.putpixel((x, y), (240, 240, 200, 70))
    save(img, "holy_water_vial")


def draw_anointing_oil_flask():
    img = new_canvas()
    # Curved alabaster flask
    AL_HI = (245, 240, 220, 255)
    AL_MID = (215, 205, 175, 255)
    AL_LO = (170, 155, 120, 255)
    # Bulb body
    ellipse_fill(img, 16, 20, 6, 7, AL_MID)
    ellipse_fill(img, 16, 20, 5, 6, AL_HI)
    # Bottom shadow
    ellipse_fill(img, 16, 22, 5, 4, AL_LO)
    ellipse_fill(img, 16, 21, 4, 3, AL_MID)
    # Neck
    fill_rect(img, 14, 11, 17, 14, AL_MID)
    px(img, 14, 11, AL_HI); px(img, 14, 12, AL_HI)
    px(img, 17, 13, AL_LO)
    # Stopper
    STOP = (120, 80, 40, 255)
    fill_rect(img, 13, 8, 18, 11, STOP)
    fill_rect(img, 13, 8, 18, 8, (160, 110, 60, 255))
    # Gold band
    fill_rect(img, 14, 13, 17, 14, (220, 175, 60, 255))
    px(img, 14, 13, (250, 220, 100, 255))
    # Oil dripping shine on belly
    px(img, 13, 17, (255, 250, 240, 255))
    px(img, 14, 16, (255, 250, 240, 200))
    save(img, "anointing_oil_flask")


def draw_holy_symbol():
    """Yahwist cross/cruciform on a neck cord."""
    img = new_canvas()
    # Cord (above)
    CORD = (110, 80, 50, 255)
    for x in range(7, 26):
        # arc shape
        dy = -abs(x - 16) // 4
        px(img, x, 8 + dy, CORD)
        px(img, x, 9 + dy, CORD)
    # Pendant ring at top of cross
    RING = (220, 175, 60, 255)
    RING_HI = (250, 220, 100, 255)
    ellipse_fill(img, 16, 11, 2, 2, RING)
    px(img, 15, 10, RING_HI)
    # Inner hole
    px(img, 16, 11, (60, 40, 20, 255))
    # Cross body — gold
    GOLD_HI = (250, 220, 100, 255)
    GOLD_MID = (220, 175, 60, 255)
    GOLD_LO = (160, 115, 30, 255)
    # Vertical bar
    fill_rect(img, 14, 13, 17, 26, GOLD_MID)
    fill_rect(img, 14, 13, 14, 25, GOLD_HI)
    fill_rect(img, 17, 14, 17, 26, GOLD_LO)
    # Horizontal bar
    fill_rect(img, 10, 17, 21, 20, GOLD_MID)
    fill_rect(img, 10, 17, 21, 17, GOLD_HI)
    fill_rect(img, 10, 20, 21, 20, GOLD_LO)
    # Center jewel
    JEWEL = (200, 60, 60, 255)
    JEWEL_HI = (255, 130, 130, 255)
    fill_rect(img, 15, 18, 16, 19, JEWEL)
    px(img, 15, 18, JEWEL_HI)
    # Glow
    for x, y in [(13, 16), (18, 16), (13, 21), (18, 21)]:
        if img.getpixel((x, y))[3] == 0:
            img.putpixel((x, y), (255, 240, 180, 60))
    save(img, "holy_symbol")


def draw_censer_lit():
    """Hanging incense burner with smoke."""
    img = new_canvas()
    BRASS_HI = (255, 220, 130, 255)
    BRASS_MID = (210, 165, 70, 255)
    BRASS_LO = (140, 100, 40, 255)
    # Chain (3 links)
    CHAIN = (180, 140, 60, 255)
    for y in [4, 6, 8]:
        px(img, 16, y, CHAIN)
        px(img, 15, y, BRASS_LO)
        px(img, 17, y, BRASS_LO)
    # Top cap
    fill_rect(img, 12, 10, 19, 11, BRASS_MID)
    px(img, 12, 10, BRASS_HI); px(img, 19, 10, BRASS_LO)
    # Vent holes in cap
    px(img, 14, 11, (50, 30, 10, 255))
    px(img, 17, 11, (50, 30, 10, 255))
    # Bowl
    for y in range(12, 22):
        if y < 17:
            width = 5 + (y - 12)
        else:
            width = 9 - (y - 17)
        for x in range(16 - width, 16 + width + 1):
            d = x - (16 - width)
            if d == 0:
                px(img, x, y, BRASS_LO)
            elif d == 1:
                px(img, x, y, BRASS_MID)
            elif x == 16 - width + 2:
                px(img, x, y, BRASS_HI)
            elif x == 16 + width:
                px(img, x, y, BRASS_LO)
            else:
                px(img, x, y, BRASS_MID)
    # Glowing coals inside (visible through cap holes — show as warm dots near top)
    px(img, 14, 12, (255, 120, 30, 255))
    px(img, 17, 12, (255, 100, 20, 255))
    # Smoke rising
    SMOKE = (220, 220, 220, 180)
    SMOKE_F = (220, 220, 220, 100)
    for i, (x, y) in enumerate([(14, 7), (15, 5), (13, 3), (18, 6), (17, 4), (19, 2)]):
        img.putpixel((x, y), SMOKE if i % 2 == 0 else SMOKE_F)
    save(img, "censer_lit")


def draw_censer_unlit():
    """Same shape, no smoke, dim coals."""
    img = new_canvas()
    BRASS_HI = (210, 175, 90, 255)
    BRASS_MID = (170, 130, 55, 255)
    BRASS_LO = (110, 80, 30, 255)
    CHAIN = (140, 105, 45, 255)
    for y in [4, 6, 8]:
        px(img, 16, y, CHAIN)
        px(img, 15, y, BRASS_LO)
        px(img, 17, y, BRASS_LO)
    fill_rect(img, 12, 10, 19, 11, BRASS_MID)
    px(img, 12, 10, BRASS_HI); px(img, 19, 10, BRASS_LO)
    px(img, 14, 11, (40, 25, 10, 255))
    px(img, 17, 11, (40, 25, 10, 255))
    for y in range(12, 22):
        if y < 17:
            width = 5 + (y - 12)
        else:
            width = 9 - (y - 17)
        for x in range(16 - width, 16 + width + 1):
            d = x - (16 - width)
            if d == 0:
                px(img, x, y, BRASS_LO)
            elif x == 16 - width + 2:
                px(img, x, y, BRASS_HI)
            elif x == 16 + width:
                px(img, x, y, BRASS_LO)
            else:
                px(img, x, y, BRASS_MID)
    save(img, "censer_unlit")


def draw_incense_stick():
    img = new_canvas()
    # Wooden stick
    WOOD = (110, 75, 45, 255)
    WOOD_HI = (150, 110, 70, 255)
    for y in range(8, 28):
        px(img, 16, y, WOOD)
        px(img, 17, y, WOOD)
    px(img, 16, 8, WOOD_HI); px(img, 16, 12, WOOD_HI)
    # Incense coating (brown rod near top half)
    COAT = (90, 50, 25, 255)
    fill_rect(img, 15, 10, 18, 20, COAT)
    fill_rect(img, 15, 10, 15, 20, (60, 35, 18, 255))
    fill_rect(img, 18, 10, 18, 20, (130, 80, 40, 255))
    # Ember tip
    px(img, 16, 9, (255, 120, 40, 255))
    px(img, 17, 9, (255, 100, 30, 255))
    px(img, 16, 10, (255, 200, 80, 255))
    # Smoke wisp
    px(img, 16, 6, (220, 220, 220, 180))
    px(img, 15, 4, (220, 220, 220, 120))
    px(img, 17, 2, (220, 220, 220, 80))
    save(img, "incense_stick")


def draw_anointing_horn():
    """Ram's horn for sacred anointing."""
    img = new_canvas()
    HORN_HI = (180, 140, 95, 255)
    HORN_MID = (140, 100, 60, 255)
    HORN_LO = (95, 65, 35, 255)
    HORN_DARK = (60, 40, 20, 255)
    # Curved horn — wide at right (opening), narrow at left (tip)
    # Generated as a curving shape
    horn_pts = [
        (6, 18, 1), (7, 17, 1), (8, 16, 2), (9, 15, 2), (10, 14, 2),
        (11, 13, 3), (12, 13, 3), (13, 13, 3), (14, 14, 4), (15, 14, 4),
        (16, 15, 4), (17, 16, 5), (18, 17, 5), (19, 18, 6), (20, 19, 6),
        (21, 20, 7), (22, 21, 7), (23, 22, 6), (24, 22, 5),
    ]
    for px_, py_, thick in horn_pts:
        for t in range(-thick, thick + 1):
            yy = py_ + t
            if 0 <= yy < SIZE:
                color = HORN_MID
                if t == -thick:
                    color = HORN_HI
                elif t == thick:
                    color = HORN_DARK
                elif t == -thick + 1:
                    color = HORN_HI
                elif t == thick - 1:
                    color = HORN_LO
                px(img, px_, yy, color)
    # Opening (right end) — show inner dark
    fill_rect(img, 23, 17, 25, 21, HORN_DARK)
    fill_rect(img, 24, 18, 25, 20, (30, 20, 10, 255))
    # Gold band around opening
    GOLD = (220, 175, 60, 255)
    GOLD_HI = (250, 220, 100, 255)
    for y in range(16, 23):
        px(img, 22, y, GOLD)
        px(img, 22, y, GOLD_HI if y == 17 else GOLD)
    # Oil shimmer at opening
    px(img, 24, 19, (250, 230, 130, 255))
    save(img, "anointing_horn")


# ============================================================
# PHASE 3 — COMMUNION (4)
# ============================================================

def draw_unleavened_bread():
    img = new_canvas()
    # Flat round bread
    BREAD_HI = (245, 220, 165, 255)
    BREAD_MID = (215, 180, 120, 255)
    BREAD_LO = (170, 130, 75, 255)
    # Disc
    for y in range(13, 22):
        dy = y - 17
        width = max(0, 9 - abs(dy))
        for x in range(16 - width, 16 + width + 1):
            dx = x - 16
            d2 = dx * dx + dy * dy * 2
            if d2 < 70:
                px(img, x, y, BREAD_HI)
            elif d2 < 90:
                px(img, x, y, BREAD_MID)
            else:
                px(img, x, y, BREAD_LO)
    # Crusty edge dots
    for x, y in [(8, 17), (24, 17), (10, 13), (22, 13), (10, 21), (22, 21), (16, 12), (16, 22)]:
        if img.getpixel((x, y))[3] > 0:
            img.putpixel((x, y), BREAD_LO)
    # Score lines (cross marks — unleavened tradition)
    for x in range(13, 20):
        if img.getpixel((x, 17))[3] > 0:
            img.putpixel((x, 17), BREAD_LO)
    for y in range(14, 21):
        if img.getpixel((16, y))[3] > 0:
            img.putpixel((16, y), BREAD_LO)
    save(img, "unleavened_bread")


def draw_communion_cup():
    """Silver goblet with wine."""
    img = new_canvas()
    SILVER_HI = (235, 235, 240, 255)
    SILVER_MID = (185, 185, 195, 255)
    SILVER_LO = (130, 130, 145, 255)
    SILVER_DARK = (75, 75, 90, 255)
    # Bowl of cup
    for y in range(8, 16):
        if y < 12:
            width = 6
        else:
            width = 10 - (y - 12)
        for x in range(16 - width, 16 + width + 1):
            d = x - (16 - width)
            if d == 0 or x == 16 + width:
                px(img, x, y, SILVER_LO)
            elif d == 1:
                px(img, x, y, SILVER_HI)
            else:
                px(img, x, y, SILVER_MID)
    # Wine surface
    WINE = (130, 25, 35, 255)
    WINE_HI = (175, 50, 60, 255)
    fill_rect(img, 11, 9, 21, 10, WINE)
    fill_rect(img, 12, 9, 19, 9, WINE_HI)
    # Stem
    fill_rect(img, 15, 16, 17, 23, SILVER_MID)
    fill_rect(img, 15, 16, 15, 23, SILVER_HI)
    fill_rect(img, 17, 16, 17, 23, SILVER_LO)
    # Knot in stem
    fill_rect(img, 14, 19, 18, 20, SILVER_MID)
    px(img, 14, 19, SILVER_HI); px(img, 18, 20, SILVER_DARK)
    # Foot/base
    fill_rect(img, 11, 24, 21, 25, SILVER_MID)
    fill_rect(img, 12, 23, 20, 23, SILVER_HI)
    fill_rect(img, 11, 25, 21, 25, SILVER_LO)
    save(img, "communion_cup")


def draw_bread_of_presence():
    """Stack of 12 small loaves on a golden tray."""
    img = new_canvas()
    GOLD_HI = (250, 220, 100, 255)
    GOLD_MID = (220, 175, 60, 255)
    GOLD_LO = (160, 115, 30, 255)
    BREAD_HI = (245, 220, 165, 255)
    BREAD_MID = (215, 180, 120, 255)
    BREAD_LO = (170, 130, 75, 255)
    # Tray
    fill_rect(img, 6, 23, 26, 26, GOLD_MID)
    fill_rect(img, 6, 23, 26, 23, GOLD_HI)
    fill_rect(img, 6, 26, 26, 26, GOLD_LO)
    # 6 loaves bottom row, 4 middle, 2 top — pyramid
    def loaf(cx, cy):
        fill_rect(img, cx - 1, cy - 1, cx + 1, cy, BREAD_MID)
        px(img, cx - 1, cy - 1, BREAD_HI)
        px(img, cx + 1, cy, BREAD_LO)
    # Bottom row of 6
    for i, cx in enumerate([8, 11, 14, 17, 20, 23]):
        loaf(cx, 22)
    # Middle row of 4
    for cx in [10, 13, 17, 20]:
        loaf(cx, 19)
    # Top row of 2
    loaf(13, 16); loaf(18, 16)
    # Incense bowls on either end (decoration)
    INC_HI = (255, 220, 120, 255)
    INC_MID = (200, 150, 50, 255)
    fill_rect(img, 5, 20, 7, 22, INC_MID)
    px(img, 5, 20, INC_HI)
    fill_rect(img, 24, 20, 26, 22, INC_MID)
    px(img, 24, 20, INC_HI)
    # Smoke wisps
    px(img, 6, 18, (220, 220, 220, 180))
    px(img, 25, 18, (220, 220, 220, 180))
    save(img, "bread_of_presence")


def draw_blessed_candle():
    img = new_canvas()
    # Tall white candle
    WAX_HI = (250, 248, 230, 255)
    WAX_MID = (220, 215, 195, 255)
    WAX_LO = (175, 170, 145, 255)
    fill_rect(img, 13, 10, 18, 27, WAX_MID)
    fill_rect(img, 13, 10, 13, 27, WAX_HI)
    fill_rect(img, 18, 10, 18, 27, WAX_LO)
    # Wax drip
    px(img, 13, 15, WAX_HI); px(img, 12, 16, WAX_MID); px(img, 12, 17, WAX_MID); px(img, 12, 18, WAX_LO)
    # Wick
    fill_rect(img, 15, 7, 16, 9, (40, 30, 20, 255))
    # Flame
    FLAME_TIP = (255, 250, 200, 255)
    FLAME_HI = (255, 220, 100, 255)
    FLAME_MID = (255, 160, 40, 255)
    FLAME_LO = (220, 90, 20, 255)
    fill_rect(img, 14, 4, 17, 6, FLAME_MID)
    px(img, 15, 3, FLAME_HI); px(img, 16, 3, FLAME_HI)
    px(img, 15, 5, FLAME_HI); px(img, 16, 4, FLAME_TIP)
    px(img, 14, 6, FLAME_LO); px(img, 17, 6, FLAME_LO)
    # Halo
    for x, y in [(11, 4), (20, 4), (13, 2), (18, 2)]:
        if img.getpixel((x, y))[3] == 0:
            img.putpixel((x, y), (255, 240, 180, 60))
    # Gold band
    fill_rect(img, 13, 24, 18, 25, (220, 175, 60, 255))
    fill_rect(img, 13, 24, 13, 24, (250, 220, 100, 255))
    save(img, "blessed_candle")


# ============================================================
# PHASE 4 — PRIEST GARMENTS (4)
# ============================================================

def draw_priest_robe_top():
    img = new_canvas()
    ROBE_HI = (250, 245, 230, 255)
    ROBE_MID = (220, 215, 200, 255)
    ROBE_LO = (170, 165, 145, 255)
    GOLD_HI = (250, 220, 100, 255)
    GOLD_MID = (220, 175, 60, 255)
    # Collar / neck
    fill_rect(img, 14, 7, 17, 9, ROBE_MID)
    px(img, 14, 7, ROBE_HI); px(img, 17, 7, ROBE_LO)
    # Shoulders
    fill_rect(img, 11, 10, 20, 12, ROBE_MID)
    px(img, 11, 10, ROBE_HI); px(img, 20, 10, ROBE_LO)
    # Torso
    fill_rect(img, 10, 13, 21, 24, ROBE_MID)
    fill_rect(img, 10, 13, 10, 24, ROBE_HI)
    fill_rect(img, 21, 13, 21, 24, ROBE_LO)
    # Sleeves
    fill_rect(img, 7, 13, 9, 20, ROBE_MID)
    fill_rect(img, 22, 13, 24, 20, ROBE_MID)
    fill_rect(img, 7, 13, 7, 20, ROBE_HI)
    fill_rect(img, 24, 13, 24, 20, ROBE_LO)
    # Sleeve hem
    fill_rect(img, 7, 21, 9, 22, GOLD_MID)
    fill_rect(img, 22, 21, 24, 22, GOLD_MID)
    px(img, 7, 21, GOLD_HI); px(img, 24, 22, (160, 115, 30, 255))
    # Vertical gold stripe (priestly center)
    fill_rect(img, 15, 13, 16, 23, GOLD_MID)
    px(img, 15, 13, GOLD_HI)
    # Cross emblem at chest
    fill_rect(img, 15, 16, 16, 19, (180, 30, 30, 255))
    fill_rect(img, 14, 17, 17, 17, (180, 30, 30, 255))
    px(img, 15, 16, (220, 60, 60, 255))
    # Bottom hem
    fill_rect(img, 10, 24, 21, 25, GOLD_MID)
    save(img, "priest_robe_top")


def draw_priest_robe_bottom():
    img = new_canvas()
    ROBE_HI = (250, 245, 230, 255)
    ROBE_MID = (220, 215, 200, 255)
    ROBE_LO = (170, 165, 145, 255)
    GOLD_MID = (220, 175, 60, 255)
    # Waistband
    fill_rect(img, 10, 7, 21, 9, GOLD_MID)
    px(img, 10, 7, (250, 220, 100, 255))
    # Body of robe (flares)
    for y in range(10, 27):
        flare = (y - 10) // 4
        for x in range(9 - flare, 22 + flare + 1):
            d = x - (9 - flare)
            total = (22 + flare) - (9 - flare)
            if d == 0:
                px(img, x, y, ROBE_HI)
            elif d == total:
                px(img, x, y, ROBE_LO)
            else:
                px(img, x, y, ROBE_MID)
    # Vertical fold lines
    for y in range(10, 26):
        if img.getpixel((13, y))[3] > 0:
            img.putpixel((13, y), ROBE_LO)
        if img.getpixel((18, y))[3] > 0:
            img.putpixel((18, y), ROBE_LO)
    # Gold hem
    for x in range(7, 25):
        if img.getpixel((x, 26))[3] > 0:
            img.putpixel((x, 26), GOLD_MID)
        if img.getpixel((x, 27))[3] > 0:
            img.putpixel((x, 27), (160, 115, 30, 255))
    save(img, "priest_robe_bottom")


def draw_mitre():
    """Tall priestly hat."""
    img = new_canvas()
    HAT_HI = (250, 245, 230, 255)
    HAT_MID = (220, 215, 200, 255)
    HAT_LO = (170, 165, 145, 255)
    GOLD_HI = (250, 220, 100, 255)
    GOLD_MID = (220, 175, 60, 255)
    RED = (180, 30, 30, 255)
    RED_HI = (220, 70, 70, 255)
    # Mitre tall shape (pointed top, splits in two peaks classically)
    # Base brim
    fill_rect(img, 8, 22, 23, 24, HAT_MID)
    fill_rect(img, 8, 22, 23, 22, HAT_HI)
    fill_rect(img, 8, 24, 23, 24, HAT_LO)
    # Main shape — tall taper
    for y in range(8, 22):
        width = 4 + (y - 8) // 2
        for x in range(16 - width, 16 + width + 1):
            d = x - (16 - width)
            if d == 0:
                px(img, x, y, HAT_HI)
            elif x == 16 + width:
                px(img, x, y, HAT_LO)
            else:
                px(img, x, y, HAT_MID)
    # Top split (V notch)
    fill_rect(img, 15, 8, 17, 11, (0, 0, 0, 0))
    px(img, 16, 11, HAT_LO)
    # Gold band at brim
    fill_rect(img, 8, 21, 23, 21, GOLD_MID)
    # Vertical red stripe
    fill_rect(img, 15, 12, 16, 21, RED)
    px(img, 15, 12, RED_HI)
    # Cross on front
    fill_rect(img, 15, 15, 16, 18, GOLD_MID)
    fill_rect(img, 14, 16, 17, 16, GOLD_MID)
    px(img, 15, 15, GOLD_HI)
    save(img, "mitre")


def draw_stole():
    """Long fabric strip worn over shoulders — embroidered."""
    img = new_canvas()
    STOLE_HI = (245, 230, 180, 255)
    STOLE_MID = (210, 190, 130, 255)
    STOLE_LO = (155, 135, 85, 255)
    GOLD = (220, 175, 60, 255)
    RED = (180, 30, 30, 255)
    # Horseshoe shape — over shoulders, two strips hanging down
    # Top arc (across shoulders)
    fill_rect(img, 10, 8, 21, 10, STOLE_MID)
    fill_rect(img, 10, 8, 21, 8, STOLE_HI)
    fill_rect(img, 10, 10, 21, 10, STOLE_LO)
    # Left strip down
    fill_rect(img, 10, 11, 13, 26, STOLE_MID)
    fill_rect(img, 10, 11, 10, 26, STOLE_HI)
    fill_rect(img, 13, 11, 13, 26, STOLE_LO)
    # Right strip down
    fill_rect(img, 18, 11, 21, 26, STOLE_MID)
    fill_rect(img, 18, 11, 18, 26, STOLE_HI)
    fill_rect(img, 21, 11, 21, 26, STOLE_LO)
    # Embroidered crosses on each strip
    for cy in [15, 22]:
        # Left
        fill_rect(img, 11, cy, 12, cy + 2, RED)
        fill_rect(img, 10, cy + 1, 13, cy + 1, RED)
        # Right
        fill_rect(img, 19, cy, 20, cy + 2, RED)
        fill_rect(img, 18, cy + 1, 21, cy + 1, RED)
    # Gold trim along edges
    for y in range(8, 27):
        if img.getpixel((10, y))[3] > 0 and y not in (15, 16, 17, 22, 23, 24):
            pass  # leave highlight
    # Tassel at bottom of each strip
    for cx in [11, 12, 19, 20]:
        px(img, cx, 27, GOLD)
    save(img, "stole")


# ============================================================
# PHASE 5 — BOOKS & SCROLLS (3)
# ============================================================

def draw_yahwist_scripture():
    img = new_canvas()
    LEATHER_HI = (130, 70, 40, 255)
    LEATHER_MID = (95, 50, 25, 255)
    LEATHER_LO = (60, 30, 15, 255)
    PAGE = (245, 230, 195, 255)
    PAGE_SHADOW = (200, 180, 140, 255)
    GOLD = (220, 175, 60, 255)
    GOLD_HI = (250, 220, 100, 255)
    # Book cover
    fill_rect(img, 7, 7, 24, 25, LEATHER_MID)
    fill_rect(img, 7, 7, 24, 7, LEATHER_HI)
    fill_rect(img, 7, 7, 7, 25, LEATHER_HI)
    fill_rect(img, 7, 25, 24, 25, LEATHER_LO)
    fill_rect(img, 24, 7, 24, 25, LEATHER_LO)
    # Page edges (right side)
    fill_rect(img, 25, 9, 26, 24, PAGE)
    fill_rect(img, 25, 25, 26, 25, PAGE_SHADOW)
    # Gold border inside cover
    fill_rect(img, 9, 9, 22, 9, GOLD)
    fill_rect(img, 9, 23, 22, 23, GOLD)
    fill_rect(img, 9, 9, 9, 23, GOLD)
    fill_rect(img, 22, 9, 22, 23, GOLD)
    # Cross emblem in center
    fill_rect(img, 15, 12, 16, 20, GOLD)
    fill_rect(img, 13, 14, 18, 15, GOLD)
    px(img, 15, 12, GOLD_HI)
    px(img, 13, 14, GOLD_HI)
    # Decorative corners (Yahwist 4-corners motif)
    for cx, cy in [(10, 10), (21, 10), (10, 22), (21, 22)]:
        px(img, cx, cy, GOLD_HI)
    save(img, "yahwist_scripture")


def draw_sealed_scroll():
    img = new_canvas()
    PARCH_HI = (250, 235, 195, 255)
    PARCH_MID = (225, 205, 155, 255)
    PARCH_LO = (180, 155, 105, 255)
    # Rolled scroll (horizontal cylinder)
    fill_rect(img, 5, 13, 27, 19, PARCH_MID)
    fill_rect(img, 5, 13, 27, 13, PARCH_HI)
    fill_rect(img, 5, 19, 27, 19, PARCH_LO)
    # End rolls (darker)
    fill_rect(img, 4, 13, 5, 19, PARCH_LO)
    fill_rect(img, 27, 13, 28, 19, PARCH_LO)
    # End spiral indicator
    px(img, 5, 16, PARCH_MID); px(img, 27, 16, PARCH_MID)
    # Wax seal in middle (red blob with cross)
    WAX = (170, 20, 20, 255)
    WAX_HI = (220, 60, 60, 255)
    WAX_LO = (110, 10, 10, 255)
    ellipse_fill(img, 16, 16, 4, 3, WAX)
    px(img, 14, 15, WAX_HI); px(img, 15, 15, WAX_HI)
    px(img, 18, 18, WAX_LO)
    # Cross imprint on seal
    px(img, 16, 15, (250, 200, 120, 255))
    px(img, 16, 17, (250, 200, 120, 255))
    px(img, 15, 16, (250, 200, 120, 255))
    px(img, 17, 16, (250, 200, 120, 255))
    save(img, "sealed_scroll")


def draw_open_prayer_scroll():
    img = new_canvas()
    PARCH_HI = (250, 235, 195, 255)
    PARCH_MID = (225, 205, 155, 255)
    PARCH_LO = (180, 155, 105, 255)
    # Open parchment (vertical)
    fill_rect(img, 9, 7, 22, 25, PARCH_MID)
    fill_rect(img, 9, 7, 9, 25, PARCH_HI)
    fill_rect(img, 22, 7, 22, 25, PARCH_LO)
    # Curled top and bottom
    fill_rect(img, 8, 6, 23, 7, PARCH_LO)
    fill_rect(img, 8, 25, 23, 26, PARCH_LO)
    # End rolls (curls on edges)
    for y in range(7, 26):
        if y == 7 or y == 25:
            continue
    # Text lines (alternating)
    INK = (60, 40, 20, 255)
    for y in [10, 12, 14, 16, 18, 20, 22]:
        # Some shorter lines for variety
        end = 21 if y % 4 == 0 else 19
        for x in range(11, end):
            if (x + y) % 2 == 0:
                px(img, x, y, INK)
    # Illuminated capital at top — gold
    GOLD = (220, 175, 60, 255)
    GOLD_HI = (250, 220, 100, 255)
    fill_rect(img, 11, 9, 13, 11, GOLD)
    px(img, 11, 9, GOLD_HI)
    # Cross at bottom center
    RED = (180, 30, 30, 255)
    fill_rect(img, 15, 23, 16, 25, RED)
    fill_rect(img, 14, 24, 17, 24, RED)
    save(img, "open_prayer_scroll")


# ============================================================
# PHASE 6 — SPECIAL (2)
# ============================================================

def draw_cherubim_seal():
    """Mystical winged emblem — high-level prayer item."""
    img = new_canvas()
    SEAL_BG = (240, 230, 180, 255)
    SEAL_BG_HI = (255, 250, 220, 255)
    SEAL_RIM = (200, 165, 80, 255)
    GOLD = (220, 175, 60, 255)
    GOLD_HI = (250, 220, 100, 255)
    BLUE = (60, 120, 200, 255)
    BLUE_HI = (120, 180, 240, 255)
    # Circular disc
    ellipse_fill(img, 16, 16, 10, 10, SEAL_RIM)
    ellipse_fill(img, 16, 16, 9, 9, SEAL_BG)
    ellipse_fill(img, 16, 16, 8, 8, SEAL_BG_HI)
    ellipse_fill(img, 16, 16, 8, 8, SEAL_BG)
    # Gold border ring
    for ang_step in range(0, 32):
        import math
        a = ang_step * (3.14159 * 2 / 32)
        x = int(16 + 9.5 * math.cos(a))
        y = int(16 + 9.5 * math.sin(a))
        px(img, x, y, GOLD)
    # Winged motif — two upward-curving wings
    # Left wing
    for i, (x, y) in enumerate([(11, 14), (10, 13), (9, 14), (10, 15), (11, 16)]):
        px(img, x, y, BLUE if i % 2 else BLUE_HI)
    # Right wing
    for i, (x, y) in enumerate([(21, 14), (22, 13), (23, 14), (22, 15), (21, 16)]):
        px(img, x, y, BLUE if i % 2 else BLUE_HI)
    # Central eye / face
    fill_rect(img, 15, 14, 17, 18, GOLD_HI)
    px(img, 16, 15, (40, 30, 100, 255))  # pupil
    px(img, 16, 17, (180, 30, 30, 255))  # mouth dot
    # Halo around top
    px(img, 14, 12, GOLD_HI); px(img, 18, 12, GOLD_HI); px(img, 16, 11, GOLD_HI)
    # Faint outer glow
    for x, y in [(5, 16), (27, 16), (16, 5), (16, 27), (8, 8), (24, 8), (8, 24), (24, 24)]:
        if img.getpixel((x, y))[3] == 0:
            img.putpixel((x, y), (255, 240, 180, 70))
    save(img, "cherubim_seal")


def draw_demonic_ashes():
    """Cursed/demonic ash pile (red-tinged dark, for the Yahwist 'destroy this' track)."""
    img = new_canvas()
    DARK = (40, 25, 20, 255)
    MID = (90, 50, 40, 255)
    HI = (140, 80, 65, 255)
    EMBER = (220, 50, 30, 255)
    EMBER_HI = (255, 120, 50, 255)
    # Pile
    for y in range(20, 28):
        width = 30 - y
        for x in range(16 - width, 16 + width):
            d = abs(x - 16)
            if d < width - 5:
                px(img, x, y, HI)
            elif d < width - 2:
                px(img, x, y, MID)
            else:
                px(img, x, y, DARK)
    # Glowing embers
    px(img, 13, 23, EMBER_HI)
    px(img, 18, 24, EMBER)
    px(img, 16, 22, EMBER_HI)
    px(img, 14, 25, EMBER)
    # Stray dark wisps rising
    px(img, 14, 19, (60, 35, 30, 180))
    px(img, 18, 17, (60, 35, 30, 140))
    px(img, 16, 15, (60, 35, 30, 90))
    save(img, "demonic_ashes")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("Phase 1 — Bones")
    draw_bones()
    print("Phase 2 — Holy implements")
    draw_holy_water_vial()
    draw_anointing_oil_flask()
    draw_holy_symbol()
    draw_censer_lit()
    draw_censer_unlit()
    draw_incense_stick()
    draw_anointing_horn()
    print("Phase 3 — Communion")
    draw_unleavened_bread()
    draw_communion_cup()
    draw_bread_of_presence()
    draw_blessed_candle()
    print("Phase 4 — Priest garments")
    draw_priest_robe_top()
    draw_priest_robe_bottom()
    draw_mitre()
    draw_stole()
    print("Phase 5 — Books & scrolls")
    draw_yahwist_scripture()
    draw_sealed_scroll()
    draw_open_prayer_scroll()
    print("Phase 6 — Special")
    draw_cherubim_seal()
    draw_demonic_ashes()
    print(f"\nDone! 27 sprites at {OUT}")
