#!/usr/bin/env python3
"""
Combat-spell radial impacts — 48×48, 4 frames each.
For the 6 router projectile sprites that fly through the air and splash
on the target: ORB, MAGIC, GNOMEBALL, SKULL, SPIKEBALL, FIRE.

Each impact is element-themed: ORB=gold sparkle, MAGIC=ice shatter,
GNOMEBALL=leaf scatter, SKULL=death wisps, SPIKEBALL=dirt clods,
FIRE=flame splash.

All share the same 4-frame arc:
  0 spawn → 1 expand → 2 peak wraps target → 3 dissipate.
"""
import os, math
from PIL import Image

W = H = 48
CX, CY = 24, 24
TRANS = (0, 0, 0, 0)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def stable_hash(x, y, salt=0):
    v = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    return (v & 0xFFFF) / 0xFFFF


# Target silhouette for the "wrap" effect at peak.
def in_silhouette(x, y):
    dx, dy = x - CX, y - CY
    if abs(dx) <= 3 and -14 <= dy <= -9: return True
    if abs(dx) <= 4 and -8 <= dy <= 2: return True
    if abs(dx) <= 2 and 3 <= dy <= 12: return True
    if -7 <= dx <= -5 and -6 <= dy <= 2: return True
    if 5 <= dx <= 7 and -6 <= dy <= 2: return True
    return False


def radial_filled_disc(px, palette, radius, peak=False, dim_silhouette=False, dither_outer=True):
    """Build a layered radial impact. palette is dict[band_threshold -> color]."""
    bands_sorted = sorted(palette.items(), key=lambda kv: kv[0])
    r2 = radius * radius
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 > r2:
                continue
            t = d2 / r2   # 0 at center, 1 at edge
            if dim_silhouette and in_silhouette(x, y):
                t = min(1.0, t * 2.0)  # body area appears dimmer / further from "core"
            # Outer dither for soft falloff
            if dither_outer and t > 0.85 and (x + y) % 2 == 1:
                continue
            # Pick band: largest threshold ≤ t gets the color
            color = None
            for thresh, c in bands_sorted:
                if t <= thresh:
                    color = c
                    break
            if color:
                put(px, x, y, color)


def particles(px, frame, specs):
    """Place specks per frame. specs is dict[frame -> list of (x,y,color)]."""
    for x, y, c in specs.get(frame, []):
        put(px, x, y, c)


# ===========================================================
# ORB impact — gold/holy sparkle burst
# ===========================================================
ORB_BANDS = {
    "0": (0.05, (255, 255, 255, 255)),  # center white
    "1": (0.25, (255, 247, 208, 255)),
    "2": (0.55, (245, 230, 160, 255)),
    "3": (0.85, (217, 194, 104, 255)),
    "4": (1.00, (140, 122,  68, 255)),
}

def orb_palette():
    return {v[0]: v[1] for v in ORB_BANDS.values()}

def draw_orb_radial(px, radius, peak=False):
    radial_filled_disc(px, orb_palette(), radius, peak=peak, dim_silhouette=peak)

def draw_orb_streaks(px, frame, length=12, count=8):
    """White wind streaks radiating outward."""
    offset = frame * 18
    for i in range(count):
        ang = math.radians(i * (360 / count) + offset)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        for step in range(length - 3, length):
            x = CX + int(round(cos_a * step))
            y = CY + int(round(sin_a * step))
            color = (255, 255, 255, 255) if step <= length - 2 else (200, 200, 220, 255)
            put(px, x, y, color)

def orb_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        draw_orb_radial(px, radius=6)
    elif frame == 1:
        draw_orb_radial(px, radius=14)
        draw_orb_streaks(px, frame, length=10, count=6)
    elif frame == 2:
        draw_orb_radial(px, radius=22, peak=True)
        draw_orb_streaks(px, frame, length=18, count=10)
    elif frame == 3:
        draw_orb_radial(px, radius=10)
        # Lingering sparkles
        for ang_deg in range(0, 360, 45):
            r = 16
            ang = math.radians(ang_deg + frame * 10)
            x = CX + int(round(math.cos(ang) * r))
            y = CY + int(round(math.sin(ang) * r))
            put(px, x, y, (255, 247, 208, 255))
    return img


# ===========================================================
# MAGIC impact — ice shatter, blue shards burst outward
# ===========================================================
MAGIC_BANDS = {
    "0": (0.05, (255, 255, 255, 255)),
    "1": (0.25, (224, 245, 255, 255)),
    "2": (0.55, (168, 222, 255, 255)),
    "3": (0.85, ( 91, 168, 229, 255)),
    "4": (1.00, ( 54, 102, 144, 255)),
}
def magic_palette():
    return {v[0]: v[1] for v in MAGIC_BANDS.values()}

def draw_magic_shards(px, frame, count=8, length=14):
    """Diamond-shaped ice shards radiating outward."""
    offset = frame * 22.5
    for i in range(count):
        ang = math.radians(i * (360 / count) + offset)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        for step in range(length - 4, length):
            x = CX + int(round(cos_a * step))
            y = CY + int(round(sin_a * step))
            color = (224, 245, 255, 255) if step <= length - 2 else (91, 168, 229, 255)
            put(px, x, y, color)
        # Tip — bright white
        tip = length
        x = CX + int(round(cos_a * tip))
        y = CY + int(round(sin_a * tip))
        put(px, x, y, (255, 255, 255, 255))

def magic_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        radial_filled_disc(px, magic_palette(), radius=6)
    elif frame == 1:
        radial_filled_disc(px, magic_palette(), radius=14)
        draw_magic_shards(px, frame, count=6, length=12)
    elif frame == 2:
        radial_filled_disc(px, magic_palette(), radius=20, peak=True, dim_silhouette=True)
        draw_magic_shards(px, frame, count=8, length=18)
        draw_magic_shards(px, frame, count=8, length=12)
    elif frame == 3:
        radial_filled_disc(px, magic_palette(), radius=10)
        # Lingering ice specks falling
        for x, y in [(10, 22), (38, 26), (16, 36), (32, 32), (24, 4)]:
            put(px, x, y, (168, 222, 255, 255))
    return img


# ===========================================================
# GNOMEBALL impact — green leaf scatter
# ===========================================================
GNOME_BANDS = {
    "0": (0.05, (255, 255, 255, 255)),
    "1": (0.25, (232, 245, 192, 255)),
    "2": (0.55, (168, 208,  96, 255)),
    "3": (0.85, ( 90, 138,  40, 255)),
    "4": (1.00, ( 58,  88,  24, 255)),
}
def gnome_palette():
    return {v[0]: v[1] for v in GNOME_BANDS.values()}

def draw_petal(px, cx, cy, dx_dir, dy_dir, dim=False):
    color = (90, 138, 40, 255) if dim else (168, 208, 96, 255)
    bright = (232, 245, 192, 255)
    tx, ty = -dy_dir, dx_dir
    bx, by = cx + dx_dir, cy + dy_dir
    put(px, bx, by, color)
    put(px, bx + tx, by + ty, color)
    put(px, bx + dx_dir, by + dy_dir, bright)
    put(px, bx + dx_dir + tx, by + dy_dir + ty, color)

def gnome_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        radial_filled_disc(px, gnome_palette(), radius=6)
    elif frame == 1:
        radial_filled_disc(px, gnome_palette(), radius=14)
        # 4 petals at cardinal
        for ang_deg in (0, 90, 180, 270):
            ang = math.radians(ang_deg)
            x = CX + int(round(math.cos(ang) * 12))
            y = CY + int(round(math.sin(ang) * 12))
            dx = int(round(math.cos(ang)))
            dy = int(round(math.sin(ang)))
            draw_petal(px, x, y, dx, dy)
    elif frame == 2:
        radial_filled_disc(px, gnome_palette(), radius=20, peak=True, dim_silhouette=True)
        # 8 petals at all angles
        for ang_deg in range(0, 360, 45):
            ang = math.radians(ang_deg)
            r = 16
            x = CX + int(round(math.cos(ang) * r))
            y = CY + int(round(math.sin(ang) * r))
            dx = int(round(math.cos(ang) * 1.2))
            dy = int(round(math.sin(ang) * 1.2))
            if dx == 0 and dy == 0:
                continue
            draw_petal(px, x, y, max(-1, min(1, dx)), max(-1, min(1, dy)))
    elif frame == 3:
        radial_filled_disc(px, gnome_palette(), radius=10)
        # Scattered leaf bits
        for x, y in [(8, 12), (40, 16), (10, 36), (38, 34), (24, 4)]:
            put(px, x, y, (168, 208, 96, 255))
    return img


# ===========================================================
# SKULL impact — purple death wisps with red embers
# ===========================================================
SKULL_BANDS = {
    "0": (0.05, (200, 192, 208, 255)),
    "1": (0.25, (144, 128, 160, 255)),
    "2": (0.55, ( 90,  72,  96, 255)),
    "3": (0.85, ( 50,  35,  60, 255)),
    "4": (1.00, ( 26,  16,  32, 255)),
}
def skull_palette():
    return {v[0]: v[1] for v in SKULL_BANDS.values()}

def draw_skull_wisps(px, frame, count=6, length=14):
    """Curving wisps of cursed flame radiating outward."""
    offset = frame * 12
    for i in range(count):
        base = i * (360 / count) + offset
        for step in range(length - 4, length):
            ang = math.radians(base + math.sin(step / 2.0) * 8)
            x = CX + int(round(math.cos(ang) * step))
            y = CY + int(round(math.sin(ang) * step))
            if step <= length - 2:
                color = (192, 48, 31, 255)   # outer flame red
            else:
                color = (80, 16, 32, 255)    # deep crimson
            put(px, x, y, color)

def skull_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        radial_filled_disc(px, skull_palette(), radius=6)
    elif frame == 1:
        radial_filled_disc(px, skull_palette(), radius=14)
        draw_skull_wisps(px, frame, count=4, length=10)
    elif frame == 2:
        radial_filled_disc(px, skull_palette(), radius=20, peak=True, dim_silhouette=True)
        draw_skull_wisps(px, frame, count=8, length=16)
        # Embers
        for x, y in [(12, 8), (36, 10), (8, 36), (40, 34), (24, 4), (24, 44)]:
            put(px, x, y, (255, 128, 48, 255))
    elif frame == 3:
        radial_filled_disc(px, skull_palette(), radius=10)
        # Drifting purple wisps
        for x, y in [(8, 12), (40, 16), (12, 38), (36, 32)]:
            put(px, x, y, (90, 72, 96, 255))
    return img


# ===========================================================
# SPIKEBALL impact — dirt clods + dust cloud
# ===========================================================
SPIKE_BANDS = {
    "0": (0.05, (212, 152, 112, 255)),
    "1": (0.25, (160, 112,  80, 255)),
    "2": (0.55, (107,  69,  32, 255)),
    "3": (0.85, ( 58,  40,  24, 255)),
    "4": (1.00, ( 26,  20,  12, 255)),
}
def spike_palette():
    return {v[0]: v[1] for v in SPIKE_BANDS.values()}

def draw_dirt_clods(px, count, frame):
    """Chunky dirt clods scattered around — irregular 2x2 blocks."""
    base_positions = [
        (6, 8), (38, 10), (8, 38), (40, 36),
        (22, 4), (4, 24), (44, 24), (24, 44),
        (14, 6), (34, 6), (14, 42), (34, 42),
    ]
    moss_positions = [(8, 10), (38, 12), (10, 36), (40, 32)]
    for i, (x, y) in enumerate(base_positions[:count]):
        # Slight per-frame drift
        x += (frame % 2)
        # 2-pixel cluster
        put(px, x, y, (107, 69, 32, 255))
        put(px, x + 1, y, (58, 40, 24, 255))
        put(px, x, y + 1, (160, 112, 80, 255))
    if count >= 8:
        for x, y in moss_positions:
            put(px, x, y, (104, 128, 48, 255))   # moss bits

def spike_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        radial_filled_disc(px, spike_palette(), radius=6)
        draw_dirt_clods(px, count=2, frame=frame)
    elif frame == 1:
        radial_filled_disc(px, spike_palette(), radius=14)
        draw_dirt_clods(px, count=4, frame=frame)
    elif frame == 2:
        radial_filled_disc(px, spike_palette(), radius=20, peak=True, dim_silhouette=True)
        draw_dirt_clods(px, count=12, frame=frame)
    elif frame == 3:
        radial_filled_disc(px, spike_palette(), radius=10)
        draw_dirt_clods(px, count=6, frame=frame)
    return img


# ===========================================================
# FIRE impact — flame splash with embers
# ===========================================================
FIRE_BANDS = {
    "0": (0.05, (255, 255, 255, 255)),
    "1": (0.25, (255, 240, 180, 255)),
    "2": (0.55, (255, 200,  80, 255)),
    "3": (0.85, (255, 120,  40, 255)),
    "4": (1.00, (130,  20,  20, 255)),
}
def fire_palette():
    return {v[0]: v[1] for v in FIRE_BANDS.values()}

def draw_fire_tongues(px, count, length, frame):
    """Flame tongues licking outward — small teardrop shapes."""
    offset = frame * 18
    for i in range(count):
        ang = math.radians(i * (360 / count) + offset)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        for step in range(length - 4, length + 1):
            x = CX + int(round(cos_a * step))
            y = CY + int(round(sin_a * step))
            if step <= length - 3:
                color = (255, 200, 80, 255)
            elif step <= length - 1:
                color = (255, 120, 40, 255)
            else:
                color = (255, 255, 255, 255)
            put(px, x, y, color)

def draw_embers(px, frame):
    sets = {
        2: [(8, 6, (255, 240, 180, 255)), (40, 8, (255, 240, 180, 255)),
            (10, 38, (255, 200, 80, 255)), (38, 36, (255, 200, 80, 255)),
            (24, 4, (255, 255, 255, 255))],
        3: [(6, 4, (255, 200, 80, 255)), (42, 6, (255, 120, 40, 255)),
            (8, 40, (130, 20, 20, 255)), (40, 38, (130, 20, 20, 255))],
    }
    for x, y, c in sets.get(frame, []):
        put(px, x, y, c)

def fire_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        radial_filled_disc(px, fire_palette(), radius=6)
    elif frame == 1:
        radial_filled_disc(px, fire_palette(), radius=14)
        draw_fire_tongues(px, count=6, length=12, frame=frame)
    elif frame == 2:
        radial_filled_disc(px, fire_palette(), radius=20, peak=True, dim_silhouette=True)
        draw_fire_tongues(px, count=8, length=18, frame=frame)
        draw_embers(px, frame)
    elif frame == 3:
        radial_filled_disc(px, fire_palette(), radius=10)
        draw_fire_tongues(px, count=4, length=10, frame=frame)
        draw_embers(px, frame)
    return img


# ===========================================================
# Driver — emit all 6 impacts
# ===========================================================
IMPACTS = [
    ("0_orb",       orb_frame),
    ("1_magic",     magic_frame),
    ("3_gnomeball", gnome_frame),
    ("4_skull",     skull_frame),
    ("5_spikeball", spike_frame),
    ("element_fire", fire_frame),
]

if __name__ == "__main__":
    for folder, frame_fn in IMPACTS:
        out = f"/home/sparky/ogrs/art/projectiles/{folder}/impact"
        os.makedirs(out, exist_ok=True)
        for i in range(4):
            img = frame_fn(i)
            img.save(f"{out}/frame_{i:02d}.png")
            img.resize((W * 6, H * 6), Image.NEAREST).save(f"{out}/frame_{i:02d}_x6.png")
        print(f"done: {folder}")
