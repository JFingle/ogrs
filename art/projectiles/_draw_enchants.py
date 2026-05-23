#!/usr/bin/env python3
"""
5 enchant-amulet tier spells — escalating sparkle intensity per tier.
Each 30×30 4-frame. Tiers go from a single faint blue speck (LVL1) to
a full white-hot corona (LVL5). At a glance you can tell which tier
was cast by the *scale* of the effect.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def sparkle(px, x, y, peak_color, mid_color, dim_color, big=False):
    """5-pixel cross sparkle; if big, 9-pixel cross."""
    put(px, x, y, peak_color)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        put(px, x + dx, y + dy, mid_color)
    if big:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            put(px, x + dx, y + dy, dim_color)


def beam(px, x0, y0, x1, y1, color):
    """Straight line beam of one color."""
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        put(px, x0, y0, color)
        return
    for i in range(steps + 1):
        x = x0 + dx * i // steps
        y = y0 + dy * i // steps
        put(px, x, y, color)


# Per-tier configuration
TIERS = {
    1: dict(
        peak=(220, 235, 255, 255),
        mid=(160, 200, 240, 255),
        dim=( 80, 130, 200, 255),
        sparkle_count=[1, 1, 2, 1],
        sparkle_size=False,
        beam_count=0,
        corona=False,
    ),
    2: dict(
        peak=(180, 230, 255, 255),
        mid=(100, 180, 240, 255),
        dim=( 40, 110, 200, 255),
        sparkle_count=[1, 2, 3, 2],
        sparkle_size=False,
        beam_count=0,
        corona=False,
    ),
    3: dict(
        peak=(255, 245, 180, 255),
        mid=(255, 200,  80, 255),
        dim=(200, 130,  40, 255),
        sparkle_count=[2, 3, 5, 3],
        sparkle_size=True,
        beam_count=4,
        corona=False,
    ),
    4: dict(
        peak=(240, 210, 255, 255),
        mid=(180, 130, 230, 255),
        dim=(100,  60, 180, 255),
        sparkle_count=[2, 4, 6, 4],
        sparkle_size=True,
        beam_count=6,
        corona=True,
    ),
    5: dict(
        peak=(255, 255, 255, 255),
        mid=(255, 240, 200, 255),
        dim=(220, 190,  80, 255),
        sparkle_count=[3, 5, 8, 5],
        sparkle_size=True,
        beam_count=8,
        corona=True,
    ),
}


def draw_tier(tier, frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    config = TIERS[tier]
    peak_c = config['peak']
    mid_c = config['mid']
    dim_c = config['dim']

    # Center sparkle — always present, scales with tier and frame
    center_size = config['sparkle_size'] and (frame >= 1)
    sparkle(px, CX, CY, peak_c, mid_c, dim_c, big=center_size)

    # Tier 4+5: extra big center on peak frame
    if frame == 2 and tier >= 4:
        for dx, dy in [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]:
            put(px, CX + dx, CY + dy, mid_c)

    # Surrounding sparkles, positions deterministic per frame
    sparkle_positions = {
        0: [(7, 6), (21, 8)],
        1: [(7, 6), (21, 8), (8, 22), (22, 22)],
        2: [(7, 6), (21, 8), (8, 22), (22, 22), (14, 3), (3, 14), (25, 14), (14, 25)],
        3: [(8, 7), (20, 7), (7, 21), (21, 21)],
    }
    n_sparkles = config['sparkle_count'][frame]
    for i in range(min(n_sparkles, len(sparkle_positions[frame]))):
        x, y = sparkle_positions[frame][i]
        sparkle(px, x, y, peak_c, mid_c, dim_c, big=False)

    # Beams radiating outward (tier 3+)
    if config['beam_count'] > 0 and frame >= 1:
        beam_count = config['beam_count']
        beam_length = 11 if frame == 2 else 9
        for i in range(beam_count):
            ang = math.radians(i * (360 / beam_count) + frame * 8)
            x1 = CX + int(round(math.cos(ang) * beam_length))
            y1 = CY + int(round(math.sin(ang) * beam_length))
            # Beam from outer edge inward; brightest at outer tip
            for step in range(3):
                bx = CX + int(round(math.cos(ang) * (beam_length - step)))
                by = CY + int(round(math.sin(ang) * (beam_length - step)))
                color = peak_c if step == 0 else (mid_c if step == 1 else dim_c)
                put(px, bx, by, color)

    # Full corona (tier 4+5)
    if config['corona'] and frame == 2:
        for ang_deg in range(0, 360, 15):
            ang = math.radians(ang_deg)
            r = 13
            x = CX + int(round(math.cos(ang) * r))
            y = CY + int(round(math.sin(ang) * r))
            put(px, x, y, dim_c)

    return img


if __name__ == "__main__":
    for tier in (1, 2, 3, 4, 5):
        folder = f"enchant_lvl{tier}"
        out = f"/home/sparky/ogrs/art/projectiles/{folder}/frames"
        os.makedirs(out, exist_ok=True)
        for i in range(4):
            img = draw_tier(tier, i)
            img.save(f"{out}/frame_{i:02d}.png")
            img.resize((W * 8, H * 8), Image.NEAREST).save(f"{out}/frame_{i:02d}_x8.png")
        print(f"done: {folder}")
