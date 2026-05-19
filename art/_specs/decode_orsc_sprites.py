#!/usr/bin/env python3
"""
Decode entries from Authentic_Sprites.orsc.
Per zip entry (from com/openrsc/client/model/Sprite.unpack):
  int width, int height, byte requiresShift,
  int xShift, int yShift, int something1, int something2,
  int[width*height] pixels  -- all big-endian
Header = 25 bytes.
"""
import struct, sys, zipfile
from PIL import Image

ARCHIVE = "/home/sparky/ogrs/client/Cache/video/Authentic_Sprites.orsc"
OUTDIR = "/home/sparky/ogrs/art/reference"

def decode(data):
    if len(data) < 25:
        return None
    w, h = struct.unpack(">II", data[0:8])
    shift = data[8]
    xs, ys, s1, s2 = struct.unpack(">IIII", data[9:25])
    expected = 25 + w * h * 4
    if len(data) < expected:
        return None
    pixels = struct.unpack(f">{w*h}I", data[25:expected])
    img = Image.new("RGBA", (w, h))
    for i, p in enumerate(pixels):
        # Treat 0 as transparent (RSC convention), else opaque RGB from low 24 bits.
        if p == 0:
            img.putpixel((i % w, i // w), (0, 0, 0, 0))
        else:
            r = (p >> 16) & 0xFF
            g = (p >> 8) & 0xFF
            b = p & 0xFF
            img.putpixel((i % w, i // w), (r, g, b, 255))
    return img, (w, h, shift, xs, ys, s1, s2)

TYPES = {
    "3160": "ORB",
    "3161": "MAGIC",
    "3162": "RANGED",
    "3163": "GNOMEBALL",
    "3164": "SKULL",
    "3165": "SPIKEBALL",
    "3166": "BLANK",
}

def main():
    with zipfile.ZipFile(ARCHIVE) as z:
        for eid, name in TYPES.items():
            try:
                data = z.read(eid)
            except KeyError:
                print(f"missing {eid}")
                continue
            res = decode(data)
            if not res:
                print(f"{eid}: decode failed")
                continue
            img, meta = res
            w, h, shift, xs, ys, s1, s2 = meta
            base = f"{OUTDIR}/proj_{eid}_{name}"
            img.save(base + ".png")
            img.resize((w * 8, h * 8), Image.NEAREST).save(base + "_x8.png")
            print(f"{eid} ({name}): {w}x{h} shift={shift} xs={xs} ys={ys} s1={s1} s2={s2}")

if __name__ == "__main__":
    main()
