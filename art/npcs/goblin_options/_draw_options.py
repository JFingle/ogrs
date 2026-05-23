#!/usr/bin/env python3
"""
Goblin design options — 3 directions for replacing the current goblin sprite.

Existing sprite (slot 139): a small grey bestial creature, NOT a classic
humanoid goblin. OpenRSC redrew the goblin as original art.

Each option below is a single idle pose at ~60×60 to show the design
direction. Full 18-frame animation cycles come later if Sparky picks one.

A: Polished bestial — same creature, sharper
B: Humanoid goblin — classic green slumped humanoid with club
C: 3 species variants — Hound (current), Warrior (humanoid), Shaman (robed)
"""
import os, math
from PIL import Image

CANVAS = 60
TRANS = (0, 0, 0, 0)


def make_canvas():
    return Image.new("RGBA", (CANVAS, CANVAS), TRANS)


def put(px, x, y, c):
    if c is not None and 0 <= x < CANVAS and 0 <= y < CANVAS:
        px[x, y] = c


def put_block(px, x, y, w, h, c):
    for dx in range(w):
        for dy in range(h):
            put(px, x + dx, y + dy, c)


# ===========================================================
# OPTION A — POLISHED BESTIAL
# Cleaned up version of the existing creature
# ===========================================================
A_OUTLINE = ( 28,  24,  30, 255)
A_FUR_DK  = ( 70,  68,  78, 255)
A_FUR_BASE= (110, 108, 118, 255)
A_FUR_HI  = (170, 168, 180, 255)
A_BELLY   = (140, 135, 145, 255)
A_EYE     = (220,  40,  40, 255)
A_EYE_HI  = (255, 200, 200, 255)
A_TOOTH   = (240, 220, 120, 255)
A_CLAW    = ( 50,  44,  50, 255)
A_TONGUE  = (180,  50,  60, 255)


def option_a_polished():
    img = make_canvas()
    px = img.load()
    # Side-view 4-legged beast, head at right
    # Body bulk
    put_block(px, 14, 30, 30, 14, A_FUR_BASE)
    # Belly underside
    put_block(px, 17, 42, 24, 3, A_BELLY)
    # Body outline
    for x in range(14, 44):
        put(px, x, 29, A_OUTLINE)
        put(px, x, 44, A_OUTLINE)
    for y in range(30, 44):
        put(px, 13, y, A_OUTLINE)
    # Back fur tufts (spiky)
    for x in [16, 19, 22, 25, 28, 31, 34, 37]:
        put(px, x, 28, A_FUR_DK)
        put(px, x, 27, A_FUR_DK)
        put(px, x, 26, A_OUTLINE)
    # Head (right side, larger)
    put_block(px, 38, 24, 14, 14, A_FUR_BASE)
    # Head outline
    for x in range(37, 53):
        put(px, x, 23, A_OUTLINE)
        put(px, x, 38, A_OUTLINE)
    for y in range(24, 38):
        put(px, 36, y, A_OUTLINE)
        put(px, 52, y, A_OUTLINE)
    # Snout (juts forward, right side)
    put_block(px, 50, 30, 4, 6, A_FUR_DK)
    for x in range(50, 54):
        put(px, x, 29, A_OUTLINE)
        put(px, x, 36, A_OUTLINE)
    put(px, 54, 31, A_OUTLINE)
    put(px, 54, 32, A_OUTLINE)
    put(px, 54, 33, A_OUTLINE)
    put(px, 54, 34, A_OUTLINE)
    put(px, 54, 35, A_OUTLINE)
    # Eyes (red, predator)
    put_block(px, 44, 27, 2, 2, A_EYE)
    put_block(px, 48, 27, 2, 2, A_EYE)
    put(px, 44, 27, A_EYE_HI)
    put(px, 48, 27, A_EYE_HI)
    # Eye outline
    for x, y in [(43, 27), (43, 28), (44, 26), (45, 26), (45, 27), (45, 28),
                 (47, 27), (47, 28), (48, 26), (49, 26), (49, 27), (49, 28)]:
        if px[x, y] == TRANS:
            put(px, x, y, A_OUTLINE)
    # Teeth (yellow fangs)
    put(px, 51, 35, A_TOOTH)
    put(px, 53, 35, A_TOOTH)
    put(px, 52, 36, A_TONGUE)
    # Ears (small, pointed back)
    put(px, 38, 22, A_OUTLINE)
    put(px, 39, 21, A_OUTLINE)
    put(px, 40, 22, A_OUTLINE)
    put(px, 39, 22, A_FUR_DK)
    # Front legs (right side)
    put_block(px, 39, 44, 3, 6, A_FUR_DK)
    put_block(px, 39, 48, 3, 2, A_CLAW)
    # Back legs (left side)
    put_block(px, 16, 44, 3, 6, A_FUR_DK)
    put_block(px, 16, 48, 3, 2, A_CLAW)
    # Tail (curving up-left from rear)
    for i, (dx, dy) in enumerate([(0, 0), (-2, 0), (-4, -1), (-5, -3), (-5, -5)]):
        put(px, 13 + dx, 33 + dy, A_FUR_DK)
        put(px, 13 + dx, 34 + dy, A_OUTLINE)
    # Highlight along the top of the body
    for x in [18, 21, 24, 27, 30, 33, 36, 38]:
        put(px, x, 31, A_FUR_HI)
    return img


# ===========================================================
# OPTION B — CLASSIC HUMANOID GOBLIN
# Small, hunched, green-skinned, club + loincloth
# ===========================================================
B_OUTLINE   = ( 16,  28,  16, 255)
B_SKIN_DK   = ( 56,  90,  36, 255)
B_SKIN_BASE = ( 90, 140,  60, 255)
B_SKIN_HI   = (140, 180,  90, 255)
B_LOIN_DK   = ( 70,  44,  20, 255)
B_LOIN_BASE = (130,  80,  40, 255)
B_LOIN_HI   = (180, 130,  70, 255)
B_TOOTH     = (240, 220, 120, 255)
B_EYE       = (210,  40,  40, 255)
B_EYE_W     = (240, 240, 200, 255)
B_CLUB_DK   = ( 70,  44,  20, 255)
B_CLUB_BASE = (130,  90,  50, 255)


def option_b_humanoid():
    img = make_canvas()
    px = img.load()
    # Hunched humanoid, facing right
    # HEAD (big, with big nose and ears)
    # Head body
    put_block(px, 24, 14, 14, 14, B_SKIN_BASE)
    for x in range(23, 39):
        put(px, x, 13, B_OUTLINE)
        put(px, x, 28, B_OUTLINE)
    for y in range(14, 28):
        put(px, 23, y, B_OUTLINE)
        put(px, 38, y, B_OUTLINE)
    # Big pointed ears (sticking sideways)
    for y in [17, 18, 19]:
        put(px, 22, y, B_SKIN_BASE)
        put(px, 21, y, B_OUTLINE)
    put(px, 20, 18, B_OUTLINE)
    for y in [17, 18, 19]:
        put(px, 39, y, B_SKIN_BASE)
        put(px, 40, y, B_OUTLINE)
    put(px, 41, 18, B_OUTLINE)
    # Big nose (juts forward)
    put_block(px, 38, 19, 4, 4, B_SKIN_DK)
    for x in range(38, 42):
        put(px, x, 18, B_OUTLINE)
        put(px, x, 23, B_OUTLINE)
    put(px, 42, 19, B_OUTLINE)
    put(px, 42, 20, B_OUTLINE)
    put(px, 42, 21, B_OUTLINE)
    put(px, 42, 22, B_OUTLINE)
    # Eyes (small, beady)
    put(px, 28, 18, B_EYE_W)
    put(px, 28, 19, B_EYE)
    put(px, 32, 18, B_EYE_W)
    put(px, 32, 19, B_EYE)
    # Brow ridge
    for x in range(27, 34):
        put(px, x, 17, B_OUTLINE)
    # Teeth (yellow fangs)
    put(px, 30, 24, B_TOOTH)
    put(px, 32, 24, B_TOOTH)
    for x in range(27, 35):
        put(px, x, 25, B_OUTLINE)
    # Skin highlight on forehead
    put(px, 25, 15, B_SKIN_HI)
    put(px, 26, 15, B_SKIN_HI)
    put(px, 27, 15, B_SKIN_HI)

    # BODY (small, hunched chest)
    put_block(px, 22, 28, 14, 10, B_SKIN_BASE)
    for x in range(21, 37):
        put(px, x, 28, B_OUTLINE)
        put(px, x, 38, B_OUTLINE)
    for y in range(29, 38):
        put(px, 21, y, B_OUTLINE)
        put(px, 36, y, B_OUTLINE)
    # Belly shading
    put_block(px, 25, 33, 10, 4, B_SKIN_DK)

    # LOINCLOTH (brown wrap)
    put_block(px, 21, 38, 16, 5, B_LOIN_BASE)
    for x in range(21, 38):
        put(px, x, 43, B_OUTLINE)
    put(px, 20, 39, B_OUTLINE)
    put(px, 20, 40, B_OUTLINE)
    put(px, 20, 41, B_OUTLINE)
    put(px, 37, 39, B_OUTLINE)
    put(px, 37, 40, B_OUTLINE)
    put(px, 37, 41, B_OUTLINE)
    # Loincloth folds / highlight
    put(px, 24, 39, B_LOIN_HI)
    put(px, 28, 39, B_LOIN_HI)
    put(px, 32, 39, B_LOIN_HI)
    put(px, 22, 41, B_LOIN_DK)
    put(px, 35, 41, B_LOIN_DK)

    # LEGS (short, bent)
    # Left leg
    put_block(px, 23, 43, 4, 8, B_SKIN_BASE)
    for y in range(43, 51):
        put(px, 22, y, B_OUTLINE)
        put(px, 27, y, B_OUTLINE)
    for x in range(22, 28):
        put(px, x, 51, B_OUTLINE)
    # Right leg
    put_block(px, 31, 43, 4, 8, B_SKIN_BASE)
    for y in range(43, 51):
        put(px, 30, y, B_OUTLINE)
        put(px, 35, y, B_OUTLINE)
    for x in range(30, 36):
        put(px, x, 51, B_OUTLINE)

    # FEET (dark, splayed)
    put_block(px, 21, 50, 7, 2, B_LOIN_DK)
    put_block(px, 29, 50, 7, 2, B_LOIN_DK)

    # ARMS (with club in right hand)
    # Left arm hangs down
    put_block(px, 19, 30, 3, 8, B_SKIN_BASE)
    for y in range(30, 38):
        put(px, 18, y, B_OUTLINE)
    for x in range(18, 22):
        put(px, x, 38, B_OUTLINE)
    # Right arm holding club (raised slightly)
    put_block(px, 37, 28, 3, 6, B_SKIN_BASE)
    for x in range(37, 40):
        put(px, x, 27, B_OUTLINE)
    for y in range(28, 34):
        put(px, 40, y, B_OUTLINE)
    # CLUB in right hand (vertical knobby weapon)
    # Club shaft
    put_block(px, 42, 22, 3, 14, B_CLUB_BASE)
    for y in range(22, 36):
        put(px, 41, y, B_OUTLINE)
        put(px, 45, y, B_OUTLINE)
    for x in range(42, 45):
        put(px, x, 21, B_OUTLINE)
    # Club head (knobby top)
    put_block(px, 40, 17, 7, 5, B_CLUB_DK)
    for x in range(40, 47):
        put(px, x, 16, B_OUTLINE)
        put(px, x, 22, B_OUTLINE)
    for y in range(17, 22):
        put(px, 39, y, B_OUTLINE)
        put(px, 47, y, B_OUTLINE)
    # Club spikes
    put(px, 38, 19, B_OUTLINE)
    put(px, 48, 19, B_OUTLINE)
    put(px, 43, 14, B_OUTLINE)
    put(px, 43, 15, B_CLUB_DK)
    return img


# ===========================================================
# OPTION C — 3 GOBLIN SPECIES VARIANTS
# Hound (existing creature, kept), Warrior (humanoid+shield),
# Shaman (humanoid+staff+robe)
# ===========================================================

def option_c_hound():
    # Same as Option A — the existing creature becomes the "Hound" species
    return option_a_polished()


def option_c_warrior():
    """Goblin Warrior — humanoid with iron shield + sword instead of club."""
    img = option_b_humanoid()
    px = img.load()
    # Overpaint the right arm's club with a sword
    # Erase club area (40-48, 14-36)
    for x in range(38, 49):
        for y in range(14, 37):
            if px[x, y] != TRANS:
                # Only erase non-skin pixels
                pass
    # Easier: build a fresh canvas with body but different weapon
    img = make_canvas()
    px = img.load()
    # Re-render the humanoid base
    img2 = option_b_humanoid()
    px2 = img2.load()
    # Copy everything except the club area
    for x in range(CANVAS):
        for y in range(CANVAS):
            if 38 <= x <= 49 and 14 <= y <= 36:
                continue
            put(px, x, y, px2[x, y] if px2[x, y][3] > 0 else None)

    # Add IRON SWORD (vertical, narrow, grey blade)
    BLADE_DK = ( 60,  60,  72, 255)
    BLADE_BASE = (140, 140, 160, 255)
    BLADE_HI = (220, 220, 240, 255)
    HILT = ( 90,  60,  20, 255)
    # Sword blade
    for y in range(14, 32):
        put(px, 42, y, BLADE_DK)
        put(px, 43, y, BLADE_BASE)
        put(px, 44, y, BLADE_HI if y < 22 else BLADE_BASE)
    # Tip
    put(px, 43, 13, BLADE_DK)
    # Cross-guard
    put_block(px, 40, 32, 7, 2, HILT)
    for x in range(40, 47):
        put(px, x, 34, B_OUTLINE)
    # Grip
    put_block(px, 42, 34, 3, 3, HILT)
    put(px, 43, 37, B_OUTLINE)
    # Pommel
    put(px, 43, 38, HILT)
    # Outline
    for y in range(13, 32):
        put(px, 41, y, B_OUTLINE)
        put(px, 45, y, B_OUTLINE)

    # Add SHIELD in left arm position (round wooden shield)
    SHIELD_DK = ( 70,  44,  20, 255)
    SHIELD_BASE = (130,  90,  50, 255)
    SHIELD_RIM = (180, 180, 200, 255)
    # Shield on left side of body — overlapping the left arm
    # Round shield centered at (15, 32)
    cx, cy = 15, 32
    for x in range(CANVAS):
        for y in range(CANVAS):
            dx, dy = x - cx, y - cy
            d2 = dx * dx + dy * dy
            if d2 <= 25:
                put(px, x, y, SHIELD_BASE)
            elif d2 <= 36:
                put(px, x, y, SHIELD_DK)
            elif d2 <= 49:
                put(px, x, y, B_OUTLINE)
    # Shield boss (metal stud center)
    put_block(px, 14, 31, 3, 3, SHIELD_RIM)
    put(px, 15, 32, BLADE_HI)
    return img


def option_c_shaman():
    """Goblin Shaman — humanoid in robe with staff and feathered headdress."""
    img = make_canvas()
    px = img.load()
    ROBE_DK   = ( 30,  20,  60, 255)
    ROBE_BASE = ( 60,  44, 120, 255)
    ROBE_HI   = (110,  80, 180, 255)
    FEATHER_R = (220,  60,  60, 255)
    FEATHER_W = (240, 230, 200, 255)
    BONE      = (240, 220, 180, 255)
    STAFF_DK  = ( 70,  44,  20, 255)
    STAFF_BASE= (130,  90,  50, 255)
    SKULL_W   = (220, 220, 200, 255)

    # HEAD (same green humanoid base)
    put_block(px, 24, 14, 14, 14, B_SKIN_BASE)
    for x in range(23, 39):
        put(px, x, 13, B_OUTLINE); put(px, x, 28, B_OUTLINE)
    for y in range(14, 28):
        put(px, 23, y, B_OUTLINE); put(px, 38, y, B_OUTLINE)
    # Ears
    for y in [17, 18, 19]:
        put(px, 22, y, B_SKIN_BASE); put(px, 21, y, B_OUTLINE)
        put(px, 39, y, B_SKIN_BASE); put(px, 40, y, B_OUTLINE)
    # Big nose
    put_block(px, 38, 19, 4, 4, B_SKIN_DK)
    for x in range(38, 42):
        put(px, x, 18, B_OUTLINE); put(px, x, 23, B_OUTLINE)
    put(px, 42, 19, B_OUTLINE); put(px, 42, 20, B_OUTLINE)
    put(px, 42, 21, B_OUTLINE); put(px, 42, 22, B_OUTLINE)
    # Glowing eyes (mystical purple-white)
    put(px, 28, 18, FEATHER_W); put(px, 28, 19, ROBE_HI)
    put(px, 32, 18, FEATHER_W); put(px, 32, 19, ROBE_HI)
    for x in range(27, 34):
        put(px, x, 17, B_OUTLINE)
    # Teeth
    put(px, 30, 24, B_TOOTH); put(px, 32, 24, B_TOOTH)
    for x in range(27, 35):
        put(px, x, 25, B_OUTLINE)

    # FEATHERED HEADDRESS — band across forehead with 3 feathers rising
    put_block(px, 23, 12, 16, 2, ROBE_DK)
    # 3 feathers (red + white tipped)
    feather_xs = [25, 31, 36]
    for fx in feather_xs:
        # 5-pixel tall feather
        put(px, fx, 8, FEATHER_W)
        put(px, fx, 9, FEATHER_R)
        put(px, fx, 10, FEATHER_R)
        put(px, fx, 11, FEATHER_R)
        put(px, fx - 1, 10, FEATHER_R)
        put(px, fx + 1, 10, FEATHER_R)
        put(px, fx, 7, B_OUTLINE)

    # ROBE (covers body + legs, billowing)
    # Body section
    put_block(px, 22, 28, 16, 22, ROBE_BASE)
    for x in range(21, 39):
        put(px, x, 28, B_OUTLINE)
        put(px, x, 51, B_OUTLINE)
    for y in range(29, 51):
        put(px, 21, y, B_OUTLINE)
        put(px, 39, y, B_OUTLINE)
    # Robe shading — vertical bands
    for x in [24, 28, 32, 36]:
        for y in range(29, 50):
            put(px, x, y, ROBE_DK)
    # Robe highlight on left side
    for y in range(29, 49):
        put(px, 22, y, ROBE_HI)
    # Bottom hem ragged
    for x in [22, 25, 27, 30, 33, 36, 38]:
        put(px, x, 51, ROBE_DK)
        put(px, x, 52, B_OUTLINE)

    # STAFF (left side, taller than goblin)
    # Staff shaft
    for y in range(2, 50):
        put(px, 15, y, STAFF_BASE)
        put(px, 16, y, STAFF_DK)
        put(px, 14, y, B_OUTLINE)
        put(px, 17, y, B_OUTLINE)
    # Staff top — small skull
    # Skull cranium
    put_block(px, 11, 0, 9, 6, SKULL_W)
    for x in range(11, 20):
        put(px, x, -1 if False else 0, B_OUTLINE)
    # Outline
    for x in range(11, 20):
        put(px, x, 6, B_OUTLINE)
    for y in range(0, 6):
        put(px, 10, y, B_OUTLINE)
        put(px, 20, y, B_OUTLINE)
    # Eye sockets
    put(px, 13, 3, B_OUTLINE)
    put(px, 14, 3, B_OUTLINE)
    put(px, 16, 3, B_OUTLINE)
    put(px, 17, 3, B_OUTLINE)
    # Teeth grooves
    put(px, 13, 5, B_OUTLINE)
    put(px, 15, 5, B_OUTLINE)
    put(px, 17, 5, B_OUTLINE)

    return img


# ===========================================================
# Driver
# ===========================================================
OUTPUTS = [
    ("option_a_polished",   option_a_polished),
    ("option_b_humanoid",   option_b_humanoid),
    ("option_c_hound",      option_c_hound),
    ("option_c_warrior",    option_c_warrior),
    ("option_c_shaman",     option_c_shaman),
]

if __name__ == "__main__":
    out = "/home/sparky/ogrs/art/npcs/goblin_options"
    os.makedirs(out, exist_ok=True)
    for name, fn in OUTPUTS:
        img = fn()
        img.save(f"{out}/{name}.png")
        img.resize((CANVAS * 6, CANVAS * 6), Image.NEAREST).save(f"{out}/{name}_x6.png")
        print(f"done: {name}")
