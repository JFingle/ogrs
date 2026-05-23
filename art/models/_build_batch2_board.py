"""Batch 2 board: pineapple/dragonfruit/coconut/papaya (6 states each) + herb (4)."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/FARMING_BATCH2_BOARD.png"

CELL = 200
PAD = 10
LABEL_W = 200
TITLE_H = 64
COL_HEADER_H = 56

# Use the larger 6-state column set as the canvas width
STATES_6 = [
    ("1_sapling",        "Sapling"),
    ("2_young",          "Young"),
    ("3_mature_empty",   "Empty"),
    ("4_mature_partial", "Partial"),
    ("5_mature_full",    "FULL"),
    ("6_dead",           "Dead/Stump"),
]
# Herb only has 4 states; we'll align them under columns 2-5
STATES_4 = [
    ("1_seedling",  1),
    ("2_sprouting", 2),
    ("3_growing",   3),
    ("4_mature",    4),
]

ROWS_6 = [
    ("Pineapple",   "v3_pineapple"),
    ("Dragonfruit", "v3_dragonfruit"),
    ("Coconut",     "v3_coconut"),
    ("Papaya",      "v3_papaya"),
]
ROW_HERB = ("Herb", "v3_herb")

ALL_ROWS = ROWS_6 + [ROW_HERB]

W = LABEL_W + len(STATES_6) * (CELL + PAD) + PAD
H = TITLE_H + COL_HEADER_H + len(ALL_ROWS) * (CELL + PAD) + PAD

img = Image.new("RGB", (W, H), (24, 22, 32))
draw = ImageDraw.Draw(img)

try:
    font_lbl   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_col   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except Exception:
    font_lbl = font_col = font_title = ImageFont.load_default()

draw.text((PAD, 18),
          "OGRS Farming Batch 2 — Pineapple, Dragonfruit, Coconut, Papaya, Herb",
          fill=(255, 255, 255), font=font_title)

# Column headers
for ci, (key, head) in enumerate(STATES_6):
    x = LABEL_W + PAD + ci * (CELL + PAD)
    y = TITLE_H
    bbox = draw.textbbox((0, 0), head, font=font_col)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + 12), head, fill=(255, 240, 180), font=font_col)

# 6-state rows
for ri, (row_label, prefix) in enumerate(ROWS_6):
    y = TITLE_H + COL_HEADER_H + ri * (CELL + PAD)
    draw.rectangle([(0, y), (LABEL_W - PAD, y + CELL)], fill=(45, 42, 55))
    draw.text((10, y + (CELL // 2) - 12), row_label, fill=(255, 255, 255), font=font_lbl)
    for ci, (key, head) in enumerate(STATES_6):
        x = LABEL_W + PAD + ci * (CELL + PAD)
        if "full" in key: bg = (55, 70, 50)
        elif "dead" in key or "stump" in key: bg = (40, 35, 50)
        else: bg = (50, 50, 60)
        draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
        # For coconut/papaya, state 6 is "6_stump"; others use "6_dead"
        actual_key = key
        if key == "6_dead" and prefix in ("v3_coconut", "v3_papaya"):
            actual_key = "6_stump"
        src = f"{RENDER_DIR}/{prefix}_{actual_key}.png"
        if os.path.exists(src):
            sp = Image.open(src).convert("RGBA")
            if sp.size != (CELL, CELL):
                sp = sp.resize((CELL, CELL), Image.LANCZOS)
            img.paste(sp, (x, y), sp)

# Herb row (4 states, slotted into columns 2-5 visually)
y = TITLE_H + COL_HEADER_H + len(ROWS_6) * (CELL + PAD)
draw.rectangle([(0, y), (LABEL_W - PAD, y + CELL)], fill=(45, 42, 55))
draw.text((10, y + (CELL // 2) - 12), "Herb", fill=(255, 255, 255), font=font_lbl)
herb_files = ["v3_herb_1_seedling.png", "v3_herb_2_sprouting.png",
              "v3_herb_3_growing.png", "v3_herb_4_mature.png"]
herb_labels = ["Seedling", "Sprouting", "Growing", "Mature"]
# Map 4 cells to columns 1, 2, 3, 4 (skip column 0, leave 5 empty)
for ci, (fname, lbl) in enumerate(zip(herb_files, herb_labels), start=1):
    x = LABEL_W + PAD + ci * (CELL + PAD)
    bg = (55, 70, 50) if "mature" in fname else (50, 50, 60)
    draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
    src = f"{RENDER_DIR}/{fname}"
    if os.path.exists(src):
        sp = Image.open(src).convert("RGBA")
        if sp.size != (CELL, CELL):
            sp = sp.resize((CELL, CELL), Image.LANCZOS)
        img.paste(sp, (x, y), sp)
    # Tiny inline label since herb states don't align with the column headers
    bbox = draw.textbbox((0, 0), lbl, font=font_col)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + CELL - 26), lbl, fill=(220, 220, 230), font=font_col)
# Mark columns 0 and 5 as N/A for herb
for ci in (0, 5):
    x = LABEL_W + PAD + ci * (CELL + PAD)
    draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=(36, 34, 44))
    draw.text((x + 60, y + CELL // 2 - 10), "(n/a)", fill=(120, 120, 140), font=font_col)

img.save(OUT)
print(f"Board: {OUT}  size={img.size}")

# Sync
windows_dir = "/mnt/c/OGRS_Art/models/farming"
shutil.copy(OUT, f"{windows_dir}/FARMING_BATCH2_BOARD.png")
# Per-crop folders
for cfg_name in ("pineapple", "dragonfruit", "coconut", "papaya", "herb"):
    src_dir = f"/home/sparky/ogrs/art/models/farming/{cfg_name}"
    dst_dir = f"{windows_dir}/{cfg_name}"
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.isdir(src_dir):
        for fname in os.listdir(src_dir):
            if fname.endswith((".obj", ".mtl")):
                shutil.copy(f"{src_dir}/{fname}", f"{dst_dir}/{fname}")
print(f"Synced to: {windows_dir}")
