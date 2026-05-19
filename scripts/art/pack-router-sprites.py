#!/usr/bin/env python3
"""
OGRS — Pack the 7 router projectile sprites into Authentic_Sprites.orsc.

Replaces ZIP entries 3160-3166 (the projectile slots — ORB, MAGIC, RANGED,
GNOMEBALL, SKULL, SPIKEBALL, BLANK) with new art authored at
~/ogrs/art/projectiles/<i>_<name>/frames/frame_02.png. Frame 02 is the
"peak" frame per the authoring spec, which reads best as a static
in-flight sprite (the engine doesn't animate projectiles per frame —
just one static sprite during the flight arc).

Blob format (from client/src/com/openrsc/client/model/Sprite.unpack):
    int   width            (4 bytes, big-endian)
    int   height           (4 bytes BE)
    byte  requiresShift    (1 byte, 1 = true)
    int   xShift           (4 bytes BE)
    int   yShift           (4 bytes BE)
    int   something1       (4 bytes BE)
    int   something2       (4 bytes BE)
    int[] pixels (w*h)     (4 bytes ARGB each, BE)

Strategy: read the existing entry's header so we preserve the shift /
"something" values (they govern draw-origin offsets); only swap the
pixel payload (and update width/height to the new 30x30).

Run: python3 scripts/art/pack-router-sprites.py
"""
import os
import shutil
import struct
import sys
import zipfile
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
ARCHIVE = REPO / "client" / "Cache" / "video" / "Authentic_Sprites.orsc"
BACKUP = ARCHIVE.with_suffix(ARCHIVE.suffix + ".bak")
ART_ROOT = REPO / "art" / "projectiles"

# Slot ID -> source folder (matching HANDOFF.md §1A).
SLOTS = {
    3160: "0_orb",
    3161: "1_magic",
    3162: "2_ranged",
    3163: "3_gnomeball",
    3164: "4_skull",
    3165: "5_spikeball",
    3166: "6_blank",
}

HEADER_FMT = ">IIbIIII"          # width, height, requiresShift, xShift, yShift, s1, s2
HEADER_LEN = struct.calcsize(HEADER_FMT)  # 25


def read_header(blob: bytes) -> dict:
    if len(blob) < HEADER_LEN:
        raise ValueError(f"blob too short: {len(blob)} bytes")
    w, h, rs, xs, ys, s1, s2 = struct.unpack(HEADER_FMT, blob[:HEADER_LEN])
    return {
        "width": w, "height": h,
        "requires_shift": rs, "x_shift": xs, "y_shift": ys,
        "something1": s1, "something2": s2,
    }


def encode_blob(img: Image.Image, header: dict) -> bytes:
    """Encode the new sprite blob with the art's dimensions but original
    shift / something values (so positioning matches the engine's
    expectations for the projectile slot)."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    w, h = img.size
    pixels = img.tobytes()  # RGBA, row-major
    # Convert RGBA -> ARGB big-endian ints
    out = bytearray()
    out += struct.pack(
        HEADER_FMT,
        w, h,
        header["requires_shift"],
        header["x_shift"],
        header["y_shift"],
        header["something1"],
        header["something2"],
    )
    for i in range(0, len(pixels), 4):
        r, g, b, a = pixels[i], pixels[i + 1], pixels[i + 2], pixels[i + 3]
        out += bytes((a, r, g, b))
    return bytes(out)


def main() -> int:
    if not ARCHIVE.exists():
        print(f"FATAL: {ARCHIVE} not found", file=sys.stderr)
        return 1
    if not BACKUP.exists():
        print(f"Backing up archive -> {BACKUP}")
        shutil.copy2(ARCHIVE, BACKUP)
    else:
        print(f"Backup exists at {BACKUP} (leaving alone)")

    # Read all entries + names from the (current) archive. We work from
    # the backup so the script is idempotent — running it twice yields
    # the same output without compounding.
    with zipfile.ZipFile(BACKUP, "r") as zin:
        names = zin.namelist()
        # Read every entry's bytes into memory (~18 MB OK for this repo).
        entries = {n: zin.read(n) for n in names}

    # Build the replacement blobs.
    replaced = 0
    for slot, folder in SLOTS.items():
        key = str(slot)
        if key not in entries:
            print(f"WARN: slot {slot} missing in archive — skipping")
            continue
        png_path = ART_ROOT / folder / "frames" / "frame_02.png"
        if not png_path.exists():
            print(f"WARN: art missing {png_path} — leaving slot {slot} as-is")
            continue
        old_header = read_header(entries[key])
        img = Image.open(png_path)
        new_blob = encode_blob(img, old_header)
        entries[key] = new_blob
        print(f"  slot {slot} <- {png_path.relative_to(REPO)} "
              f"({img.size[0]}x{img.size[1]}, {len(new_blob)} bytes; "
              f"shift={old_header['x_shift']},{old_header['y_shift']})")
        replaced += 1

    # Rewrite the archive in place.
    tmp = ARCHIVE.with_suffix(ARCHIVE.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, entries[n])
    tmp.replace(ARCHIVE)
    print(f"Wrote {ARCHIVE} ({len(names)} entries, {replaced} replaced).")

    # Optional: mirror to the Windows install if /mnt/c/OGRS exists.
    mirror = Path("/mnt/c/OGRS/Cache/video/Authentic_Sprites.orsc")
    if mirror.parent.exists():
        shutil.copy2(ARCHIVE, mirror)
        print(f"Mirrored to {mirror}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
