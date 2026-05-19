#!/usr/bin/env python3
"""
Procedural MAGIC projectile — Water / Ice spells.
Ice crystal silhouette (diamond core + diagonal shards) so it reads
distinct from the ORB at native 30×30. Cool palette only — warm tones
are reserved for the (future) FIRE split.
"""
import math
from PIL import Image

W = H = 30
CX, CY = 14, 14

TRANSPARENT     = (0, 0, 0, 0)
CORE_PEAK       = (255, 255, 255, 255)
CORE_HIGHLIGHT  = (224, 245, 255, 255)  # E0F5FF
CORE_BASE       = (168, 222, 255, 255)  # A8DEFF
CORE_SHADE      = ( 91, 168, 229, 255)  # 5BA8E5
HALO_BRIGHT     = (186, 214, 238, 255)  # BAD6EE
HALO_DIM        = (110, 140, 170, 255)  # 6E8CAA
SHARD_BRIGHT    = (255, 255, 255, 255)
SHARD_MID       = (186, 214, 238, 255)
SHARD_DIM       = ( 74, 102, 128, 255)


def in_bounds(x, y):
    return 0 <= x < W and 0 <= y < H


def put(px, x, y, color):
    if in_bounds(x, y):
        px[x, y] = color


def diamond_distance(x, y, cx, cy):
    """Manhattan distance — gives a diamond silhouette."""
    return abs(x - cx) + abs(y - cy)


def draw_core(px, peak=False, scale=1.0):
    """Diamond crystal core with 3 value bands."""
    r_peak = int(round(0 * scale))   # single bright center pixel
    r_high = int(round(2 * scale))
    r_base = int(round(4 * scale))
    r_shade = int(round(5 * scale))
    for x in range(W):
        for y in range(H):
            d = diamond_distance(x, y, CX, CY)
            if d <= r_peak:
                px[x, y] = CORE_PEAK if peak else CORE_HIGHLIGHT
            elif d <= r_high:
                px[x, y] = CORE_HIGHLIGHT
            elif d <= r_base:
                px[x, y] = CORE_BASE
            elif d <= r_shade:
                px[x, y] = CORE_SHADE


def draw_halo(px, intensity=1.0, expanded=False):
    """Thin diamond ring around the core, slightly squared off."""
    r_inner = 6
    r_outer = 7 if expanded else 6
    for x in range(W):
        for y in range(H):
            d = diamond_distance(x, y, CX, CY)
            if r_inner < d <= r_outer + 1:
                if intensity >= 1.0:
                    px[x, y] = HALO_BRIGHT
                elif intensity >= 0.5:
                    if (x + y) % 2 == 0:
                        px[x, y] = HALO_BRIGHT
                    else:
                        px[x, y] = HALO_DIM
                else:
                    if (x + y) % 2 == 0:
                        px[x, y] = HALO_DIM


def draw_shards(px, length, with_outer_specks=False):
    """4 diagonal shards at the corners of the diamond."""
    # Diagonals: NE, NW, SE, SW
    dirs = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
    start = 6  # outside the core
    for dx, dy in dirs:
        for step in range(length):
            r = start + step
            x = CX + dx * r
            y = CY + dy * r
            # Color by position along shard
            if step <= 1:
                color = SHARD_BRIGHT
            elif step <= length - 2:
                color = SHARD_MID
            else:
                color = SHARD_DIM
            put(px, x, y, color)
            # 1-px shoulder for chunkiness
            if step <= 1:
                put(px, x - dx, y, SHARD_MID)
                put(px, x, y - dy, SHARD_MID)

    if with_outer_specks:
        # Frost specks at the cardinal points (peak frame visual flourish)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            r = start + length + 1
            put(px, CX + dx * r, CY + dy * r, SHARD_BRIGHT)


def draw_frame(scale, peak, halo, halo_expanded, shard_len, frost_specks):
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    px = img.load()
    draw_core(px, peak=peak, scale=scale)
    draw_halo(px, intensity=halo, expanded=halo_expanded)
    draw_shards(px, length=shard_len, with_outer_specks=frost_specks)
    return img


frames = [
    # (scale, peak, halo, halo_expanded, shard_len, frost_specks)
    (1.00, False, 0.4, False, 3, False),   # frame_00 — base
    (1.05, False, 0.7, False, 4, False),   # frame_01 — extending
    (1.10,  True, 1.0,  True, 5,  True),   # frame_02 — PEAK
    (1.00, False, 0.4, False, 3, False),   # frame_03 — retracted
]

base = "/home/sparky/ogrs/art/projectiles/1_magic/frames"
import os
os.makedirs(base, exist_ok=True)
for i, args in enumerate(frames):
    img = draw_frame(*args)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print(f"frame_{i:02d}: scale={args[0]} peak={args[1]} halo={args[2]} shard_len={args[4]}")
print("done")
