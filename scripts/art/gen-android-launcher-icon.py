#!/usr/bin/env python3
"""
OGRS — generate Android launcher icons procedurally.

5 densities: mdpi (48), hdpi (72), xhdpi (96), xxhdpi (144), xxxhdpi (192).
Each is a rounded-square OGRS shield: dark green RSC-feel background, gold
"OGRS" lettering, hairline border. Saved into the upstream Android module's
drawable folders so the build script picks them up.

Run:
  python3 scripts/art/gen-android-launcher-icon.py
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
ANDROID_RES = REPO / "openrsc-upstream" / "Android_Client" / "Open RSC Android Client" / "src" / "main" / "res"

DENSITIES = {
    "drawable-mdpi":    48,
    "drawable-hdpi":    72,
    "drawable-xhdpi":   96,
    "drawable-xxhdpi": 144,
    "drawable-xxxhdpi":192,
}

# RSC-feeling palette: deep forest green inner, darker outer ring, gold text.
BG_OUTER  = (28, 56, 36, 255)    # dark spruce
BG_INNER  = (52, 102, 64, 255)   # mid forest
BORDER    = (212, 166, 74, 255)  # gold
TEXT_GOLD = (240, 196, 92, 255)
TEXT_DARK = (24, 16, 4, 255)


def find_font(size: int) -> ImageFont.FreeTypeFont:
    """Try a few Linux font paths; fall back to PIL's default if none."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    radius = max(4, size // 6)
    # Outer rounded square (the "tile" silhouette).
    d.rounded_rectangle((0, 0, size - 1, size - 1),
                        radius=radius, fill=BG_OUTER)
    # Inner inset for a chiseled-tile feel.
    inset = max(2, size // 16)
    d.rounded_rectangle((inset, inset, size - 1 - inset, size - 1 - inset),
                        radius=max(2, radius - inset),
                        fill=BG_INNER, outline=BORDER, width=max(1, size // 48))

    # "OGRS" lettering centered. Pick a font size that fills ~60% width.
    text = "OGRS"
    # Iterate font size down until the text fits with margins.
    fsize = int(size * 0.42)
    while fsize > 6:
        font = find_font(fsize)
        bbox = d.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if tw <= size * 0.78 and th <= size * 0.55:
            break
        fsize -= 1
    tx = (size - tw) // 2 - bbox[0]
    ty = (size - th) // 2 - bbox[1] - max(1, size // 64)
    # Subtle drop shadow for legibility on small densities.
    d.text((tx + max(1, size // 48), ty + max(1, size // 48)),
           text, font=font, fill=TEXT_DARK)
    d.text((tx, ty), text, font=font, fill=TEXT_GOLD)
    return img


def main():
    for folder, size in DENSITIES.items():
        out_dir = ANDROID_RES / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        img = render(size)
        out_path = out_dir / "ic_launcher.png"
        img.save(out_path)
        print(f"  {out_path.relative_to(REPO)}  ({size}x{size})")
    print(f"Wrote 5 launcher icons under {ANDROID_RES.relative_to(REPO)}")


if __name__ == "__main__":
    main()
