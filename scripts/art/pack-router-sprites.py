#!/usr/bin/env python3
"""
OGRS — Pack art sprites into Authentic_Sprites.orsc.

Replaces / adds entries for:
  * Router slots 3160-3166 (HANDOFF.md §1A / §3A).
  * Unique spell projectiles 3167-3204 (§1C / §3B): 38 spells, one frame
    each. Frame_02 picked per the authoring spec (peak frame, best for
    a static in-flight read).
  * Router impacts 3700-3727 (§1B / §3C): 7 types x 4 frames each.
  * Crumble Undead impact 3730-3733 (§1B / §3E): 4 frames.
  * Directional arrow + flame variants 3740-3755 (§1E / §3D): 8
    compass directions per sprite (N, NE, E, SE, S, SW, W, NW).

Blob format (from client/src/com/openrsc/client/model/Sprite.unpack):
    int   width            (4 bytes, big-endian)
    int   height           (4 bytes BE)
    byte  requiresShift    (1 byte, 1 = true)
    int   xShift           (4 bytes BE)
    int   yShift           (4 bytes BE)
    int   something1       (4 bytes BE)
    int   something2       (4 bytes BE)
    int[] pixels (w*h)     (4 bytes ARGB each, BE)

Strategy:
  * Router slots: read the existing entry's header so we preserve the
    shift / "something" values (they govern draw-origin offsets); only
    swap the pixel payload.
  * New slots (unique projectiles, impacts, directions): synthesize a
    header. requiresShift=1, xShift=yShift=imgW/2 for projectiles
    (center-anchored), 32/32 for "something" (matching the originals).

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

HEADER_FMT = ">IIbIIII"          # width, height, requiresShift, xShift, yShift, s1, s2
HEADER_LEN = struct.calcsize(HEADER_FMT)  # 25

# -- Router projectile slots (§3A — header preserved from original) ---------
ROUTER_SLOTS = {
    3160: "0_orb",
    3161: "1_magic",
    3162: "2_ranged",
    3163: "3_gnomeball",
    3164: "4_skull",
    3165: "5_spikeball",
    3166: "6_blank",
}

# -- Unique spell projectiles (§3B — 38 spells, IDs 3167-3204) -------------
# Order matters: the index in this list defines the OgrsProjectileTypes
# integer constant. Keep in lockstep with OgrsProjectileTypes.java and
# EntityHandler.loadProjectiles().
UNIQUE_PROJ_FOLDERS = [
    # idx 7 onward (since 0..6 are router types)
    "debuff_confuse",        # 7
    "debuff_weaken",         # 8
    "debuff_vulnerability",  # 9
    "debuff_enfeeble",       # 10
    "debuff_stun",           # 11
    "debuff_crumble_undead", # 12
    "debuff_fear",           # 13
    "bolt_chill",            # 14
    "bolt_shock",            # 15
    "bolt_elemental",        # 16
    "bolt_iban",             # 17
    "element_fire",          # 18
    "buff_thick_skin",       # 19
    "buff_burst_of_strength",# 20
    "buff_rock_skin",        # 21
    "buff_camouflage",       # 22
    "util_low_alch",         # 23
    "util_high_alch",        # 24
    "util_telegrab",         # 25
    "util_bones_to_bananas", # 26
    "util_bones_to_bread",   # 27
    "util_superheat",        # 28
    "util_charge",           # 29
    "charge_air_orb",        # 30
    "charge_water_orb",      # 31
    "charge_earth_orb",      # 32
    "charge_fire_orb",       # 33
    "tele_varrock",          # 34
    "tele_lumbridge",        # 35
    "tele_falador",          # 36
    "tele_camelot",          # 37
    "tele_ardougne",         # 38
    "tele_watchtower",       # 39
    "enchant_lvl1",          # 40
    "enchant_lvl2",          # 41
    "enchant_lvl3",          # 42
    "enchant_lvl4",          # 43
    "enchant_lvl5",          # 44
]
UNIQUE_PROJ_BASE = 3167  # type 7 -> slot 3167

# -- Impact sprites (§3C — 7 routers x 4 frames, IDs 3700-3727) ------------
IMPACT_SLOTS = [
    # (folder, baseSlotId). 4 frames consumed sequentially.
    ("0_orb",        3700),
    ("1_magic",      3704),
    # 2_ranged has no impact authored (it's an arrow — physical hit, no burst)
    ("3_gnomeball",  3708),
    ("4_skull",      3712),
    ("5_spikeball",  3716),
    ("element_fire", 3720),   # FIRE family impact
    ("debuff_crumble_undead", 3724),  # holy bone burst (used by §3E too)
]

# -- Directional variants (§3D — 8 dirs for arrow + flame, IDs 3740-3755) --
# Order follows the atan2 picker: 0=E, 1=SE, 2=S, 3=SW, 4=W, 5=NW, 6=N, 7=NE
DIR_ORDER = ["E", "SE", "S", "SW", "W", "NW", "N", "NE"]
DIRECTION_SETS = [
    ("2_ranged",     3740),  # 3740..3747
    ("element_fire", 3748),  # 3748..3755
]


def read_header(blob: bytes) -> dict:
    if len(blob) < HEADER_LEN:
        raise ValueError(f"blob too short: {len(blob)} bytes")
    w, h, rs, xs, ys, s1, s2 = struct.unpack(HEADER_FMT, blob[:HEADER_LEN])
    return {
        "width": w, "height": h,
        "requires_shift": rs, "x_shift": xs, "y_shift": ys,
        "something1": s1, "something2": s2,
    }


def synth_header(w: int, h: int, *, anchor_center: bool) -> dict:
    """Synthesize a header for a brand-new sprite slot.

    Sparky 2026-05-20: the original anchor_center=True path produced
    x_shift=15/y_shift=15 for our 30x30 sprites. The engine's
    drawSpriteClipping/drawSprite both consult those shifts and pixel-
    offset the draw by ~19 px for that combination — sprites rendered
    off-center in the autocast picker and at unexpected screen positions
    during projectile flight. Setting shifts to zero (with
    requires_shift still true to match the originals' flag) keeps the
    flight-time positioning math behaved and the UI-tile draws centered.
    """
    return {
        "width": w, "height": h,
        "requires_shift": 1,
        "x_shift": 0,
        "y_shift": 0,
        "something1": 32,
        "something2": 32,
    }


def encode_blob(img: Image.Image, header: dict) -> bytes:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    w, h = img.size
    pixels = img.tobytes()
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


def replace_router_slot(entries: dict, slot: int, folder: str) -> bool:
    key = str(slot)
    if key not in entries:
        print(f"WARN: slot {slot} missing in archive — skipping")
        return False
    png = ART_ROOT / folder / "frames" / "frame_02.png"
    if not png.exists():
        print(f"WARN: art missing {png} — leaving slot {slot} as-is")
        return False
    old = read_header(entries[key])
    img = Image.open(png)
    entries[key] = encode_blob(img, old)
    return True


def write_new_slot(entries: dict, slot: int, png_path: Path, *, anchor_center: bool) -> bool:
    if not png_path.exists():
        print(f"WARN: art missing {png_path} — skipping slot {slot}")
        return False
    img = Image.open(png_path)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    hdr = synth_header(img.size[0], img.size[1], anchor_center=anchor_center)
    entries[str(slot)] = encode_blob(img, hdr)
    return True


def main() -> int:
    if not ARCHIVE.exists():
        print(f"FATAL: {ARCHIVE} not found", file=sys.stderr)
        return 1
    if not BACKUP.exists():
        print(f"Backing up archive -> {BACKUP}")
        shutil.copy2(ARCHIVE, BACKUP)
    else:
        print(f"Backup exists at {BACKUP} (leaving alone)")

    with zipfile.ZipFile(BACKUP, "r") as zin:
        names = zin.namelist()
        entries = {n: zin.read(n) for n in names}

    # 1) Router slots (existing entries, preserve header).
    print("Packing router slots (§3A):")
    replaced = 0
    for slot, folder in ROUTER_SLOTS.items():
        if replace_router_slot(entries, slot, folder):
            print(f"  {slot:4d} <- {folder}/frame_02.png")
            replaced += 1

    # 2) Unique spell projectiles (§3B), new entries.
    print("Packing unique spell projectiles (§3B):")
    added_uniq = 0
    for idx, folder in enumerate(UNIQUE_PROJ_FOLDERS):
        slot = UNIQUE_PROJ_BASE + idx
        png = ART_ROOT / folder / "frames" / "frame_02.png"
        if write_new_slot(entries, slot, png, anchor_center=True):
            names_set = set(names)
            if str(slot) not in names_set:
                names.append(str(slot))
            print(f"  {slot:4d} <- {folder}/frame_02.png (type id {idx + 7})")
            added_uniq += 1

    # 3) Router impact sprites (§3C), 4 frames per type.
    print("Packing router impacts (§3C):")
    added_imp = 0
    for folder, base in IMPACT_SLOTS:
        for f in range(4):
            slot = base + f
            png = ART_ROOT / folder / "impact" / f"frame_{f:02d}.png"
            if write_new_slot(entries, slot, png, anchor_center=True):
                if str(slot) not in set(names):
                    names.append(str(slot))
                added_imp += 1
        print(f"  {base:4d}..{base+3} <- {folder}/impact/")

    # 4) Directional variants (§3D), arrow + flame x 8 directions.
    print("Packing directional variants (§3D):")
    added_dir = 0
    for folder, base in DIRECTION_SETS:
        for i, dname in enumerate(DIR_ORDER):
            slot = base + i
            # Naming differs per folder; try a couple of conventions.
            candidates = [
                ART_ROOT / folder / "directions" / f"arrow_{dname}.png",
                ART_ROOT / folder / "directions" / f"flame_{dname}.png",
                ART_ROOT / folder / "directions" / f"{dname}.png",
            ]
            png = next((p for p in candidates if p.exists()), None)
            if png is None:
                print(f"WARN: no direction art for {folder}/{dname} — skipping slot {slot}")
                continue
            if write_new_slot(entries, slot, png, anchor_center=True):
                if str(slot) not in set(names):
                    names.append(str(slot))
                added_dir += 1
        print(f"  {base:4d}..{base+7} <- {folder}/directions/")

    # Rewrite archive in place.
    tmp = ARCHIVE.with_suffix(ARCHIVE.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, entries[n])
    tmp.replace(ARCHIVE)
    print(
        f"Wrote {ARCHIVE}: {len(names)} entries, "
        f"{replaced} router replaced + {added_uniq} unique + "
        f"{added_imp} impact + {added_dir} direction frames."
    )

    mirror = Path("/mnt/c/OGRS/Cache/video/Authentic_Sprites.orsc")
    if mirror.parent.exists():
        shutil.copy2(ARCHIVE, mirror)
        print(f"Mirrored to {mirror}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
