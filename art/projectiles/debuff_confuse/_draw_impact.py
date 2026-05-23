#!/usr/bin/env python3
"""
CONFUSE radial impact — 48×48, 4 frames.
Purple aura grows from impact point with floating '?' glyphs orbiting
the target silhouette at peak. Dissipates with lingering question marks.
"""
import os, math
from PIL import Image

W = H = 48
CX, CY = 24, 24
TRANS = (0, 0, 0, 0)

P_DEEP   = ( 58,  26,  96, 255)
P_MID    = (106,  58, 160, 255)
P_BRIGHT = (176, 128, 224, 255)
P_HIGH   = (232, 204, 255, 255)
P_GLOW   = (255, 240, 255, 255)
WHITE    = (255, 255, 255, 255)
SPECK    = (220, 180, 255, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


Q_GLYPH = [
    ".##.",
    "#..#",
    "...#",
    "..#.",
    "..#.",
    "....",
    "..#.",
]


def draw_question(px, cx, cy, bright=False):
    color = WHITE if bright else P_HIGH
    shadow = P_DEEP
    h = len(Q_GLYPH)
    w = len(Q_GLYPH[0])
    for row, line in enumerate(Q_GLYPH):
        for col, ch in enumerate(line):
            if ch != "#":
                continue
            x = cx + col - w // 2
            y = cy + row - h // 2
            put(px, x + 1, y + 1, shadow)
    for row, line in enumerate(Q_GLYPH):
        for col, ch in enumerate(line):
            if ch != "#":
                continue
            x = cx + col - w // 2
            y = cy + row - h // 2
            put(px, x, y, color)


def draw_aura(px, radius_sq, intensity=1.0):
    for x in range(W):
        for y in range(H):
            dx, dy = x - CX, y - CY
            d2 = dx * dx + dy * dy
            if d2 <= radius_sq:
                if d2 <= radius_sq * 0.10:
                    put(px, x, y, P_HIGH if intensity > 0.7 else P_BRIGHT)
                elif d2 <= radius_sq * 0.35:
                    put(px, x, y, P_BRIGHT)
                elif d2 <= radius_sq * 0.65:
                    put(px, x, y, P_MID)
                elif d2 <= radius_sq * 0.90:
                    put(px, x, y, P_DEEP)
                else:
                    if (x + y) % 2 == 0:
                        put(px, x, y, P_DEEP)


def draw_orbiting_specks(px, frame, count=8, radius=14):
    """Bright purple specks orbiting the target."""
    offset = frame * 24
    for i in range(count):
        ang = math.radians(i * (360 / count) + offset)
        x = CX + int(round(math.cos(ang) * radius))
        y = CY + int(round(math.sin(ang) * radius))
        put(px, x, y, P_BRIGHT)


def draw_questions_orbit(px, frame, count, radius):
    """Place '?' glyphs orbiting the target silhouette."""
    offset = frame * 30
    for i in range(count):
        ang = math.radians(i * (360 / count) + offset)
        qx = CX + int(round(math.cos(ang) * radius))
        qy = CY + int(round(math.sin(ang) * radius))
        draw_question(px, qx, qy, bright=(frame == 2))


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    if frame == 0:
        draw_aura(px, radius_sq=36)
        draw_question(px, CX, CY, bright=False)
    elif frame == 1:
        draw_aura(px, radius_sq=140)
        draw_orbiting_specks(px, frame, count=6, radius=10)
        draw_question(px, CX, CY, bright=False)
        draw_question(px, CX + 12, CY - 6, bright=False)
    elif frame == 2:
        # PEAK — full aura + 4 ?s orbiting + bright center
        draw_aura(px, radius_sq=350, intensity=1.0)
        draw_orbiting_specks(px, frame, count=10, radius=18)
        draw_questions_orbit(px, frame, count=4, radius=14)
        # Big bright center ?
        draw_question(px, CX, CY, bright=True)
    elif frame == 3:
        # Dissipating — fewer specks, fading aura
        draw_aura(px, radius_sq=180)
        draw_orbiting_specks(px, frame, count=6, radius=16)
        draw_question(px, CX, CY, bright=False)
        draw_question(px, CX - 11, CY + 8, bright=False)
    return img


if __name__ == "__main__":
    base = "/home/sparky/ogrs/art/projectiles/debuff_confuse/impact"
    os.makedirs(base, exist_ok=True)
    for i in range(4):
        img = draw_frame(i)
        img.save(f"{base}/frame_{i:02d}.png")
        img.resize((W * 6, H * 6), Image.NEAREST).save(f"{base}/frame_{i:02d}_x6.png")
    print("done")
