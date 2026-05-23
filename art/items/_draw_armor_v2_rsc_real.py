#!/usr/bin/env python3
"""
Armor v2 — uses REAL RSC base templates + pictureMask tint.

Replaces my earlier Phase 12-15 templates (which were custom-drawn).
Now we extract the actual RSC armor sprites from the cache, apply each
tier's official pictureMask as a multiplicative tint, then add masterwork
overlays (gem, trim, glow) on top.

Native sprite sizes preserved per slot — the RSC template dictates dimensions.
"""
import struct, zipfile, os
from PIL import Image

ARCHIVE = "/home/sparky/ogrs/client/Cache/video/Authentic_Sprites.orsc"
OUT = "/home/sparky/ogrs/art/items/armor_v2"
os.makedirs(OUT, exist_ok=True)


def decode_sprite(data):
    """Decode an .orsc sprite blob (25-byte header + RGBA ints)."""
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


# Pull armor templates from the cache once
ARMOR_TEMPLATES_SID = {
    'platebody':     2158,   # items:8
    'platelegs':     2159,   # items:9
    'medium_helm':   2155,   # items:5
    'large_helm':    2156,   # items:6
    'chainmail':     2157,   # items:7
    'kite_shield':   2152,   # items:2
    'square_shield': 2153,   # items:3
}

templates = {}
with zipfile.ZipFile(ARCHIVE) as z:
    for name, sid in ARMOR_TEMPLATES_SID.items():
        try:
            data = z.read(str(sid))
            templates[name] = decode_sprite(data)
        except KeyError:
            print(f"missing template {name} at sprite {sid}")


# Per-tier pictureMask (decoded from EntityHandler.java)
TIERS = {
    'bronze':  0xFF7F19,   # 16737817 — orange
    'iron':    0xEEDDDD,   # 15654365 — light grey
    'steel':   0xEEEEEE,   # 15658734 — silver
    'black':   0x303030,   # 3158064  — black
    'mithril': 0x99AACC,   # 10072780 — blue-grey
    'adamant': 0xB2D499,   # 11717785 — green
    'rune':    0x00FFFF,   # 65535    — cyan
}


def apply_tint(template_img, mask_int):
    """Apply pictureMask as a multiplicative tint to the template.

    The engine's blend treats the mask as a color multiplier:
        out_rgb = template_rgb * mask_rgb / 255
    This preserves the lightness pattern of the template while shifting hue.
    """
    mask_r = (mask_int >> 16) & 0xFF
    mask_g = (mask_int >> 8) & 0xFF
    mask_b = mask_int & 0xFF
    out = template_img.copy()
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] == 0:
                continue
            nr = (p[0] * mask_r) // 255
            ng = (p[1] * mask_g) // 255
            nb = (p[2] * mask_b) // 255
            px[x, y] = (nr, ng, nb, p[3])
    return out


# ===========================================================
# MASTERWORK OVERLAYS — gem + trim + glow added to tinted template
# ===========================================================

def add_mw_overlays(img, gem_color, glow_color=None, trim_pixels=None, etching_pixels=None):
    """Layer masterwork features on top of the tinted template.

    - gem_color: 3×3 gem block at sprite center
    - glow_color: dithered halo behind sprite
    - trim_pixels: list of (x, y) for trim/etching overlays
    - etching_pixels: list of (x, y) for rune-etch markings"""
    w, h = img.size
    cx, cy = w // 2, h // 2

    # Glow halo (drawn on a new layer behind)
    if glow_color:
        new = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        new_px = new.load()
        for x in range(w):
            for y in range(h):
                dx, dy = x - cx, y - cy
                d2 = dx * dx + dy * dy
                # Halo just outside the sprite silhouette
                if (w * h) // 6 < d2 <= (w * h) // 3:
                    if (x + y) % 2 == 0:
                        new_px[x, y] = glow_color
        # Composite: glow behind, then img on top
        new.alpha_composite(img)
        img = new

    px = img.load()

    # Trim accent
    if trim_pixels:
        for tx, ty in trim_pixels:
            if 0 <= tx < w and 0 <= ty < h:
                if px[tx, ty][3] > 0:   # only on opaque areas
                    px[tx, ty] = (255, 220, 100, 255) if not trim_pixels else trim_pixels[0] if isinstance(trim_pixels[0], tuple) and len(trim_pixels[0]) == 4 else (255, 220, 100, 255)
                else:
                    pass

    # Etching markings
    if etching_pixels:
        for tx, ty, ec in etching_pixels:
            if 0 <= tx < w and 0 <= ty < h:
                if px[tx, ty][3] > 0:
                    px[tx, ty] = ec

    # Central gem
    if gem_color:
        gem_cells = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),           (1, 0),
            (-1, 1),  (0, 1),  (1, 1),
        ]
        for dx, dy in gem_cells:
            x = cx + dx; y = cy + dy
            if 0 <= x < w and 0 <= y < h:
                px[x, y] = gem_color
        # Bright center pixel
        if 0 <= cx < w and 0 <= cy < h:
            px[cx, cy] = (255, 255, 255, 255)

    return img


# Masterwork config per tier
MW_CONFIGS = {
    'bronze':  {'gem': (220,  30,  30, 255), 'glow': (255, 200, 100,  90)},
    'iron':    {'gem': (240, 180,  40, 255), 'glow': (230, 200, 130,  80)},
    'steel':   {'gem': ( 30, 100, 220, 255), 'glow': (130, 180, 255,  90)},
    'black':   {'gem': (140,   0, 200, 255), 'glow': (180,  40,  60, 110)},
    'mithril': {'gem': (240, 240, 255, 255), 'glow': (160, 200, 255, 110)},
    'adamant': {'gem': ( 40, 220, 100, 255), 'glow': (100, 220, 130, 110)},
    'rune':    {'gem': (200,  60, 220, 255), 'glow': (180, 220, 255, 130)},
}


# ===========================================================
# DRIVER
# ===========================================================
if __name__ == "__main__":
    SLOTS = ['platebody', 'platelegs', 'large_helm', 'kite_shield', 'medium_helm', 'chainmail', 'square_shield']
    for slot in SLOTS:
        template = templates.get(slot)
        if template is None:
            print(f"skip {slot}: missing template")
            continue
        for tier_name, mask_int in TIERS.items():
            # Vanilla tier
            tinted = apply_tint(template, mask_int)
            base_name = f"{slot}_{tier_name}"
            tinted.save(f"{OUT}/{base_name}.png")
            tinted.resize((template.size[0] * 8, template.size[1] * 8), Image.NEAREST).save(f"{OUT}/{base_name}_x8.png")
            # Masterwork variant
            cfg = MW_CONFIGS[tier_name]
            mw = add_mw_overlays(tinted.copy(), gem_color=cfg['gem'], glow_color=cfg['glow'])
            mw_name = f"{slot}_{tier_name}_mw"
            mw.save(f"{OUT}/{mw_name}.png")
            mw.resize((mw.size[0] * 8, mw.size[1] * 8), Image.NEAREST).save(f"{OUT}/{mw_name}_x8.png")
            print(f"done: {base_name} + {mw_name}")
    print(f"\n=== Armor v2 complete: {len(SLOTS) * len(TIERS) * 2} sprites ===")
