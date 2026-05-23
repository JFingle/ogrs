"""Trees board: 6 trees (rows) × 6 states (cols)."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/TREES_BOARD.png"

CELL = 200
PAD = 10
LABEL_W = 180
TITLE_H = 70
COL_HEADER_H = 60

ROWS = [
    ("Apple",      "trees_apple"),
    ("Lemon",      "trees_lemon"),
    ("Lime",       "trees_lime"),
    ("Orange",     "trees_orange"),
    ("Grapefruit", "trees_grapefruit"),
    ("Banana",     "trees_banana"),
]

COL_LABELS = [
    ("1_sapling",        "Sapling",          "exhausted @ 25%"),
    ("2_young",          "Young Tree",       "exhausted @ 55%"),
    ("3_mature_empty",   "Mature (Empty)",   "exhausted (post-harvest)"),
    ("4_mature_partial", "Mature (Partial)", "~40% fruit kept"),
    ("5_mature_full",    "Mature (Full)",    "vanilla — harvest ready"),
    ("6_stump",          "Stump",            "vanilla treestump (chop)"),
]

W = LABEL_W + len(COL_LABELS) * (CELL + PAD) + PAD
H = TITLE_H + COL_HEADER_H + len(ROWS) * (CELL + PAD) + PAD

img = Image.new("RGB", (W, H), (24, 22, 32))
draw = ImageDraw.Draw(img)

try:
    font_lbl   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_col   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except Exception:
    font_lbl = font_sub = font_col = font_title = ImageFont.load_default()

draw.text((PAD, 18), "OGRS Fruit Trees 3D — 6 states per tree (derived from vanilla RSC geometry)",
          fill=(255, 255, 255), font=font_title)

# Column headers
for ci, (key, head, sub) in enumerate(COL_LABELS):
    x = LABEL_W + PAD + ci * (CELL + PAD)
    y = TITLE_H
    # Header label
    bbox = draw.textbbox((0, 0), head, font=font_col)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + 4), head, fill=(255, 240, 180), font=font_col)
    # Subtext
    bbox = draw.textbbox((0, 0), sub, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + 30), sub, fill=(170, 170, 200), font=font_sub)

# Rows
for ri, (row_label, prefix) in enumerate(ROWS):
    y = TITLE_H + COL_HEADER_H + ri * (CELL + PAD)
    draw.rectangle([(0, y), (LABEL_W - PAD, y + CELL)], fill=(45, 42, 55))
    bbox = draw.textbbox((0, 0), row_label, font=font_lbl)
    th = bbox[3] - bbox[1]
    draw.text((10, y + (CELL - th) // 2 - 4), row_label, fill=(255, 255, 255), font=font_lbl)
    for ci, (key, head, sub) in enumerate(COL_LABELS):
        x = LABEL_W + PAD + ci * (CELL + PAD)
        # Highlight Mature (Full) — the canonical "harvest ready"
        bg = (55, 70, 50) if "full" in key else ((40, 35, 50) if "stump" in key else (50, 50, 60))
        draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
        src = f"{RENDER_DIR}/{prefix}_{key}.png"
        if os.path.exists(src):
            sp = Image.open(src).convert("RGBA")
            if sp.size != (CELL, CELL):
                sp = sp.resize((CELL, CELL), Image.LANCZOS)
            img.paste(sp, (x, y), sp)

img.save(OUT)
print(f"Board: {OUT}  size={img.size}")

# Sync
windows_dir = "/mnt/c/OGRS_Art/models/farming/trees"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/TREES_BOARD.png")

# Sync per-tree folders
trees_src = "/home/sparky/ogrs/art/models/farming/trees"
for row_label, prefix in ROWS:
    name = prefix.replace("trees_", "")
    src_dir = f"{trees_src}/{name}"
    if not os.path.isdir(src_dir):
        continue
    dst_dir = f"{windows_dir}/{name}"
    os.makedirs(dst_dir, exist_ok=True)
    for fname in os.listdir(src_dir):
        if fname.endswith((".obj", ".mtl")):
            shutil.copy(f"{src_dir}/{fname}", f"{dst_dir}/{fname}")
print(f"Synced to: {windows_dir}")
