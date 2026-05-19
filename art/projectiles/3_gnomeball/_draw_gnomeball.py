#!/usr/bin/env python3
"""
Procedural GNOMEBALL projectile — Claws of Guthix + utility spells.
Mossy green orb with 4 leaf-petal lobes rotating around it. Round core
silhouette (like ORB) but distinguished by hue + chunky petals (vs ORB's
long thin wind streaks).
"""
import math, os
from PIL import Image

W = H = 30
CX, CY = 14, 14

TRANS         = (0, 0, 0, 0)
CORE_PEAK     = (255, 255, 255, 255)
CORE_HI       = (232, 245, 192, 255)  # E8F5C0
CORE_BASE     = (168, 208,  96, 255)  # A8D060
CORE_SHADE    = ( 90, 138,  40, 255)  # 5A8A28
HALO_BRIGHT   = (197, 229, 160, 255)  # C5E5A0
HALO_DIM      = (122, 160,  80, 255)  # 7AA050
PETAL_BRIGHT  = (232, 245, 192, 255)
PETAL_BASE    = (168, 208,  96, 255)
PETAL_SHADE   = ( 58,  88,  24, 255)  # 3A5818


def in_bounds(x, y):
    return 0 <= x < W and 0 <= y < H


def put(px, x, y, c):
    if c is not None and in_bounds(x, y):
        px[x, y] = c


def draw_core(px, peak=False):
    """Round green orb with 3 value bands."""
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                put(px, x, y, CORE_PEAK if peak else CORE_HI)
            elif d2 <= 4:
                put(px, x, y, CORE_HI)
            elif d2 <= 10:
                put(px, x, y, CORE_BASE)
            elif d2 <= 16:
                put(px, x, y, CORE_SHADE)


def draw_halo(px, intensity=1.0, expand=False):
    """Soft chartreuse ring just outside the core."""
    r_inner_sq = 16
    r_outer_sq = 30 if expand else 25
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if r_inner_sq < d2 <= r_outer_sq:
                if intensity >= 1.0:
                    put(px, x, y, HALO_BRIGHT)
                elif intensity >= 0.5:
                    put(px, x, y, HALO_BRIGHT if (x + y) % 2 == 0 else HALO_DIM)
                else:
                    if (x + y) % 2 == 0:
                        put(px, x, y, HALO_DIM)


def draw_petal(px, cx, cy, dx_dir, dy_dir):
    """Draws a small 3-wide × 2-tall leaf lobe with directional shading.
    dx_dir, dy_dir are the outward direction vectors (-1, 0, 1)."""
    # Petal "body" is a 2×2 cluster offset outward by (dx_dir, dy_dir) one step.
    # Then a single bright pixel on the outermost cell of the petal in the outward direction.
    # Shoulders perpendicular to the outward vector.
    # 1) main body (2×2)
    bx, by = cx + dx_dir, cy + dy_dir
    # Use the "tangent" direction to spread the petal sideways
    tx, ty = -dy_dir, dx_dir
    body_cells = [
        (bx, by, PETAL_BASE),
        (bx + tx, by + ty, PETAL_BASE),
        (bx + dx_dir, by + dy_dir, PETAL_BRIGHT),
        (bx + dx_dir + tx, by + dy_dir + ty, PETAL_BASE),
    ]
    for x, y, c in body_cells:
        put(px, x, y, c)
    # 2) tip (outermost pixel) — bright highlight
    put(px, bx + 2 * dx_dir, by + 2 * dy_dir, PETAL_BRIGHT)
    # 3) shadow pixel underneath the petal
    put(px, bx - tx, by - ty, PETAL_SHADE)


def draw_petals(px, rotation_step):
    """Place 4 petals at evenly-spaced angles, rotated rotation_step × 22.5°."""
    # rotation_step is 0,1,2,3
    base_angles = [0, 90, 180, 270]
    angle_offset = rotation_step * 22.5
    for base in base_angles:
        angle = math.radians(base + angle_offset)
        # Place petal at radius 5 from center (just outside the core)
        r = 5
        cx = CX + int(round(math.cos(angle) * r))
        cy = CY + int(round(math.sin(angle) * r))
        # Direction vector pointing outward (normalized to nearest -1/0/+1)
        dx_dir = int(round(math.cos(angle)))
        dy_dir = int(round(math.sin(angle)))
        if dx_dir == 0 and dy_dir == 0:
            continue
        draw_petal(px, cx, cy, dx_dir, dy_dir)


def draw_frame(rotation_step, peak, halo_intensity, halo_expand):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    draw_core(px, peak=peak)
    draw_halo(px, intensity=halo_intensity, expand=halo_expand)
    draw_petals(px, rotation_step)
    return img


frames = [
    # (rotation_step, peak, halo_intensity, halo_expand)
    (0, False, 0.4, False),
    (1, False, 0.7, False),
    (2,  True, 1.0,  True),
    (3, False, 0.4, False),
]

base = "/home/sparky/ogrs/art/projectiles/3_gnomeball/frames"
os.makedirs(base, exist_ok=True)
for i, args in enumerate(frames):
    img = draw_frame(*args)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
    print(f"frame_{i:02d}: rot_step={args[0]} peak={args[1]} halo={args[2]}")
print("done")
