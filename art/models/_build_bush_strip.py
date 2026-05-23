"""Strip for a single bush — 6 states in a row + sync to Windows."""
import os, shutil, sys
from PIL import Image, ImageDraw, ImageFont

bush_name = sys.argv[1] if len(sys.argv) > 1 else "redberry"

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/BUSH_{bush_name}_STRIP.png"

CELL = 256
PAD = 16
LABEL_H = 38
TITLE_H = 56

STATES = [
    ("1_sapling",        "Sapling"),
    ("2_young",          "Young"),
    ("3_mature_empty",   "Mature (empty)"),
    ("4_mature_partial", "Mature (partial)"),
    ("5_mature_full",    "Mature (FULL)"),
    ("6_dead",           "Dead / removed"),
]

W = len(STATES) * (CELL + PAD) + PAD
H = TITLE_H + CELL + LABEL_H + PAD * 2

img = Image.new("RGB", (W, H), (28, 26, 36))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except Exception:
    font = font_title = ImageFont.load_default()

draw.text((PAD, 16), f"{bush_name.title()} Bush — 6 hand-authored states",
          fill=(255, 255, 255), font=font_title)

for i, (key, label) in enumerate(STATES):
    x = PAD + i * (CELL + PAD)
    y = TITLE_H + PAD
    bg = (55, 70, 50) if "full" in key else ((40, 35, 50) if "dead" in key else (50, 50, 60))
    draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
    src = f"{RENDER_DIR}/bush_{bush_name}_{key}.png"
    if os.path.exists(src):
        sp = Image.open(src).convert("RGBA")
        img.paste(sp, (x, y), sp)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + CELL + 6), label, fill=(220, 220, 230), font=font)

img.save(OUT)
print(f"Strip: {OUT}")

# Sync
windows_dir = f"/mnt/c/OGRS_Art/models/farming/bushes/{bush_name}"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/STRIP.png")
src_dir = f"/home/sparky/ogrs/art/models/farming/bushes/{bush_name}"
if os.path.isdir(src_dir):
    for fname in os.listdir(src_dir):
        if fname.endswith((".obj", ".mtl")):
            shutil.copy(f"{src_dir}/{fname}", f"{windows_dir}/{fname}")
print(f"Synced: {windows_dir}")
