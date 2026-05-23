#!/usr/bin/env python3
"""
WEAKEN debuff — saps target strength.
A drooping olive-grey droplet trailing downward. Color reads 'lifeless /
drained.' Frame cycle shows the droplet sagging then snapping back.
Distinct from Enfeeble (which is a misty cloud, not a droplet).
"""
import os
from PIL import Image

W = H = 30
CX = 14
TRANS = (0, 0, 0, 0)

OUTLINE   = ( 42,  45,  20, 255)
DEEP      = ( 74,  80,  40, 255)
BASE      = (107, 116,  56, 255)
MID       = (139, 144,  80, 255)
PALE      = (168, 176, 112, 255)
HIGH      = (192, 196, 144, 255)
DRIP      = ( 90,  98,  50, 255)


def put(px, x, y, c):
    if c is not None and 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# Droplet shape — vertical teardrop with rounded top, pointed bottom.
# Defined as ASCII art across rows, with center column at index 4 (width 9).
DROPLET = [
    "...###...",   # row 0 — top arc
    "..#####..",
    ".#######.",
    "#########",
    "#########",
    "#########",
    ".#######.",
    "..#####..",
    "...###...",
    "....#....",   # row 9 — drip starts
]

# Color shading map keyed by position relative to droplet center.
# Uses outline / deep / base / mid / pale / high.
def shade_for(col, row, w, h):
    # Outline at the outermost lit cell of each row
    cx = w // 2
    # Highlight upper-left interior
    if 2 <= row <= 4 and 3 <= col <= 4:
        return HIGH
    if 1 <= row <= 5 and 2 <= col <= 5:
        return PALE
    if 0 <= row <= 7 and 1 <= col <= 7:
        return MID
    if 1 <= row <= 7 and 1 <= col <= 7:
        return BASE
    return DEEP


def draw_droplet(px, y_offset, stretch=False):
    """Draw the droplet centered horizontally, shifted vertically by y_offset.
    If stretch=True, extend an extra-tall body before the drip."""
    body = DROPLET[:]
    if stretch:
        # Insert one extra-tall row
        body = body[:7] + ["..#####..", "..#####..", "...###..."] + body[7:]
    w = len(body[0])
    for row, line in enumerate(body):
        for col, ch in enumerate(line):
            if ch != "#":
                continue
            x = CX + col - w // 2
            y = 6 + row + y_offset
            # First decide if this is an outline pixel (edge of row).
            # An outline cell is the leftmost/rightmost '#' in its row.
            row_first = line.find("#")
            row_last = line.rfind("#")
            if col in (row_first, row_last):
                put(px, x, y, OUTLINE)
            else:
                put(px, x, y, shade_for(col, row, w, len(body)))


def draw_drip(px, y_base, length):
    """A single-column vertical drip extending below the droplet."""
    for dy in range(length):
        y = y_base + dy
        if dy < length - 1:
            put(px, CX, y, DRIP)
        else:
            put(px, CX, y, DEEP)


def draw_down_chevron(px, y_top):
    """Small downward-pointing chevron under the drip — indicates 'sapping'."""
    rows = [
        (CX - 2, y_top, DEEP),
        (CX + 2, y_top, DEEP),
        (CX - 1, y_top + 1, OUTLINE),
        (CX + 1, y_top + 1, OUTLINE),
        (CX,     y_top + 2, OUTLINE),
    ]
    for x, y, c in rows:
        put(px, x, y, c)


def draw_frame(frame):
    img = Image.new("RGBA", (W, H), TRANS)
    px = img.load()
    # frame 0: base droplet, short drip
    # frame 1: droplet sagging (stretched), longer drip
    # frame 2: peak sag (max stretch) + chevron arrow appears
    # frame 3: snap back to base
    if frame == 0:
        draw_droplet(px, y_offset=0, stretch=False)
        draw_drip(px, y_base=15, length=2)
    elif frame == 1:
        draw_droplet(px, y_offset=0, stretch=True)
        draw_drip(px, y_base=18, length=3)
    elif frame == 2:
        draw_droplet(px, y_offset=0, stretch=True)
        draw_drip(px, y_base=18, length=4)
        draw_down_chevron(px, 24)
    elif frame == 3:
        draw_droplet(px, y_offset=0, stretch=False)
        draw_drip(px, y_base=15, length=1)
    return img


base = "/home/sparky/ogrs/art/projectiles/debuff_weaken/frames"
os.makedirs(base, exist_ok=True)
for i in range(4):
    img = draw_frame(i)
    img.save(f"{base}/frame_{i:02d}.png")
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"{base}/frame_{i:02d}_x8.png")
print("done")
