"""Generate the OGRS placeholder logo at 180x180. Hand-replaceable later."""
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter

SIZE = 180
import os; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "client", "src", "res", "icon.png")

# Palette — earth/medieval Old Gielinor feel
BG_DARK = (24, 36, 22, 0)       # transparent canvas
DISC_GREEN = (38, 64, 42, 255)  # deep forest green disc
DISC_RIM = (122, 92, 47, 255)   # aged bronze border
OG_GOLD = (212, 166, 74, 255)   # warm gold letters
OG_SHADOW = (60, 40, 12, 200)   # drop shadow
RS_CREAM = (232, 216, 168, 255) # smaller RS below

img = Image.new("RGBA", (SIZE, SIZE), BG_DARK)
draw = ImageDraw.Draw(img)

# Outer aged-bronze ring
pad = 4
draw.ellipse([pad, pad, SIZE - pad, SIZE - pad], outline=DISC_RIM, width=5)
# Inner forest disc
draw.ellipse([pad + 6, pad + 6, SIZE - pad - 6, SIZE - pad - 6], fill=DISC_GREEN)
# Inner highlight to give the disc a slight roundness
hl = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
hl_draw = ImageDraw.Draw(hl)
hl_draw.ellipse([28, 22, 110, 78], fill=(160, 200, 140, 38))
hl = hl.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img, hl)
draw = ImageDraw.Draw(img)

# Bottom banner — aged bronze ribbon for "RS"
banner_h = 32
banner_top = SIZE - banner_h - 22
banner_left = 26
banner_right = SIZE - 26
draw.rounded_rectangle(
    [banner_left, banner_top, banner_right, banner_top + banner_h],
    radius=6,
    fill=DISC_RIM,
    outline=(48, 32, 12, 255),
    width=2,
)

# Fonts
serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
og_font = ImageFont.truetype(serif, 96)
rs_font = ImageFont.truetype(serif, 24)

# "OG" with drop shadow — centered horizontally, baseline raised slightly
og_text = "OG"
og_bbox = draw.textbbox((0, 0), og_text, font=og_font)
og_w = og_bbox[2] - og_bbox[0]
og_h = og_bbox[3] - og_bbox[1]
og_x = (SIZE - og_w) // 2 - og_bbox[0]
og_y = (banner_top - og_h) // 2 - og_bbox[1] - 2
# Shadow
draw.text((og_x + 3, og_y + 3), og_text, font=og_font, fill=OG_SHADOW)
# Letters
draw.text((og_x, og_y), og_text, font=og_font, fill=OG_GOLD)

# "Old Gielinor" small banner text
rs_text = "OLD GIELINOR"
rs_font_small = ImageFont.truetype(serif, 16)
rs_bbox = draw.textbbox((0, 0), rs_text, font=rs_font_small)
rs_w = rs_bbox[2] - rs_bbox[0]
rs_h = rs_bbox[3] - rs_bbox[1]
rs_x = (SIZE - rs_w) // 2 - rs_bbox[0]
rs_y = banner_top + (banner_h - rs_h) // 2 - rs_bbox[1] - 1
draw.text((rs_x, rs_y), rs_text, font=rs_font_small, fill=RS_CREAM)

img.save(OUT, "PNG")
print(f"Wrote {OUT}: {img.size} mode={img.mode}")
