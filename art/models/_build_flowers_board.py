"""Common flowers board: 7 species × 4 stages."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/FLOWERS_COMMON_BOARD.png"

CELL = 200
PAD = 10
LABEL_W = 200
TITLE_H = 64
COL_HEADER_H = 44

FLOWERS = [
    ("Daisy",     "daisy",     "white petals + yellow disc, low growing"),
    ("Lavender",  "lavender",  "purple flower-spike on tall thin stem"),
    ("Marigold",  "marigold",  "orange pompom blooms, bushy"),
    ("Poppy",     "poppy",     "4 red cup-petals + black center"),
    ("Rose",      "rose",      "spiral red petals, thorny branching"),
    ("Sunflower", "sunflower", "tall stem, huge yellow ray bloom"),
    ("Tulip",     "tulip",     "cup-shaped 6 petals, single bloom"),
]
STAGES = [
    ("1_seedling", "Seedling"),
    ("2_growing",  "Growing"),
    ("3_budding",  "Budding"),
    ("4_mature",   "Mature (FULL)"),
]

W = LABEL_W + len(STAGES) * (CELL + PAD) + PAD
H = TITLE_H + COL_HEADER_H + len(FLOWERS) * (CELL + PAD) + PAD

img = Image.new("RGB", (W, H), (24, 22, 32))
draw = ImageDraw.Draw(img)

try:
    font_lbl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 19)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_col = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except Exception:
    font_lbl = font_sub = font_col = font_title = ImageFont.load_default()

draw.text((PAD, 18),
          "OGRS Common Flowers — 7 species × 4 stages (hand-authored, real-world researched)",
          fill=(255, 255, 255), font=font_title)

for ci, (key, head) in enumerate(STAGES):
    x = LABEL_W + PAD + ci * (CELL + PAD)
    y = TITLE_H
    bbox = draw.textbbox((0, 0), head, font=font_col)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + 12), head, fill=(255, 240, 180), font=font_col)

for ri, (label, prefix, desc) in enumerate(FLOWERS):
    y = TITLE_H + COL_HEADER_H + ri * (CELL + PAD)
    draw.rectangle([(0, y), (LABEL_W - PAD, y + CELL)], fill=(45, 42, 55))
    draw.text((10, y + 16), label, fill=(255, 255, 255), font=font_lbl)
    words = desc.split(" ")
    line = ""; line_y = y + 44
    for w in words:
        test = (line + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font_sub)
        if bbox[2] - bbox[0] > LABEL_W - 24:
            draw.text((10, line_y), line, fill=(170, 170, 200), font=font_sub)
            line = w; line_y += 16
        else:
            line = test
    if line:
        draw.text((10, line_y), line, fill=(170, 170, 200), font=font_sub)
    for ci, (key, head) in enumerate(STAGES):
        x = LABEL_W + PAD + ci * (CELL + PAD)
        bg = (55, 70, 50) if "mature" in key else (50, 50, 60)
        draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
        src = f"{RENDER_DIR}/flower_{prefix}_{key}.png"
        if os.path.exists(src):
            sp = Image.open(src).convert("RGBA")
            if sp.size != (CELL, CELL):
                sp = sp.resize((CELL, CELL), Image.LANCZOS)
            img.paste(sp, (x, y), sp)

img.save(OUT)
print(f"Board: {OUT}  size={img.size}")

windows_dir = "/mnt/c/OGRS_Art/models/farming/flowers"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/FLOWERS_COMMON_BOARD.png")
src_base = "/home/sparky/ogrs/art/models/farming/flowers"
for label, prefix, desc in FLOWERS:
    src_dir = f"{src_base}/{prefix}"
    dst_dir = f"{windows_dir}/{prefix}"
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.isdir(src_dir):
        for fname in os.listdir(src_dir):
            if fname.endswith((".obj", ".mtl")):
                shutil.copy(f"{src_dir}/{fname}", f"{dst_dir}/{fname}")
print(f"Synced: {windows_dir}")
