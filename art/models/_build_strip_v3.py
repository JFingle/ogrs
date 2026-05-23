"""Comparison strip: vanilla + 4 v3 stages."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/v3_tomato_strip.png"

CELL = 256
PAD = 18
LABEL_H = 38
TITLE_H = 60

panels = [
    ("Vanilla tomatoplant\n(reference)", "v3_tomato_reference.png", (80, 100, 70)),
    ("Stage 1 — Seedling\ndepletedtomato @ 25%", "v3_tomato_1.png", (60, 70, 80)),
    ("Stage 2 — Growing\ndepletedtomato @ 60%", "v3_tomato_2.png", (60, 70, 80)),
    ("Stage 3 — Ripening\ntomatoplant + unripe green", "v3_tomato_3.png", (60, 70, 80)),
    ("Stage 4 — Harvest\nvanilla tomatoplant", "v3_tomato_4.png", (60, 70, 80)),
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

draw.text((PAD, 14), "Tomato v3 — derived from vanilla RSC geometry",
          fill=(255, 255, 255), font=font_title)

for i, (label, fname, bg) in enumerate(panels):
    x = PAD + i * (CELL + PAD)
    y = TITLE_H + PAD
    draw.rectangle([(x, y), (x + CELL, y + CELL)], fill=bg)
    src = f"{RENDER_DIR}/{fname}"
    if os.path.exists(src):
        sprite = Image.open(src).convert("RGBA")
        img.paste(sprite, (x, y), sprite)
    line1, line2 = label.split("\n")
    for li, line in enumerate((line1, line2)):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL - tw) // 2, y + CELL + 4 + li * 18), line, fill=(220, 220, 230), font=font)

img.save(OUT)
print(f"Strip: {OUT}  size={img.size}")

windows_dir = "/mnt/c/OGRS_Art/models/farming/tomato_v3"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/V3_STRIP.png")
for fname in ("v3_tomato_reference.png", "v3_tomato_1.png", "v3_tomato_2.png", "v3_tomato_3.png", "v3_tomato_4.png"):
    shutil.copy(f"{RENDER_DIR}/{fname}", f"{windows_dir}/{fname}")
for i in (1, 2, 3, 4):
    for ext in ("obj", "mtl"):
        src = f"/home/sparky/ogrs/art/models/farming/tomato_v3/stage_{i}.{ext}"
        if os.path.exists(src):
            shutil.copy(src, f"{windows_dir}/stage_{i}.{ext}")
print(f"Synced to: {windows_dir}")
