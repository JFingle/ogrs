#!/usr/bin/env python3
"""
Armor v3 — context-aware masterwork ornaments.

Each slot gets its own ornament map (where gem/trim/studs/plume go) based
on the actual silhouette of the template, not geometric center.

Improvements over v2:
  - Platebody: gem on CHEST (not center), trim across upper-chest + waist bands, pauldron studs on shoulders
  - Platelegs: gem on BELT BUCKLE (existing accent), trim along belt, knee studs on each leg
  - Large Helm: gem on FOREHEAD, crown spike on top, trim around the visor edge
  - Kite Shield: gem on the cross intersection (boss), 4 corner studs at rim
"""
import struct, zipfile, os
from PIL import Image

ARCHIVE = "/home/sparky/ogrs/client/Cache/video/Authentic_Sprites.orsc"
OUT = "/home/sparky/ogrs/art/items/armor_v3"
os.makedirs(OUT, exist_ok=True)


def decode_sprite(data):
    if len(data) < 25: return None
    w, h = struct.unpack(">II", data[0:8])
    if w * h * 4 + 25 > len(data) + 100: return None
    expected = 25 + w * h * 4
    if len(data) < expected: return None
    pixels = struct.unpack(f">{w*h}I", data[25:expected])
    img = Image.new("RGBA", (w, h))
    for i, p in enumerate(pixels):
        if p == 0:
            img.putpixel((i % w, i // w), (0, 0, 0, 0))
        else:
            r = (p >> 16) & 0xFF; g = (p >> 8) & 0xFF; b = p & 0xFF
            img.putpixel((i % w, i // w), (r, g, b, 255))
    return img


# Templates
ARMOR_TEMPLATES_SID = {
    'platebody':   2158, 'platelegs':  2159,
    'large_helm':  2156, 'kite_shield': 2152,
}
templates = {}
with zipfile.ZipFile(ARCHIVE) as z:
    for name, sid in ARMOR_TEMPLATES_SID.items():
        templates[name] = decode_sprite(z.read(str(sid)))


# Real pictureMask values from EntityHandler.java
TIERS = {
    'bronze':  0xFF7F19, 'iron':    0xEEDDDD, 'steel':   0xEEEEEE,
    'black':   0x303030, 'mithril': 0x99AACC, 'adamant': 0xB2D499,
    'rune':    0x00FFFF,
}


def apply_tint(img, mask_int):
    """Multiplicative tint: out = template * mask / 255."""
    mr = (mask_int >> 16) & 0xFF; mg = (mask_int >> 8) & 0xFF; mb = mask_int & 0xFF
    out = img.copy()
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] == 0: continue
            px[x, y] = ((p[0] * mr) // 255, (p[1] * mg) // 255, (p[2] * mb) // 255, p[3])
    return out


def put_on_opaque(px, w, h, x, y, color):
    """Paint pixel only if the underlying template pixel is opaque."""
    if 0 <= x < w and 0 <= y < h:
        if px[x, y][3] > 0:
            px[x, y] = color


# ===========================================================
# Per-slot ornament definitions (manually placed per template)
# ===========================================================

# Each ornament spec defines per-pixel positions
SLOT_ORNAMENTS = {
    'platebody': {
        'gem_center': (16, 13),     # chest center, below the existing emblem
        'trim_rows': [(7, 7, 30), (22, 7, 30)],   # (y, x_start, x_end) — upper chest + waist bands
        'studs': [(7, 6), (26, 6)],   # shoulder pauldron studs
        'plume': None,
        'glow_center': (16, 14),
    },
    'platelegs': {
        'gem_center': (40, 1),       # belt buckle (uses existing right-side belt)
        'trim_rows': [(2, 8, 36)],   # belt line across hips
        'studs': [(12, 14), (34, 14)],  # knee studs
        'plume': None,
        'glow_center': (23, 10),
    },
    'large_helm': {
        'gem_center': (17, 3),        # forehead
        'trim_rows': [(7, 10, 24), (11, 10, 24)],   # visor edge top + bottom
        'studs': [],
        'plume': (17, 0),             # crown spike at top
        'glow_center': (16, 8),
    },
    'kite_shield': {
        'gem_center': (20, 12),       # cross intersection / boss
        'trim_rows': [],              # cross is already prominent — no extra trim
        'studs': [(5, 5), (35, 5), (10, 20), (30, 20)],  # 4 corner rim studs
        'plume': None,
        'glow_center': (20, 13),
    },
}


def add_mw_overlays(img, slot_name, gem_color, glow_color, trim_color, plume_color=None):
    """Apply slot-specific masterwork overlays."""
    w, h = img.size
    ornaments = SLOT_ORNAMENTS[slot_name]

    # === Glow halo (drawn behind, then composite img on top) ===
    if glow_color:
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gpx = glow.load()
        gcx, gcy = ornaments['glow_center']
        # Halo just outside the silhouette
        for x in range(w):
            for y in range(h):
                dx, dy = x - gcx, y - gcy
                d2 = dx * dx + dy * dy
                inner = (w * h) // 6
                outer = (w * h) // 3
                if inner < d2 <= outer and (x + y) % 2 == 0:
                    if img.load()[x, y][3] == 0:   # only outside silhouette
                        gpx[x, y] = glow_color
        glow.alpha_composite(img)
        img = glow

    px = img.load()

    # === Trim bands across the silhouette ===
    if trim_color:
        for y, x_start, x_end in ornaments['trim_rows']:
            for x in range(x_start, x_end + 1):
                put_on_opaque(px, w, h, x, y, trim_color)

    # === Studs (small bright dots) ===
    stud_color = (255, 255, 255, 255)
    for sx, sy in ornaments['studs']:
        put_on_opaque(px, w, h, sx, sy, stud_color)
        # Surround stud with trim color for emphasis
        if trim_color:
            put_on_opaque(px, w, h, sx - 1, sy, trim_color)
            put_on_opaque(px, w, h, sx + 1, sy, trim_color)

    # === Plume on top (helmets only) ===
    if plume_color and ornaments['plume']:
        px_pos, py_pos = ornaments['plume']
        # 3-pixel-tall plume above the helm
        for dy in (-1, -2):
            put(px, w, h, px_pos, py_pos + dy, plume_color)

    # === Central gem (the highlight ornament) ===
    if gem_color:
        gcx, gcy = ornaments['gem_center']
        gem_cells = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),  (1, 0),
            (-1, 1),  (0, 1),  (1, 1),
        ]
        for dx, dy in gem_cells:
            put_on_opaque(px, w, h, gcx + dx, gcy + dy, gem_color)
        # Bright center
        if 0 <= gcx < w and 0 <= gcy < h and px[gcx, gcy][3] > 0:
            px[gcx, gcy] = (255, 255, 255, 255)

    return img


def put(px, w, h, x, y, c):
    """Unconditional pixel put (used for plume which goes above silhouette)."""
    if 0 <= x < w and 0 <= y < h:
        px[x, y] = c


# Per-tier MW config
MW_CONFIGS = {
    'bronze':  {'gem': (220,  30,  30, 255), 'glow': (255, 200, 100,  90), 'trim': (255, 220, 100, 255), 'plume': (220,  60,  60, 255)},
    'iron':    {'gem': (240, 180,  40, 255), 'glow': (230, 200, 130,  80), 'trim': (200, 160,  60, 255), 'plume': (220,  60,  60, 255)},
    'steel':   {'gem': ( 30, 100, 220, 255), 'glow': (130, 180, 255,  90), 'trim': (220, 230, 250, 255), 'plume': (220,  60,  60, 255)},
    'black':   {'gem': (180,   0, 220, 255), 'glow': (180,  40,  60, 110), 'trim': (220,  40,  60, 255), 'plume': (180,  20,  20, 255)},
    'mithril': {'gem': (240, 240, 255, 255), 'glow': (160, 200, 255, 110), 'trim': (220, 230, 250, 255), 'plume': (220, 220, 240, 255)},
    'adamant': {'gem': ( 40, 220, 100, 255), 'glow': (100, 220, 130, 110), 'trim': (255, 220, 100, 255), 'plume': (180, 220, 100, 255)},
    'rune':    {'gem': (220,  60, 220, 255), 'glow': (180, 220, 255, 130), 'trim': (255, 255, 255, 255), 'plume': (180, 220, 255, 255)},
}


if __name__ == "__main__":
    SLOTS = ['platebody', 'platelegs', 'large_helm', 'kite_shield']
    for slot in SLOTS:
        template = templates.get(slot)
        if template is None:
            continue
        w, h = template.size
        for tier_name, mask_int in TIERS.items():
            # Vanilla
            tinted = apply_tint(template, mask_int)
            base = f"{slot}_{tier_name}"
            tinted.save(f"{OUT}/{base}.png")
            tinted.resize((w * 8, h * 8), Image.NEAREST).save(f"{OUT}/{base}_x8.png")
            # Masterwork
            cfg = MW_CONFIGS[tier_name]
            mw = add_mw_overlays(
                tinted.copy(), slot,
                gem_color=cfg['gem'], glow_color=cfg['glow'],
                trim_color=cfg['trim'], plume_color=cfg['plume'],
            )
            mw_name = f"{base}_mw"
            mw.save(f"{OUT}/{mw_name}.png")
            mw.resize((mw.size[0] * 8, mw.size[1] * 8), Image.NEAREST).save(f"{OUT}/{mw_name}_x8.png")
            print(f"done: {base} + {mw_name}")
    print(f"\n=== Armor v3 complete ===")
