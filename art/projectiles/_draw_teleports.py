#!/usr/bin/env python3
"""
6 city teleport spells — each town-themed and visually distinct.
30×30 4-frame each. Cast on player so animation is the visual that
plays around the caster as they depart.

Town themes:
- VARROCK     : blue rune circle (capital — mage tower vibe)
- LUMBRIDGE   : warm orange cottage glow (starter — friendly)
- FALADOR     : white knight cross (Saradomin holy city)
- CAMELOT     : royal purple crown silhouette (king-and-knights)
- ARDOUGNE    : green forest swirl (woodland kingdom)
- WATCHTOWER  : grey tower beam (literal tower)

Frame arc per teleport:
0 = rune/symbol appearing
1 = symbol fully formed
2 = peak — bright flash as departure occurs
3 = symbol fading
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# ===========================================================
# VARROCK — blue rune circle
# ===========================================================
VAR_DEEP   = ( 20,  30,  80, 255)
VAR_BASE   = ( 50,  80, 180, 255)
VAR_HIGH   = (130, 170, 240, 255)
VAR_PEAK   = (220, 230, 255, 255)
VAR_RUNE   = (180, 200, 255, 255)


def varrock_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Outer rune ring
    intensity = [0.5, 0.8, 1.0, 0.6][frame]
    for ang_deg in range(0, 360, 30):
        ang = math.radians(ang_deg + frame * 15)
        # Inner ring at r=8
        r = 8
        x = CX + int(round(math.cos(ang) * r))
        y = CY + int(round(math.sin(ang) * r))
        put(px, x, y, VAR_HIGH if intensity >= 0.8 else VAR_BASE)
        # Outer ring at r=12
        x = CX + int(round(math.cos(ang) * 12))
        y = CY + int(round(math.sin(ang) * 12))
        put(px, x, y, VAR_BASE if intensity >= 0.6 else VAR_DEEP)
    # Rune glyphs (small marks at cardinal positions, varying per frame)
    rune_positions = [(0, -10), (10, 0), (0, 10), (-10, 0)]
    for dx, dy in rune_positions:
        put(px, CX + dx, CY + dy, VAR_RUNE)
        put(px, CX + dx - 1, CY + dy, VAR_RUNE if (dx, dy) == (0, -10) else VAR_BASE)
    # Center pulse
    if frame == 2:
        for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            put(px, CX + dx, CY + dy, VAR_PEAK)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            put(px, CX + dx, CY + dy, VAR_HIGH)
    elif frame >= 1:
        put(px, CX, CY, VAR_HIGH)
    return img


# ===========================================================
# LUMBRIDGE — warm orange cottage glow
# ===========================================================
LUM_DEEP   = (120,  60,  20, 255)
LUM_BASE   = (220, 130,  50, 255)
LUM_HIGH   = (255, 200, 120, 255)
LUM_PEAK   = (255, 240, 200, 255)
LUM_SMOKE  = (160, 130, 100, 255)


def lumbridge_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Cottage roof + window glow silhouette (cute pictogram)
    # Roof: triangle apex (CX, CY-7) base from (CX-6, CY-1) to (CX+6, CY-1)
    for y_off in range(-7, 0):
        half_w = abs(y_off + 7) - 7 if y_off > -7 else 0
        # Actually roof: at y=-7 width 1, at y=-1 width 13
        half_w = (7 + y_off) + 1
        for x_off in range(-half_w, half_w + 1):
            if abs(x_off) == half_w or y_off == -7:
                put(px, CX + x_off, CY + y_off, LUM_DEEP)
            else:
                put(px, CX + x_off, CY + y_off, LUM_BASE if frame < 2 else LUM_HIGH)
    # Cottage body
    for y_off in range(0, 6):
        for x_off in range(-5, 6):
            if abs(x_off) == 5 or y_off == 5:
                put(px, CX + x_off, CY + y_off, LUM_DEEP)
            else:
                put(px, CX + x_off, CY + y_off, LUM_BASE)
    # Window
    win_color = LUM_PEAK if frame == 2 else LUM_HIGH
    for dy in (1, 2, 3):
        for dx in (-1, 0, 1):
            put(px, CX + dx, CY + dy, win_color)
    # Door silhouette
    put(px, CX + 3, CY + 3, LUM_DEEP)
    put(px, CX + 3, CY + 4, LUM_DEEP)
    # Chimney smoke rising
    smoke_pos = {0: [(CX + 3, CY - 8)],
                 1: [(CX + 3, CY - 8), (CX + 4, CY - 10)],
                 2: [(CX + 3, CY - 8), (CX + 4, CY - 10), (CX + 3, CY - 12)],
                 3: [(CX + 4, CY - 9)]}
    for x, y in smoke_pos[frame]:
        put(px, x, y, LUM_SMOKE)
    # Warm aura glow around the cottage at peak
    if frame == 2:
        for ang_deg in range(0, 360, 45):
            ang = math.radians(ang_deg)
            r = 13
            x = CX + int(round(math.cos(ang) * r))
            y = CY + int(round(math.sin(ang) * r))
            put(px, x, y, LUM_HIGH)
    return img


# ===========================================================
# FALADOR — white knight cross (Saradomin)
# ===========================================================
FAL_OUTLINE = ( 80,  90, 110, 255)
FAL_BASE    = (220, 225, 235, 255)
FAL_PEAK    = (255, 255, 255, 255)
FAL_GOLD    = (240, 215, 130, 255)


def falador_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Large vertical cross + horizontal cross beam
    # Vertical bar
    for dy in range(-9, 10):
        for dx in (-1, 0, 1):
            color = FAL_PEAK if frame == 2 and dx == 0 else FAL_BASE
            put(px, CX + dx, CY + dy, color)
            # Outline
            put(px, CX + dx + 2 if dx == 1 else CX + dx - 2, CY + dy, FAL_OUTLINE)
    # Horizontal bar (slightly higher)
    for dx in range(-8, 9):
        for dy in (-1, 0, 1):
            color = FAL_PEAK if frame == 2 and dy == 0 else FAL_BASE
            put(px, CX + dx, CY + dy - 2, color)
    # Outline around the cross
    for dx in range(-8, 9):
        put(px, CX + dx, CY - 5, FAL_OUTLINE)
        put(px, CX + dx, CY + 1, FAL_OUTLINE)
    # Gold accents at the cross-tips when peak
    if frame == 2:
        for x, y in [(CX, CY - 10), (CX, CY + 10), (CX - 9, CY - 2), (CX + 9, CY - 2)]:
            put(px, x, y, FAL_GOLD)
    return img


# ===========================================================
# CAMELOT — royal purple crown silhouette
# ===========================================================
CAM_DEEP   = ( 50,  20,  90, 255)
CAM_BASE   = (110,  60, 180, 255)
CAM_HIGH   = (180, 130, 230, 255)
CAM_PEAK   = (240, 220, 255, 255)
CAM_GOLD   = (250, 215, 100, 255)
CAM_JEWEL  = (220,  60,  60, 255)


def camelot_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Crown silhouette — base band + 3 spikes + jewel in middle
    # Base band (rows 14-17)
    for dx in range(-7, 8):
        put(px, CX + dx, CY + 2, CAM_GOLD)
        put(px, CX + dx, CY + 3, CAM_DEEP)
    # Crown body (rows 11-13)
    for dx in range(-7, 8):
        for dy in range(-2, 2):
            put(px, CX + dx, CY + dy, CAM_BASE)
    # Crown bottom
    for dx in range(-7, 8):
        if abs(dx) % 2 == 0:
            put(px, CX + dx, CY + 1, CAM_HIGH)
    # 3 spikes on top
    spike_xs = [-5, 0, 5]
    for sx in spike_xs:
        # 3-pixel-tall spike
        for dy in range(-5, -2):
            put(px, CX + sx, CY + dy, CAM_BASE)
            put(px, CX + sx - 1 if dy > -5 else CX + sx, CY + dy, CAM_DEEP)
            put(px, CX + sx + 1 if dy > -5 else CX + sx, CY + dy, CAM_DEEP)
    # Tip jewels on spikes
    for sx in spike_xs:
        put(px, CX + sx, CY - 6, CAM_JEWEL if frame == 2 else CAM_HIGH)
    # Center jewel (big)
    put(px, CX, CY, CAM_JEWEL)
    put(px, CX - 1, CY, CAM_DEEP)
    put(px, CX + 1, CY, CAM_DEEP)
    put(px, CX, CY - 1, CAM_PEAK if frame == 2 else CAM_HIGH)
    return img


# ===========================================================
# ARDOUGNE — green forest swirl
# ===========================================================
ARD_DEEP    = ( 20,  60,  20, 255)
ARD_BASE    = ( 60, 120,  40, 255)
ARD_LEAF    = (110, 180,  60, 255)
ARD_HIGH    = (180, 230, 100, 255)
ARD_BARK    = ( 80,  50,  20, 255)


def ardougne_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Central tree silhouette + spiral leaves
    # Trunk
    for dy in range(2, 8):
        put(px, CX, CY + dy, ARD_BARK)
        put(px, CX + 1, CY + dy, ARD_DEEP)
    # Canopy — 3 leafy clusters
    canopy_cells = {
        (-4, -3): ARD_BASE, (-3, -3): ARD_LEAF, (-2, -3): ARD_LEAF, (-1, -3): ARD_BASE,
        (-5, -2): ARD_BASE, (-4, -2): ARD_LEAF, (-3, -2): ARD_HIGH, (-2, -2): ARD_LEAF,
        (-1, -2): ARD_LEAF, (0, -2): ARD_LEAF, (1, -2): ARD_LEAF,
        (2, -2): ARD_LEAF, (3, -2): ARD_LEAF, (4, -2): ARD_BASE,
        (-4, -1): ARD_LEAF, (-3, -1): ARD_LEAF, (-2, -1): ARD_HIGH, (-1, -1): ARD_LEAF,
        (0, -1): ARD_LEAF, (1, -1): ARD_LEAF, (2, -1): ARD_HIGH, (3, -1): ARD_LEAF,
        (4, -1): ARD_LEAF,
        (-3, 0): ARD_BASE, (-2, 0): ARD_LEAF, (-1, 0): ARD_LEAF, (0, 0): ARD_LEAF,
        (1, 0): ARD_LEAF, (2, 0): ARD_LEAF, (3, 0): ARD_BASE,
        (-2, 1): ARD_BASE, (-1, 1): ARD_LEAF, (0, 1): ARD_LEAF, (1, 1): ARD_LEAF, (2, 1): ARD_BASE,
    }
    for (dx, dy), c in canopy_cells.items():
        if frame == 2 and c == ARD_LEAF:
            c = ARD_HIGH
        put(px, CX + dx, CY + dy, c)
    # Swirling leaves around the tree (orbiting at radius 11)
    offset = frame * 30
    for i in range(5):
        ang = math.radians(i * 72 + offset)
        r = 11
        x = CX + int(round(math.cos(ang) * r))
        y = CY + int(round(math.sin(ang) * r))
        put(px, x, y, ARD_LEAF)
    return img


# ===========================================================
# WATCHTOWER — grey stone tower with light beam
# ===========================================================
WT_OUTLINE = ( 30,  30,  35, 255)
WT_DEEP    = ( 60,  60,  70, 255)
WT_BASE    = (110, 110, 120, 255)
WT_HIGH    = (170, 170, 180, 255)
WT_BEAM    = (255, 240, 180, 255)
WT_BEAM_HI = (255, 255, 220, 255)


def watchtower_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # Tower body — narrow rectangle, crenellated top, wider base
    # Crenellations (top)
    for dx in (-4, -2, 0, 2, 4):
        put(px, CX + dx, CY - 8, WT_OUTLINE)
        put(px, CX + dx, CY - 7, WT_BASE)
    for dx in range(-5, 6):
        put(px, CX + dx, CY - 6, WT_OUTLINE)
    # Tower middle (3 wide narrow column going down)
    for dy in range(-5, 6):
        put(px, CX - 3, CY + dy, WT_OUTLINE)
        put(px, CX + 3, CY + dy, WT_OUTLINE)
        for dx in (-2, -1, 0, 1, 2):
            put(px, CX + dx, CY + dy, WT_HIGH if dx == 0 else WT_BASE)
    # Window in middle (lit)
    window_color = WT_BEAM_HI if frame == 2 else WT_BEAM
    put(px, CX, CY - 1, window_color)
    put(px, CX, CY, window_color)
    put(px, CX - 1, CY, window_color if frame == 2 else WT_HIGH)
    put(px, CX + 1, CY, window_color if frame == 2 else WT_HIGH)
    # Tower base
    for dx in range(-5, 6):
        put(px, CX + dx, CY + 6, WT_DEEP)
        put(px, CX + dx, CY + 7, WT_OUTLINE)
    # Light beam emanating from top (only on later frames)
    if frame >= 1:
        for dy in range(-13, -7):
            for dx in (-1, 0, 1):
                if frame == 2:
                    put(px, CX + dx, CY + dy, WT_BEAM_HI if dx == 0 else WT_BEAM)
                else:
                    put(px, CX + dx, CY + dy, WT_BEAM if dx == 0 else WT_HIGH)
    return img


# ===========================================================
# Driver
# ===========================================================
SPELLS = [
    ("tele_varrock",    varrock_frame),
    ("tele_lumbridge",  lumbridge_frame),
    ("tele_falador",    falador_frame),
    ("tele_camelot",    camelot_frame),
    ("tele_ardougne",   ardougne_frame),
    ("tele_watchtower", watchtower_frame),
]

if __name__ == "__main__":
    for folder, fn in SPELLS:
        out = f"/home/sparky/ogrs/art/projectiles/{folder}/frames"
        os.makedirs(out, exist_ok=True)
        for i in range(4):
            img = fn(i)
            img.save(f"{out}/frame_{i:02d}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/frame_{i:02d}_x8.png")
        print(f"done: {folder}")
