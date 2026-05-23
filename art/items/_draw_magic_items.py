#!/usr/bin/env python3
"""
Magic skill items — runes, talismans, staves.

15 runes : stone tablet + element-colored etched symbol
 8 talismans : small amulet on a cord, element-tinted gem
 6 staves : wooden shaft + elemental orb/crystal top

All 32×32 transparent PNG. Designed fresh (vanilla OpenRSC has
appearance=0 fallback for these items so there's no canonical sprite
to copy).
"""
import os, math
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
# RUNES — stone tablets with etched symbols
# ===========================================================

# Generic stone tablet background (16×16 rounded square)
STONE_DK = ( 60,  56,  50, 255)
STONE_B  = (110, 102,  90, 255)
STONE_HI = (160, 150, 130, 255)
STONE_OL = ( 30,  26,  20, 255)

TABLET = [
    ".OOOOOOOOOOOO.",
    "OBHHBBBBBBBSSO",
    "OBHBBBBBBBBSSO",
    "OBHBBBBBBBBSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBBSSSO",
    "OBBBBBBBBSSSSO",
    "OBBBBBBBSSSSSO",
    ".OOOOOOOOOOOO.",
]


def draw_tablet(px):
    """Draw the generic stone tablet — center it horizontally."""
    th = len(TABLET)
    tw = max(len(r) for r in TABLET)
    ox, oy = (W - tw) // 2, (H - th) // 2
    CM = {'O': STONE_OL, 'B': STONE_B, 'H': STONE_HI, 'S': STONE_DK}
    stamp(px, ox, oy, TABLET, CM)
    return ox, oy, tw, th


def draw_rune(symbol_fn, glow_color):
    """Create a rune sprite — tablet + colored symbol via symbol_fn."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Faint glow halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 16, y - 16
            d2 = dx * dx + dy * dy
            if 60 <= d2 <= 120 and (x + y) % 2 == 0:
                put(px, x, y, glow_color)
    ox, oy, tw, th = draw_tablet(px)
    # Symbol centered on tablet
    cx, cy = ox + tw // 2, oy + th // 2
    symbol_fn(px, cx, cy)
    return img


# Symbol drawing functions (small etched marks)
def sym_air(px, cx, cy):
    """Swirl / spiral."""
    GLOW = (255, 250, 220, 255)
    MID  = (220, 210, 180, 255)
    cells = [
        (-2, -1), (-1, -2), (0, -2), (1, -2), (2, -1),
        (2, 0),  (1, 1),    (0, 1),  (-1, 1),
        (-1, 0),
    ]
    for i, (dx, dy) in enumerate(cells):
        c = GLOW if i % 2 == 0 else MID
        put(px, cx + dx, cy + dy, c)


def sym_water(px, cx, cy):
    """Wavy line."""
    BLUE_HI = (140, 200, 255, 255)
    BLUE_DK = ( 40, 100, 200, 255)
    wave = [(-3, 0), (-2, -1), (-1, 0), (0, 1), (1, 0), (2, -1), (3, 0)]
    for x, y in wave:
        put(px, cx + x, cy + y, BLUE_HI)
        put(px, cx + x, cy + y + 1, BLUE_DK)


def sym_earth(px, cx, cy):
    """Cross / X."""
    BROWN_HI = (160, 110,  50, 255)
    BROWN_DK = (110,  70,  20, 255)
    for d in (-2, -1, 0, 1, 2):
        put(px, cx + d, cy + d, BROWN_DK)
        put(px, cx + d, cy - d, BROWN_DK)
    put(px, cx, cy, BROWN_HI)


def sym_fire(px, cx, cy):
    """Triangle pointing up (flame)."""
    HOT = (255, 220, 100, 255)
    MID = (255, 130,  40, 255)
    DK  = (180,  40,  20, 255)
    cells = [(0, -2), (-1, -1), (0, -1), (1, -1),
             (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
             (-2, 1), (2, 1)]
    for x, y in cells:
        if abs(x) <= 1 and y < 0:
            put(px, cx + x, cy + y, HOT)
        elif y == 0:
            put(px, cx + x, cy + y, MID)
        else:
            put(px, cx + x, cy + y, DK)


def sym_mind(px, cx, cy):
    """Dot in circle (eye)."""
    HI = (220, 220, 255, 255)
    DK = (100, 100, 180, 255)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x = cx + int(round(math.cos(rad) * 2.5))
        y = cy + int(round(math.sin(rad) * 2.5))
        put(px, x, y, DK)
    put(px, cx, cy, HI)


def sym_body(px, cx, cy):
    """Small stick figure."""
    O = (200, 130,  60, 255)
    # Head
    put(px, cx, cy - 2, O)
    # Body line
    put(px, cx, cy - 1, O); put(px, cx, cy, O); put(px, cx, cy + 1, O)
    # Arms
    put(px, cx - 1, cy, O); put(px, cx + 1, cy, O)
    put(px, cx - 2, cy - 1, O); put(px, cx + 2, cy - 1, O)
    # Legs
    put(px, cx - 1, cy + 2, O); put(px, cx + 1, cy + 2, O)


def sym_cosmic(px, cx, cy):
    """5-pointed star."""
    HI = (220, 180, 255, 255)
    DK = (130,  60, 200, 255)
    # 5-point star
    for ang in range(0, 360, 72):
        rad = math.radians(ang - 90)
        x = cx + int(round(math.cos(rad) * 3))
        y = cy + int(round(math.sin(rad) * 3))
        put(px, x, y, HI)
    put(px, cx, cy, DK)


def sym_chaos(px, cx, cy):
    """Zigzag lightning."""
    HOT = (255, 100, 100, 255)
    DK  = (160,  30,  30, 255)
    pts = [(-2, -2), (-1, -1), (0, 0), (-1, 1), (0, 2), (1, 1), (2, 2)]
    for i, (dx, dy) in enumerate(pts):
        c = HOT if i % 2 == 0 else DK
        put(px, cx + dx, cy + dy, c)


def sym_nature(px, cx, cy):
    """Leaf shape."""
    GR_HI = (120, 220, 100, 255)
    GR_DK = ( 30,  90,  20, 255)
    # Leaf body
    put(px, cx, cy - 2, GR_HI)
    put(px, cx - 1, cy - 1, GR_DK); put(px, cx, cy - 1, GR_HI); put(px, cx + 1, cy - 1, GR_HI)
    put(px, cx - 1, cy, GR_HI); put(px, cx, cy, GR_HI); put(px, cx + 1, cy, GR_DK)
    put(px, cx - 1, cy + 1, GR_DK); put(px, cx, cy + 1, GR_HI); put(px, cx + 1, cy + 1, GR_DK)
    put(px, cx, cy + 2, GR_DK)


def sym_law(px, cx, cy):
    """Balanced scales (T shape)."""
    GOLD = (255, 220, 120, 255)
    DK   = (200, 170,  60, 255)
    # Horizontal bar
    for dx in (-2, -1, 0, 1, 2):
        put(px, cx + dx, cy - 1, GOLD)
    # Vertical
    for dy in (0, 1, 2):
        put(px, cx, cy + dy, GOLD)
    # End caps
    put(px, cx - 2, cy, DK); put(px, cx + 2, cy, DK)


def sym_death(px, cx, cy):
    """Skull silhouette."""
    BONE = (200, 180, 200, 255)
    DK   = ( 40,  10,  60, 255)
    # Mini skull
    put(px, cx - 1, cy - 2, BONE); put(px, cx, cy - 2, BONE); put(px, cx + 1, cy - 2, BONE)
    put(px, cx - 1, cy - 1, DK);   put(px, cx, cy - 1, BONE); put(px, cx + 1, cy - 1, DK)
    put(px, cx - 1, cy, BONE);     put(px, cx, cy, BONE);     put(px, cx + 1, cy, BONE)
    put(px, cx - 1, cy + 1, DK);   put(px, cx + 1, cy + 1, DK)


def sym_blood(px, cx, cy):
    """Drop shape."""
    HI = (255, 100, 100, 255)
    MID = (180,  30,  20, 255)
    DK  = (100,   0,   0, 255)
    put(px, cx, cy - 2, MID)
    put(px, cx - 1, cy - 1, MID); put(px, cx, cy - 1, HI); put(px, cx + 1, cy - 1, MID)
    put(px, cx - 1, cy, MID); put(px, cx, cy, MID); put(px, cx + 1, cy, DK)
    put(px, cx, cy + 1, DK)


def sym_soul(px, cx, cy):
    """Spirit swirl — wisp going up."""
    PALE = (220, 240, 255, 255)
    DK   = (120, 160, 200, 255)
    cells = [
        (0, -2), (1, -1), (-1, -1), (-1, 0), (0, 0), (1, 0),
        (-1, 1), (1, 1), (0, 2),
    ]
    for i, (dx, dy) in enumerate(cells):
        c = PALE if i % 2 == 0 else DK
        put(px, cx + dx, cy + dy, c)


def sym_life(px, cx, cy):
    """OGRS Life rune — heart/ankh shape."""
    PINK = (255, 180, 200, 255)
    DK   = (180,  40,  80, 255)
    # Cross / ankh
    put(px, cx, cy - 2, DK); put(px, cx, cy - 1, PINK); put(px, cx, cy, PINK)
    put(px, cx, cy + 1, PINK); put(px, cx, cy + 2, PINK)
    put(px, cx - 1, cy, PINK); put(px, cx + 1, cy, PINK)
    put(px, cx - 2, cy - 1, DK); put(px, cx + 2, cy - 1, DK)


def sym_astral(px, cx, cy):
    """OGRS Astral rune — crescent moon."""
    SILVER = (240, 240, 255, 255)
    DK     = (100, 120, 180, 255)
    # Crescent
    put(px, cx, cy - 2, SILVER); put(px, cx + 1, cy - 2, SILVER)
    put(px, cx - 1, cy - 1, SILVER); put(px, cx + 1, cy - 1, SILVER)
    put(px, cx - 1, cy, SILVER); put(px, cx + 1, cy, SILVER)
    put(px, cx - 1, cy + 1, SILVER); put(px, cx + 1, cy + 1, SILVER)
    put(px, cx, cy + 2, SILVER); put(px, cx + 1, cy + 2, SILVER)
    # Inner shadow (the moon's dark side)
    put(px, cx, cy, DK)


# 15 runes — name → (symbol_function, glow_color)
RUNES = [
    ('air_rune',     sym_air,     (255, 250, 220, 120)),
    ('water_rune',   sym_water,   (140, 200, 255, 120)),
    ('earth_rune',   sym_earth,   (160, 110,  50, 100)),
    ('fire_rune',    sym_fire,    (255, 130,  40, 120)),
    ('mind_rune',    sym_mind,    (180, 200, 240, 110)),
    ('body_rune',    sym_body,    (220, 160,  90, 110)),
    ('cosmic_rune',  sym_cosmic,  (180, 130, 240, 130)),
    ('chaos_rune',   sym_chaos,   (200,  50,  50, 130)),
    ('nature_rune',  sym_nature,  (100, 200,  80, 130)),
    ('law_rune',     sym_law,     (255, 240, 180, 140)),
    ('death_rune',   sym_death,   (130,  60, 180, 140)),
    ('blood_rune',   sym_blood,   (200,  20,  20, 130)),
    ('soul_rune',    sym_soul,    (180, 220, 255, 140)),
    ('life_rune',    sym_life,    (240, 130, 170, 130)),
    ('astral_rune',  sym_astral,  (200, 220, 255, 140)),
]


# ===========================================================
# TALISMANS — small amulet on cord, element-tinted
# ===========================================================

def draw_talisman(stone_color, glow_color):
    """Talisman = cord + circular stone pendant."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    OL    = ( 40,  20,  10, 255)
    CORD  = (140,  90,  40, 255)
    METAL = (180, 170, 130, 255)
    # Cord (V-shape from top)
    cord_pts = [(11, 6), (12, 7), (13, 8), (14, 9), (15, 10),
                (16, 10), (17, 10), (18, 9), (19, 8), (20, 7), (21, 6)]
    for x, y in cord_pts:
        put(px, x, y, CORD)
    # Metal cap on pendant
    for dx in range(-2, 3):
        put(px, 16 + dx, 11, METAL)
    put(px, 16, 10, METAL)
    # Halo
    for x in range(W):
        for y in range(H):
            dx, dy = x - 16, y - 19
            d2 = dx * dx + dy * dy
            if 50 <= d2 <= 100 and (x + y) % 2 == 0:
                put(px, x, y, glow_color)
    # Round stone pendant (8 wide × 9 tall)
    PENDANT = [
        "..OOOOOO..",
        ".OBHHHHBSO.",
        "OBHHHHHHBSO",
        "OBHHHHHHHSO",
        "OBHHHHHHSSO",
        "OBHHHHHSSSO",
        ".OBBBSSSSO.",
        "..OOOOOOO..",
    ]
    sh = list(stone_color[:3]) + [255]
    hi = [min(255, c + 50) for c in stone_color[:3]] + [255]
    dk = [max(0, c - 50) for c in stone_color[:3]] + [255]
    CM = {'O': OL, 'B': tuple(sh), 'H': tuple(hi), 'S': tuple(dk)}
    stamp(px, 11, 12, PENDANT, CM)
    return img


TALISMANS = [
    ('air_talisman',     (220, 220, 200), (255, 250, 220, 120)),
    ('water_talisman',   ( 60, 130, 220), (140, 200, 255, 120)),
    ('earth_talisman',   (130,  90,  40), (160, 110,  50, 100)),
    ('fire_talisman',    (220,  60,  20), (255, 130,  40, 120)),
    ('mind_talisman',    (160, 180, 220), (180, 200, 240, 110)),
    ('body_talisman',    (200, 140,  80), (220, 160,  90, 110)),
    ('cosmic_talisman',  (140,  90, 200), (180, 130, 240, 130)),
    ('chaos_talisman',   (160,  20,  20), (200,  50,  50, 130)),
]


# ===========================================================
# STAVES — wooden shaft + elemental orb top
# ===========================================================

def draw_staff(orb_color, orb_glow=None, shaft_palette=None, has_crystal=False):
    """Staff = diagonal wooden shaft + spherical orb at top with glow."""
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Shaft palette
    if shaft_palette is None:
        shaft_palette = ((90, 60, 30), (160, 110, 60), (220, 170, 100))
    WOOD_DK, WOOD_B, WOOD_HI = (tuple(c) + (255,) for c in shaft_palette)
    OL = (30, 16, 8, 255)

    # Diagonal shaft from lower-left to upper-right
    for i in range(22):
        x = 6 + i
        y = 26 - i
        if 0 <= x < W and 0 <= y < H:
            put(px, x, y, WOOD_B)
            put(px, x + 1, y, WOOD_HI)
            put(px, x, y + 1, WOOD_DK)
            put(px, x - 1, y, OL)
            put(px, x, y - 1, OL)

    # Glow around the orb
    orb_cx, orb_cy = 26, 6
    if orb_glow:
        for x in range(W):
            for y in range(H):
                dx, dy = x - orb_cx, y - orb_cy
                d2 = dx * dx + dy * dy
                if 25 <= d2 <= 60 and (x + y) % 2 == 0:
                    put(px, x, y, orb_glow)

    # Orb at top (5×5 sphere)
    orb_hi = tuple(min(255, c + 60) for c in orb_color[:3]) + (255,)
    orb_dk = tuple(max(0, c - 60) for c in orb_color[:3]) + (255,)
    orb_b  = orb_color
    if not has_crystal:
        cells = {
            (-1, -2): OL, (0, -2): OL, (1, -2): OL,
            (-2, -1): OL, (-1, -1): orb_hi, (0, -1): orb_hi, (1, -1): orb_b, (2, -1): OL,
            (-2, 0):  OL, (-1, 0):  orb_hi, (0, 0):  orb_b,  (1, 0):  orb_dk, (2, 0):  OL,
            (-2, 1):  OL, (-1, 1):  orb_b,  (0, 1):  orb_dk, (1, 1):  orb_dk, (2, 1):  OL,
            (-1, 2):  OL, (0, 2):   OL,     (1, 2):  OL,
        }
    else:
        # Crystal — diamond-shape pointing up
        cells = {
            (0, -3): OL,
            (-1, -2): OL, (0, -2): orb_hi, (1, -2): OL,
            (-2, -1): OL, (-1, -1): orb_hi, (0, -1): orb_b, (1, -1): orb_b, (2, -1): OL,
            (-2, 0):  OL, (-1, 0):  orb_b,  (0, 0):  orb_b, (1, 0):  orb_dk, (2, 0): OL,
            (-1, 1):  OL, (0, 1):   orb_dk, (1, 1):  OL,
            (0, 2):   OL,
        }
    for (dx, dy), c in cells.items():
        put(px, orb_cx + dx, orb_cy + dy, c)

    return img


STAVES = [
    # (name, orb_color, glow_color, shaft_palette, has_crystal)
    ('staff_basic',       (160, 130,  80, 255), None,                            None, False),   # plain wooden staff, brown orb
    ('staff_magic',       (180, 140, 200, 255), (220, 180, 255, 100),            None, False),   # magic staff, purple orb + glow
    ('staff_of_air',      (240, 240, 220, 255), (255, 250, 220, 130),            None, False),
    ('staff_of_water',    (100, 160, 240, 255), (140, 200, 255, 130),            None, False),
    ('staff_of_earth',    (140, 100,  60, 255), (160, 110,  50, 120),            None, False),
    ('staff_of_fire',     (240, 110,  40, 255), (255, 130,  40, 130),            None, False),
    ('battlestaff',       (140, 180, 200, 255), (180, 220, 255, 140),
                         ((20, 30, 60), (70, 100, 160), (130, 160, 220)), True),   # mithril-bound, crystal top
]


# ===========================================================
# DRIVER
# ===========================================================
if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/items/magic"

    # Runes
    out = f"{base}/runes"
    os.makedirs(out, exist_ok=True)
    for name, sym_fn, glow in RUNES:
        img = draw_rune(sym_fn, glow)
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"  rune: {name}")

    # Talismans
    out = f"{base}/talismans"
    os.makedirs(out, exist_ok=True)
    for name, stone, glow in TALISMANS:
        img = draw_talisman(stone, glow)
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"  talisman: {name}")

    # Staves
    out = f"{base}/staves"
    os.makedirs(out, exist_ok=True)
    for name, orb, glow, shaft, crystal in STAVES:
        img = draw_staff(orb, glow, shaft, crystal)
        img.save(f"{out}/{name}.png")
        img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/{name}_x8.png")
        print(f"  staff: {name}")

    print(f"\n=== Magic items complete: {len(RUNES) + len(TALISMANS) + len(STAVES)} sprites ===")
