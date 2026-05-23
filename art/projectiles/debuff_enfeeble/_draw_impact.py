#!/usr/bin/env python3
"""
ENFEEBLE impact effect — 48×48, 4 frames.
Toxic cloud explodes outward from impact point and wraps the target
silhouette before dissipating. Frame arc: spawn → expand → peak →
dissipate. A faint hole in the middle of the peak frame implies the
target standing there.
"""
import os, math
from PIL import Image

W = H = 48
CX, CY = 24, 24
TRANS = (0, 0, 0, 0)

SICK_DEEP    = ( 42,  46,  12, 255)
SICK_BASE    = ( 80,  78,  28, 255)
SICK_MID     = (140, 132,  64, 255)
SICK_PALE    = (188, 180,  96, 255)
SICK_HIGH    = (228, 220, 140, 255)
SICK_GLOW    = (255, 245, 180, 255)
TOXIC_BRIGHT = (170, 200,  80, 255)
TOXIC_DIM    = ( 88, 112,  40, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def stable_hash(x, y, salt=0):
    v = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    return (v & 0xFFFF) / 0xFFFF


def cloud_density(x, y, frame, radius, noise_intensity=0.5):
    """0..1 cloud thickness. radius controls the cloud falloff distance."""
    dx, dy = x - CX, y - CY
    d_ellip = math.sqrt((dx / 1.1) ** 2 + (dy / 0.95) ** 2)
    base = max(0, 1 - d_ellip / radius)
    noise = stable_hash(x + frame * 3, y - frame * 2, salt=frame * 11)
    return base * (1 - noise_intensity + noise_intensity * 2 * noise)


# Target silhouette — a rough humanoid where the cloud SHOULDN'T be solid.
# This creates the "wrapping around the model" feel at peak frames.
def in_target_silhouette(x, y):
    dx, dy = x - CX, y - CY
    # Head (above center)
    if abs(dx) <= 3 and -14 <= dy <= -9:
        return True
    # Torso
    if abs(dx) <= 4 and -8 <= dy <= 2:
        return True
    # Legs
    if abs(dx) <= 2 and 3 <= dy <= 12:
        return True
    # Arms (slight)
    if -7 <= dx <= -5 and -6 <= dy <= 2:
        return True
    if 5 <= dx <= 7 and -6 <= dy <= 2:
        return True
    return False


def draw_cloud(px, frame, radius, peak=False, dim_silhouette=False):
    """Layered cloud — uses radius to scale size for the impact frames."""
    bands = [
        (0.10, SICK_DEEP),
        (0.25, SICK_BASE),
        (0.45, SICK_MID),
        (0.65, SICK_PALE),
        (0.82, SICK_HIGH),
    ]
    if peak:
        bands.append((0.92, SICK_GLOW))
    for x in range(W):
        for y in range(H):
            d = cloud_density(x, y, frame, radius)
            # When wrapping target: cloud is thinner over the target silhouette
            if dim_silhouette and in_target_silhouette(x, y):
                d *= 0.4
            for thresh, color in reversed(bands):
                if d > thresh:
                    put(px, x, y, color)
                    break


def draw_tendrils(px, frame, length, count=6):
    """Wispy tendrils radiating outward."""
    angle_offset = frame * 12
    for i in range(count):
        base = i * (360 / count)
        ang = math.radians(base + angle_offset)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        for step in range(length - 4, length):
            r = step
            # Curve via small sin variation
            wave = math.sin(step / 2.5 + frame) * 0.4
            x = CX + int(round((cos_a + wave * sin_a) * r))
            y = CY + int(round((sin_a - wave * cos_a) * r))
            color = SICK_PALE if step <= length - 2 else SICK_BASE
            put(px, x, y, color)


def draw_rising_wisps(px, frame):
    """Bright toxic specks drifting upward — late-frame visual."""
    if frame == 3:
        for x, y in [(20, 6), (28, 8), (22, 10), (26, 5), (24, 7), (30, 12)]:
            put(px, x, y, TOXIC_BRIGHT)
        for x, y in [(18, 4), (32, 4), (24, 2)]:
            put(px, x, y, TOXIC_DIM)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        # Just landed — small dense core
        draw_cloud(px, frame, radius=8, peak=False)
        draw_tendrils(px, frame, length=10, count=4)
    elif frame == 1:
        # Expanding
        draw_cloud(px, frame, radius=14, peak=False)
        draw_tendrils(px, frame, length=16, count=6)
    elif frame == 2:
        # Peak — wraps target
        draw_cloud(px, frame, radius=22, peak=True, dim_silhouette=True)
        draw_tendrils(px, frame, length=22, count=8)
    elif frame == 3:
        # Dissipating — cloud shrinking, wisps rising
        draw_cloud(px, frame, radius=12, peak=False)
        draw_rising_wisps(px, frame)
    return img



if __name__ == "__main__":

    base = "/home/sparky/ogrs/art/projectiles/debuff_enfeeble/impact"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
