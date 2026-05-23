#!/usr/bin/env python3
"""Build a comparison board (6 phases) of all 27 prayer sprites at x8."""
import os
from PIL import Image, ImageDraw, ImageFont

SRC = "/home/sparky/ogrs/art/items/prayer"
OUT = "/home/sparky/ogrs/art/items/prayer/PRAYER_BOARD.png"

CELL = 256          # x8 sprite
PAD = 18
LABEL_H = 26
COLS = 7            # 7 columns

PHASES = [
    ("Phase 1 — Bones (7)", [
        ("bones", "Bones"),
        ("big_bones", "Big Bones"),
        ("wolf_bones", "Wolf Bones"),
        ("babydragon_bones", "Babydragon"),
        ("dragon_bones", "Dragon Bones"),
        ("burnt_bones", "Burnt Bones"),
        ("ashes", "Ashes"),
    ]),
    ("Phase 2 — Holy implements (7)", [
        ("holy_water_vial", "Holy Water"),
        ("anointing_oil_flask", "Anointing Oil"),
        ("holy_symbol", "Holy Symbol"),
        ("censer_lit", "Censer (lit)"),
        ("censer_unlit", "Censer (unlit)"),
        ("incense_stick", "Incense Stick"),
        ("anointing_horn", "Anointing Horn"),
    ]),
    ("Phase 3 — Communion (4)", [
        ("unleavened_bread", "Unleavened Bread"),
        ("communion_cup", "Communion Cup"),
        ("bread_of_presence", "Bread of Presence"),
        ("blessed_candle", "Blessed Candle"),
    ]),
    ("Phase 4 — Priest garments (4)", [
        ("priest_robe_top", "Robe Top"),
        ("priest_robe_bottom", "Robe Bottom"),
        ("mitre", "Mitre"),
        ("stole", "Stole"),
    ]),
    ("Phase 5 — Books & scrolls (3)", [
        ("yahwist_scripture", "Yahwist Scripture"),
        ("sealed_scroll", "Sealed Scroll"),
        ("open_prayer_scroll", "Prayer Scroll"),
    ]),
    ("Phase 6 — Special (2)", [
        ("cherubim_seal", "Cherubim Seal"),
        ("demonic_ashes", "Demonic Ashes"),
    ]),
]

PHASE_HEADER_H = 56

# Compute total height
total_h = PAD
row_w = COLS * (CELL + PAD) + PAD
for title, items in PHASES:
    total_h += PHASE_HEADER_H
    rows_in_phase = (len(items) + COLS - 1) // COLS
    total_h += rows_in_phase * (CELL + LABEL_H + PAD)

board = Image.new("RGB", (row_w, total_h), (30, 28, 38))
draw = ImageDraw.Draw(board)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    font_hdr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
except Exception:
    font = ImageFont.load_default()
    font_hdr = ImageFont.load_default()

y = PAD
for title, items in PHASES:
    # Phase header bar
    draw.rectangle([(PAD, y), (row_w - PAD, y + PHASE_HEADER_H - 8)], fill=(60, 100, 140))
    draw.text((PAD + 12, y + 8), title, fill=(255, 255, 255), font=font_hdr)
    y += PHASE_HEADER_H
    # Cells
    col = 0
    for fname, label in items:
        x = PAD + col * (CELL + PAD)
        # Cell bg
        draw.rectangle([(x, y), (x + CELL, y + CELL + LABEL_H)], fill=(45, 42, 55))
        # Sprite
        sprite_path = f"{SRC}/{fname}_x8.png"
        if os.path.exists(sprite_path):
            sprite = Image.open(sprite_path).convert("RGBA")
            board.paste(sprite, (x, y), sprite)
        # Label
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL - tw) // 2, y + CELL + 2), label, fill=(220, 220, 230), font=font)
        col += 1
        if col >= COLS:
            col = 0
            y += CELL + LABEL_H + PAD
    if col != 0:
        y += CELL + LABEL_H + PAD

board.save(OUT)
print(f"Board saved: {OUT} ({board.size[0]}x{board.size[1]})")

# Also sync to Windows side
import shutil
windows_path = "/mnt/c/OGRS_Art/items/prayer/PRAYER_BOARD.png"
os.makedirs(os.path.dirname(windows_path), exist_ok=True)
shutil.copy(OUT, windows_path)
# Also copy all individual prayer x8 sprites for browsing
for phase_title, items in PHASES:
    for fname, _ in items:
        src = f"{SRC}/{fname}_x8.png"
        if os.path.exists(src):
            shutil.copy(src, f"/mnt/c/OGRS_Art/items/prayer/{fname}_x8.png")
print(f"Synced to: {windows_path}")
