"""Build a 5-up comparison strip: reference + 4 v2 stages."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/v2_tomato_strip.png"

CELL = 256
PAD = 18
LABEL_H = 38
TITLE_H = 60

panels = [
    ("Vanilla tomatoplant.ob3\n(reference, 498 faces)", "v2_tomato_reference.png"),
    ("Stage 1 — Seedling\n(70 tris)", "v2_tomato_1.png"),
    ("Stage 2 — Growing\n(290 tris)", "v2_tomato_2.png"),
    ("Stage 3 — Ripening\n(590 tris)", "v2_tomato_3.png"),
    ("Stage 4 — Harvest\n(reuses vanilla)", "v2_tomato_4.png"),
]

W = len(panels) * (CELL + PAD) + PAD
H = TITLE_H + CELL + LABEL_H + PAD * 2

img = Image.new("RGB", (W, H), (30, 28, 38))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except Exception:
    font = ImageFont.load_default()
    font_title = ImageFont.load_default()

draw.text((PAD, 14), "Tomato v2 — vs vanilla RSC reference (RSC palette extracted)",
          fill=(255, 255, 255), font=font_title)

for i, (label, fname) in enumerate(panels):
    x = PAD + i * (CELL + PAD)
    y = TITLE_H + PAD
    # Cell bg — neutral, transparent renders read on this
    bg = (80, 100, 70) if i == 0 else (60, 70, 80)
    draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
    src = f"{RENDER_DIR}/{fname}"
    if os.path.exists(src):
        sprite = Image.open(src).convert("RGBA")
        img.paste(sprite, (x, y), sprite)
    # Label (multi-line)
    line1, line2 = label.split("\n")
    for li, line in enumerate((line1, line2)):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL - tw) // 2, y + CELL + 4 + li * 18), line, fill=(220, 220, 230), font=font)

img.save(OUT)
print(f"Strip: {OUT}  size={img.size}")

# Sync to Windows
windows_dir = "/mnt/c/OGRS_Art/models/farming/tomato_v2"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/V2_STRIP.png")
# Renders too
for fname in ("v2_tomato_reference.png", "v2_tomato_1.png", "v2_tomato_2.png", "v2_tomato_3.png", "v2_tomato_4.png"):
    shutil.copy(f"{RENDER_DIR}/{fname}", f"{windows_dir}/{fname}")
# OBJ + MTL files
for i in (1, 2, 3, 4):
    for ext in ("obj", "mtl"):
        src = f"/home/sparky/ogrs/art/models/farming/tomato_v2/stage_{i}.{ext}"
        if os.path.exists(src):
            shutil.copy(src, f"{windows_dir}/stage_{i}.{ext}")
# Reference for completeness
ref_dir = "/home/sparky/ogrs/art/models/_rsc_reference"
for fname in ("tomatoplant.obj", "tomatoplant.mtl", "depletedtomato.obj", "depletedtomato.mtl"):
    src = f"{ref_dir}/{fname}"
    if os.path.exists(src):
        shutil.copy(src, f"{windows_dir}/{fname}")
print(f"Synced to: {windows_dir}")
