"""Farm scenery board: 4 patches + 8 scenery items."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

RENDER_DIR = "/home/sparky/ogrs/art/models/_renders"
OUT = f"{RENDER_DIR}/FARM_SCENERY_BOARD.png"

CELL = 220
PAD = 14
TITLE_H = 70

SECTIONS = [
    ("Patch states — where crops grow (3×3 tile)", [
        ("patch_weeds",    "Overgrown",       "natural grass + weeds"),
        ("patch_weeded",   "Partially cleared", "half dirt / half grass"),
        ("patch_cleared",  "Cleared (raked)", "brown soil + ridges"),
        ("patch_planted",  "Planted",         "mound + seed marker"),
    ]),
    ("Scenery — farm infrastructure", [
        ("scarecrow",         "Scarecrow",       "wooden cross + straw + hat"),
        ("leprechaun_stand",  "Leprechaun stand", "NPC signpost"),
        ("compost_bin",       "Compost bin",     "wooden slats + compost"),
        ("water_can_stand",   "Water can stand", "post + hanging can"),
        ("tool_rack",         "Tool rack",       "hoe + rake + spade"),
        ("fence_section",     "Fence section",   "posts + slats + rails"),
        ("corner_stake",      "Corner stake",    "patch boundary marker"),
        ("bonemeal_pile",     "Bonemeal pile",   "fertilizer heap"),
    ]),
]

COLS = 4
SECTION_HEADER_H = 50
LABEL_H = 40

# Compute total height
total_rows = 0
for _, items in SECTIONS:
    rows_in_section = (len(items) + COLS - 1) // COLS
    total_rows += rows_in_section

W = PAD + COLS * (CELL + PAD) + PAD
H = TITLE_H + sum(SECTION_HEADER_H + ((len(items) + COLS - 1) // COLS) * (CELL + LABEL_H + PAD) for _, items in SECTIONS) + PAD

img = Image.new("RGB", (W, H), (24, 22, 32))
draw = ImageDraw.Draw(img)

try:
    font_lbl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_sec = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except Exception:
    font_lbl = font_sub = font_sec = font_title = ImageFont.load_default()

draw.text((PAD, 18), "OGRS Farm Patches + Scenery (12 models)",
          fill=(255, 255, 255), font=font_title)

y = TITLE_H
for section_title, items in SECTIONS:
    # Section header bar
    draw.rectangle([(PAD, y), (W - PAD, y + SECTION_HEADER_H - 6)], fill=(60, 100, 140))
    draw.text((PAD + 14, y + 12), section_title, fill=(255, 255, 255), font=font_sec)
    y += SECTION_HEADER_H
    col = 0
    for fname, label, desc in items:
        x = PAD + col * (CELL + PAD)
        # Cell bg
        draw.rectangle([(x, y), (x + CELL, y + CELL + LABEL_H)], fill=(50, 50, 60))
        # Render
        src = f"{RENDER_DIR}/scenery_{fname}.png"
        if os.path.exists(src):
            sp = Image.open(src).convert("RGBA")
            if sp.size != (CELL, CELL):
                sp = sp.resize((CELL, CELL), Image.LANCZOS)
            img.paste(sp, (x, y), sp)
        # Labels
        bbox = draw.textbbox((0, 0), label, font=font_lbl)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL - tw) // 2, y + CELL + 4), label, fill=(255, 255, 255), font=font_lbl)
        bbox = draw.textbbox((0, 0), desc, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL - tw) // 2, y + CELL + 22), desc, fill=(170, 170, 200), font=font_sub)
        col += 1
        if col >= COLS:
            col = 0
            y += CELL + LABEL_H + PAD
    if col != 0:
        y += CELL + LABEL_H + PAD

img.save(OUT)
print(f"Board: {OUT}  size={img.size}")

# Sync
windows_dir = "/mnt/c/OGRS_Art/models/farming/patches"
os.makedirs(windows_dir, exist_ok=True)
shutil.copy(OUT, f"{windows_dir}/FARM_SCENERY_BOARD.png")
src_dir = "/home/sparky/ogrs/art/models/farming/patches"
for fname in os.listdir(src_dir):
    if fname.endswith((".obj", ".mtl")):
        shutil.copy(f"{src_dir}/{fname}", f"{windows_dir}/{fname}")
print(f"Synced: {windows_dir}")
