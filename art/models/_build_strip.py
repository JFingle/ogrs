"""Build a 4-up comparison strip from the tomato stage renders."""
import os
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/tomato_stages_strip.png"

CELL = 256
PAD = 16
LABEL_H = 36
TITLE_H = 48

labels = [
    ("Stage 1 — Seedling", "tomato_stage_1.png"),
    ("Stage 2 — Growing",  "tomato_stage_2.png"),
    ("Stage 3 — Ripening", "tomato_stage_3.png"),
    ("Stage 4 — Harvest",  "tomato_stage_4.png"),
]

W = 4 * (CELL + PAD) + PAD
H = TITLE_H + CELL + LABEL_H + PAD * 2

img = Image.new("RGB", (W, H), (30, 28, 38))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except Exception:
    font = ImageFont.load_default()
    font_title = ImageFont.load_default()

draw.text((PAD, 10), "Tomato — 3D growth stages", fill=(255, 255, 255), font=font_title)

for i, (label, fname) in enumerate(labels):
    x = PAD + i * (CELL + PAD)
    y = TITLE_H + PAD
    # Cell bg (light grass tone so transparent renders read)
    draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=(95, 130, 80))
    src = f"{RENDER_DIR}/{fname}"
    if os.path.exists(src):
        sprite = Image.open(src).convert("RGBA")
        img.paste(sprite, (x, y), sprite)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (CELL - tw) // 2, y + CELL + 4), label, fill=(220, 220, 230), font=font)

img.save(OUT)
print(f"Strip saved: {OUT}")

# Sync to Windows
import shutil
windows_dir = "/mnt/c/OGRS_Art/models/farming/tomato"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/STAGES_STRIP.png")
for i in range(1, 5):
    shutil.copy(f"{RENDER_DIR}/tomato_stage_{i}.png", f"{windows_dir}/stage_{i}_render.png")
# Also copy the .obj + .mtl
for i in range(1, 5):
    obj_src = f"/home/sparky/ogrs/art/models/farming/tomato/stage_{i}.obj"
    mtl_src = f"/home/sparky/ogrs/art/models/farming/tomato/stage_{i}.mtl"
    if os.path.exists(obj_src):
        shutil.copy(obj_src, f"{windows_dir}/stage_{i}.obj")
    if os.path.exists(mtl_src):
        shutil.copy(mtl_src, f"{windows_dir}/stage_{i}.mtl")
print(f"Synced to: {windows_dir}")
