#!/usr/bin/env python3
"""
CONFUSE debuff — disorientation magic.
A big '?' glyph as the visual anchor, surrounded by a swirling purple aura.
The '?' tilts/wiggles per frame to suggest dizziness.
"""
import os, math
from PIL import Image

W = H = 30
CX, CY = 14, 14
TRANS = (0, 0, 0, 0)

P_DEEP   = ( 58,  26,  96, 255)
P_MID    = (106,  58, 160, 255)
P_BRIGHT = (176, 128, 224, 255)
P_HIGH   = (232, 204, 255, 255)
GLYPH    = (255, 255, 255, 255)
GLYPH_SH = (180, 140, 230, 255)
SPECK    = (220, 180, 255, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# 7×9 question-mark glyph, stored as ASCII art ('#' = lit, '.' = empty).
# Drawn at the visual center of the sprite.
Q_GLYPH = [
    ".#####.",
    "##...##",
    ".#...##",
    "....##.",
    "...##..",
    "...#...",
    ".......",
    "...#...",
    "...#...",
]


def draw_question(px, cx, cy, tilt=0, color=GLYPH, shadow=GLYPH_SH):
    """Place the '?' glyph centered at (cx, cy). tilt is a per-row x-offset for wobble."""
    h = len(Q_GLYPH)
    w = len(Q_GLYPH[0])
    for row, line in enumerate(Q_GLYPH):
        # Add a small wave to the x offset for tilt (each row shifts horizontally)
        wave = int(round(math.sin((row / h) * math.pi) * tilt))
        for col, ch in enumerate(line):
            if ch != "#":
                continue
            x = cx + col - w // 2 + wave
            y = cy + row - h // 2
            # 1-px shadow underneath / right
            put(px, x + 1, y + 1, shadow)
    # then the main glyph on top
    for row, line in enumerate(Q_GLYPH):
        wave = int(round(math.sin((row / h) * math.pi) * tilt))
        for col, ch in enumerate(line):
            if ch != "#":
                continue
            x = cx + col - w // 2 + wave
            y = cy + row - h // 2
            put(px, x, y, color)


def draw_aura(px, rotation_deg, intensity):
    """Soft purple aura rotating around the glyph — abstract swirl, not literal lines."""
    # Outer ring of dim purple
    for ang_deg in range(0, 360, 18):
        ang = math.radians(ang_deg + rotation_deg)
        r = 12
        x = CX + int(round(math.cos(ang) * r))
        y = CY + int(round(math.sin(ang) * r))
        put(px, x, y, P_DEEP if intensity < 0.8 else P_MID)
    # Mid ring — only at certain angles
    for ang_deg in range(0, 360, 36):
        ang = math.radians(ang_deg + rotation_deg)
        r = 10
        x = CX + int(round(math.cos(ang) * r))
        y = CY + int(round(math.sin(ang) * r))
        put(px, x, y, P_MID)
    # 3 bright sparks
    for ang_deg in (0, 120, 240):
        ang = math.radians(ang_deg + rotation_deg * 1.5)
        r = 9
        x = CX + int(round(math.cos(ang) * r))
        y = CY + int(round(math.sin(ang) * r))
        put(px, x, y, P_BRIGHT if intensity >= 0.8 else P_MID)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    rotation = frame * 22
    intensity = [0.7, 0.85, 1.0, 0.85][frame]
    tilt = [0, 1, 0, -1][frame]  # gentle wobble
    draw_aura(px, rotation, intensity)
    draw_question(px, CX, CY, tilt=tilt,
                  color=GLYPH if frame == 2 else P_HIGH,
                  shadow=P_DEEP)
    return img


base = "/home/sparky/ogrs/art/projectiles/debuff_confuse/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
print("done")
