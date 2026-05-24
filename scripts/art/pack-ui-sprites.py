#!/usr/bin/env python3
"""
OGRS — Pack the UI track (57 sprites) into Authentic_Sprites.orsc.

Per UI_INTEGRATION.md the UI track is rendered directly by mudclient
draw calls, not via ItemDefs. We allocate a fixed cache slot range
starting at 3837 (past the debuff swirls at 3779 and out of the way
of items 2150-3429), pack each PNG, and update mudclient.loadSprites
to load these new slots as "media" so they're available at boot.

Slot allocation:
  3837..3839   P1 status   — poison_a/b + slayer_task_widget
  3840..3860   P2 skills   — 21 skill icons
  3861..3864   P3 combat   — 4 combat-style icons
  3865..3873   P4 tabs     — 9 tab-strip icons
  3874..3876   P4 run      — 3 run-energy variants
  3877         P5 splash   — login_splash
  3878..3886   P5 dialog   — 9 dialog 9-slice pieces
  3887..3890   P6 cursors  — 4 cursor variants
  TOTAL: 54 slots (3837..3890)

After packing, mudclient.loadSprites() needs ONE new line:
  loadSprite(3837, "media", 54);   // OGRS UI sprites

Sprite header (same format as pack-router-sprites.py):
  int width, int height, byte requiresShift,
  int xShift, int yShift, int something1, int something2,
  int[width*height] pixels  -- all big-endian ARGB
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
ART_ROOT = REPO / "art" / "items" / "ui"

HEADER_FMT = ">IIbIIII"   # w, h, requiresShift, xShift, yShift, s1, s2
HEADER_LEN = struct.calcsize(HEADER_FMT)  # 25

# Slot allocation. Each entry: (slot, filename, anchor_center_bool, label)
SLOTS = [
    # P1 status
    (3837, "poison_active_a.png",      True,  "P1 poison_a"),
    (3838, "poison_active_b.png",      True,  "P1 poison_b"),
    (3839, "slayer_task_widget.png",   False, "P1 slayer_widget"),
    # P2 skills (21)
    (3840, "skill_attack.png",         False, "P2 attack"),
    (3841, "skill_strength.png",       False, "P2 strength"),
    (3842, "skill_defense.png",        False, "P2 defense"),
    (3843, "skill_hits.png",           False, "P2 hits"),
    (3844, "skill_ranged.png",         False, "P2 ranged"),
    (3845, "skill_prayer.png",         False, "P2 prayer"),
    (3846, "skill_magic.png",          False, "P2 magic"),
    (3847, "skill_cooking.png",        False, "P2 cooking"),
    (3848, "skill_woodcutting.png",    False, "P2 woodcutting"),
    (3849, "skill_fletching.png",      False, "P2 fletching"),
    (3850, "skill_fishing.png",        False, "P2 fishing"),
    (3851, "skill_firemaking.png",     False, "P2 firemaking"),
    (3852, "skill_crafting.png",       False, "P2 crafting"),
    (3853, "skill_smithing.png",       False, "P2 smithing"),
    (3854, "skill_mining.png",         False, "P2 mining"),
    (3855, "skill_herblore.png",       False, "P2 herblore"),
    (3856, "skill_agility.png",        False, "P2 agility"),
    (3857, "skill_thieving.png",       False, "P2 thieving"),
    (3858, "skill_slayer.png",         False, "P2 slayer (OGRS)"),
    (3859, "skill_farming.png",        False, "P2 farming (OGRS)"),
    (3860, "skill_runecraft.png",      False, "P2 runecraft"),
    # P3 combat tab (4)
    (3861, "combat_attack.png",        False, "P3 combat_attack"),
    (3862, "combat_strength.png",      False, "P3 combat_strength"),
    (3863, "combat_defense.png",       False, "P3 combat_defense"),
    (3864, "combat_hits.png",          False, "P3 combat_hits"),
    # P4 tab strip (9)
    (3865, "tab_inv.png",              False, "P4 tab_inv"),
    (3866, "tab_map.png",              False, "P4 tab_map"),
    (3867, "tab_skills.png",           False, "P4 tab_skills"),
    (3868, "tab_magic.png",            False, "P4 tab_magic"),
    (3869, "tab_prayer.png",           False, "P4 tab_prayer"),
    (3870, "tab_friends.png",          False, "P4 tab_friends"),
    (3871, "tab_combat.png",           False, "P4 tab_combat"),
    (3872, "tab_options.png",          False, "P4 tab_options"),
    (3873, "tab_keyboard.png",         False, "P4 tab_keyboard"),
    # P4 run energy (3)
    (3874, "run_energy_full.png",      False, "P4 run_full"),
    (3875, "run_energy_depleting.png", False, "P4 run_depleting"),
    (3876, "run_energy_exhausted.png", False, "P4 run_exhausted"),
    # P5 login splash (1)
    (3877, "login_splash.png",         False, "P5 login_splash"),
    # P5 dialog 9-slice (9)
    (3878, "dialog_tl.png",            False, "P5 dialog_tl"),
    (3879, "dialog_t.png",             False, "P5 dialog_t"),
    (3880, "dialog_tr.png",            False, "P5 dialog_tr"),
    (3881, "dialog_l.png",             False, "P5 dialog_l"),
    (3882, "dialog_c.png",             False, "P5 dialog_c"),
    (3883, "dialog_r.png",             False, "P5 dialog_r"),
    (3884, "dialog_bl.png",            False, "P5 dialog_bl"),
    (3885, "dialog_b.png",             False, "P5 dialog_b"),
    (3886, "dialog_br.png",            False, "P5 dialog_br"),
    # P6 cursors (4) — hotspots in UI_INTEGRATION.md drive OS-cursor mapping
    (3887, "cursor_walk.png",          False, "P6 cursor_walk"),
    (3888, "cursor_attack.png",        False, "P6 cursor_attack"),
    (3889, "cursor_talk.png",          False, "P6 cursor_talk"),
    (3890, "cursor_use.png",           False, "P6 cursor_use"),
]


def synth_header(w: int, h: int) -> dict:
    """OGRS pack-router-sprites convention: zero shifts, s1/s2=32."""
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


def main() -> int:
    if not ARCHIVE.exists():
        print(f"FATAL: {ARCHIVE} not found", file=sys.stderr)
        return 1
    if not BACKUP.exists():
        shutil.copy2(ARCHIVE, BACKUP)
        print(f"Backed up archive -> {BACKUP}")

    # Read existing entries
    with zipfile.ZipFile(BACKUP, "r") as zin:
        names = zin.namelist()
        entries = {n: zin.read(n) for n in names}

    added = 0
    missing = 0
    for slot, fn, _anchor, label in SLOTS:
        png_path = ART_ROOT / fn
        if not png_path.exists():
            print(f"  WARN: missing {png_path} — slot {slot} not populated")
            missing += 1
            continue
        img = Image.open(png_path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        hdr = synth_header(img.size[0], img.size[1])
        entries[str(slot)] = encode_blob(img, hdr)
        if str(slot) not in names:
            names.append(str(slot))
        added += 1
        print(f"  {slot:4d} <- {fn:<32} ({img.size[0]}x{img.size[1]})  [{label}]")

    # Rewrite archive
    tmp = ARCHIVE.with_suffix(ARCHIVE.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, entries[n])
    tmp.replace(ARCHIVE)

    print(f"\nPacked {added} UI sprites into {ARCHIVE.name}.")
    if missing:
        print(f"  ({missing} missing — check art/items/ui/ for the listed files)")

    mirror = Path("/mnt/c/OGRS/Cache/video/Authentic_Sprites.orsc")
    if mirror.parent.exists():
        shutil.copy2(ARCHIVE, mirror)
        print(f"Mirrored to {mirror}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
