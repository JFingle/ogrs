"""All 5 berry bushes board: 5 rows × 6 states."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/BUSHES_BOARD.png"

CELL = 200
PAD = 10
LABEL_W = 200
TITLE_H = 64
COL_HEADER_H = 56

ROWS = [
    ("Redberry",   "redberry",   "olive leaves / red berries"),
    ("Dwellberry", "dwellberry", "darker olive / blue-grey berries"),
    ("Janger",     "janger",     "olive + bright accent / green berries"),
    ("Cadava",     "cadava",     "sinister dark / magenta berries (poison)"),
    ("Whiteberry", "whiteberry", "mistletoe olive-tan / cream berries"),
]

STATES = [
    ("1_sapling",        "Sapling"),
    ("2_young",          "Young"),
    ("3_mature_empty",   "Empty"),
    ("4_mature_partial", "Partial"),
    ("5_mature_full",    "FULL"),
    ("6_dead",           "Dead"),
]

W = LABEL_W + len(STATES) * (CELL + PAD) + PAD
H = TITLE_H + COL_HEADER_H + len(ROWS) * (CELL + PAD) + PAD

img = Image.new("RGB", (W, H), (24, 22, 32))
draw = ImageDraw.Draw(img)

try:
    font_lbl   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    font_col   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except Exception:
    font_lbl = font_sub = font_col = font_title = ImageFont.load_default()

draw.text((PAD, 18), "OGRS Berry Bushes — 5 types × 6 states (RSC palette)",
          fill=(255, 255, 255), font=font_title)

for ci, (key, head) in enumerate(STATES):
    x = LABEL_W + PAD + ci * (CELL + PAD)
    y = TITLE_H
    bbox = draw.textbbox((0, 0), head, font=font_col)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + 12), head, fill=(255, 240, 180), font=font_col)

for ri, (row_label, prefix, palette) in enumerate(ROWS):
    y = TITLE_H + COL_HEADER_H + ri * (CELL + PAD)
    draw.rectangle([(0, y), (LABEL_W - PAD, y + CELL)], fill=(45, 42, 55))
    draw.text((10, y + 16), row_label, fill=(255, 255, 255), font=font_lbl)
    # Palette descriptor wrapped
    words = palette.split(" ")
    line = ""; line_y = y + 48
    for w in words:
        test = (line + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font_sub)
        if bbox[2] - bbox[0] > LABEL_W - 24:
            draw.text((10, line_y), line, fill=(170, 170, 200), font=font_sub)
            line = w; line_y += 18
        else:
            line = test
    if line:
        draw.text((10, line_y), line, fill=(170, 170, 200), font=font_sub)

    for ci, (key, head) in enumerate(STATES):
        x = LABEL_W + PAD + ci * (CELL + PAD)
        bg = (55, 70, 50) if "full" in key else ((40, 35, 50) if "dead" in key else (50, 50, 60))
        draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
        src = f"{RENDER_DIR}/bush_{prefix}_{key}.png"
        if os.path.exists(src):
            sp = Image.open(src).convert("RGBA")
            if sp.size != (CELL, CELL):
                sp = sp.resize((CELL, CELL), Image.LANCZOS)
            img.paste(sp, (x, y), sp)

img.save(OUT)
print(f"Board: {OUT}  size={img.size}")

windows_dir = "/mnt/c/OGRS_Art/models/farming/bushes"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/BUSHES_BOARD.png")
print(f"Synced: {windows_dir}/BUSHES_BOARD.png")
