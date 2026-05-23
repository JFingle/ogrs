"""Big board: 7 crops (rows) × 4 stages (cols)."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/FARMING_BOARD.png"

CELL = 200
PAD = 12
LABEL_W = 200
TITLE_H = 70
COL_HEADER_H = 36

# (label, render_name_prefix) — uses prefix + _1..4
ROWS = [
    ("Tomato", "v3_tomato", "fruit color swap (red→green)"),
    ("Corn",   "v3_corn",   "tassel color swap (yellow→husk-tan)"),
    ("Potato", "v3_potato", "scale-only (25/55/85%)"),
    ("Onion",  "v3_onion",  "scale-only (25/55/85%)"),
    ("Garlic", "v3_garlic", "scale-only (25/55/85%)"),
    ("Cabbage (green)", "v3_cabbage_green", "scale-only (25/55/85%)"),
    ("Cabbage (red)",   "v3_cabbage_red",   "scale-only (25/55/85%)"),
]

COL_LABELS = ["Stage 1 — Seedling", "Stage 2 — Growing", "Stage 3 — Ripening", "Stage 4 — Harvest"]

W = LABEL_W + 4 * (CELL + PAD) + PAD
H = TITLE_H + COL_HEADER_H + len(ROWS) * (CELL + PAD) + PAD

img = Image.new("RGB", (W, H), (28, 26, 36))
draw = ImageDraw.Draw(img)

try:
    font_lbl   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    font_col   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except Exception:
    font_lbl = font_sub = font_col = font_title = ImageFont.load_default()

draw.text((PAD, 18), "OGRS Farming 3D — Growth Stages (Batch 1, derived from vanilla RSC geometry)",
          fill=(255, 255, 255), font=font_title)

# Column headers
for ci, col in enumerate(COL_LABELS):
    x = LABEL_W + PAD + ci * (CELL + PAD)
    y = TITLE_H
    bbox = draw.textbbox((0, 0), col, font=font_col)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + 8), col, fill=(255, 240, 180), font=font_col)

# Rows
for ri, (row_label, prefix, technique) in enumerate(ROWS):
    y = TITLE_H + COL_HEADER_H + ri * (CELL + PAD)
    # Row label
    draw.rectangle([(0, y), (LABEL_W - PAD, y + CELL)], fill=(45, 42, 55))
    draw.text((10, y + 16), row_label, fill=(255, 255, 255), font=font_lbl)
    # Technique subtext, wrapped
    tech_words = technique.split(" ")
    line = ""
    line_y = y + 50
    for w in tech_words:
        test = (line + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font_sub)
        if bbox[2] - bbox[0] > LABEL_W - 24:
            draw.text((10, line_y), line, fill=(170, 170, 190), font=font_sub)
            line = w
            line_y += 18
        else:
            line = test
    if line:
        draw.text((10, line_y), line, fill=(170, 170, 190), font=font_sub)

    # Cells
    for ci in range(4):
        x = LABEL_W + PAD + ci * (CELL + PAD)
        # Subtle bg
        bg = (55, 70, 50) if ci == 3 else (50, 50, 60)
        draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
        # The render is 256×256 — fit into CELL
        src = f"{RENDER_DIR}/{prefix}_{ci + 1}.png"
        if os.path.exists(src):
            sp = Image.open(src).convert("RGBA")
            if sp.size != (CELL, CELL):
                sp = sp.resize((CELL, CELL), Image.LANCZOS)
            img.paste(sp, (x, y), sp)

img.save(OUT)
print(f"Board: {OUT}  size={img.size}")

# Sync
windows_dir = "/mnt/c/OGRS_Art/models/farming"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/FARMING_BOARD.png")

# Sync per-crop folders
for cfg in ROWS:
    name = cfg[1].replace("v3_", "")
    src_dir = f"/home/sparky/ogrs/art/models/farming/{name if name != 'tomato' else 'tomato_v3'}"
    if name == "tomato":
        src_dir = "/home/sparky/ogrs/art/models/farming/tomato_v3"
    if not os.path.isdir(src_dir):
        continue
    dst_dir = f"{windows_dir}/{name}"
    os.makedirs(dst_dir, exist_ok=True)
    for i in (1, 2, 3, 4):
        for ext in ("obj", "mtl"):
            src = f"{src_dir}/stage_{i}.{ext}"
            if os.path.exists(src):
                shutil.copy(src, f"{dst_dir}/stage_{i}.{ext}")
print(f"Synced to: {windows_dir}")
