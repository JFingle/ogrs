#!/usr/bin/env python3
"""OGRS — generate the thief-wearables + dragonhide wearable batches.

Reads the two paperdoll mapping specs in art/_specs/ as the source of
truth (alphabetical item order locks the ID allocation) and emits:

  - 34 YAML item definitions in content/items/
  - The AnimationDef Java block to paste into the client's
    EntityHandler.java (printed to stdout — review then patch by hand)
  - A registered sprite-pack manifest entry so build-cache-bundle.sh
    picks the new icons up

ID allocations (block-reserved 2026-05-25; do NOT change after items
ship — players will have these in their inventories):

  item_id:        1705-1738
  sprite.id:      1265-1298     (cache slots 3415-3448)
  wearable_id:    600-633       (AnimationDef indices, post-vanilla)

If you need to ship more wearables later, start the next block from
1739 / 1299 / 634 to avoid colliding with these.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parents[2]
CONTENT_ITEMS = REPO / "content" / "items"


class Wearable(NamedTuple):
    sprite_file: str        # e.g. "brown_hood.png"
    sprite_dir: str         # e.g. "thief_wearables" (under art/items/)
    display_name: str       # in-game item name
    description: str        # in-game hover description
    wear_slot: int          # 0=head 1=body 2=legs 3=cape 9=hands 10=feet
    template: str           # vanilla AnimationDef sprite template
    picture_mask: int       # RGB int used for both icon tint and worn tint
    required_skill: int     # 0 = no skill gate; 5 = ranged
    required_level: int     # level on required_skill needed to wield
    armour_bonus: int       # defensive bonus
    ranger_bonus: int       # ranged accuracy/power (dragonhide)
    base_price: int


# Thief wearables — order matches alphabetical-sorted file listing so
# brown_boots is the first ID and rogue_top is the last of this batch.
THIEF_WEARABLES: list[Wearable] = [
    Wearable("brown_boots.png",   "thief_wearables", "Brown Thief Boots",   "Soft leather boots for quiet feet.",            10, "boots",         0x6C4828, 0, 1, 1, 0,  200),
    Wearable("brown_bottom.png",  "thief_wearables", "Brown Thief Chaps",   "Brown leather chaps. Comfortable in alleyways.",  2, "leatherchaps",  0x8C6438, 0, 1, 1, 0,  300),
    Wearable("brown_cape.png",    "thief_wearables", "Brown Thief Cape",    "A plain brown cape — easy to disappear into.",    3, "cape",          0x8C6438, 0, 1, 0, 0,  150),
    Wearable("brown_gloves.png",  "thief_wearables", "Brown Thief Gloves",  "Fingerless leather gloves for nimble work.",      9, "leathergloves", 0x6C4828, 0, 1, 1, 0,  120),
    Wearable("brown_hood.png",    "thief_wearables", "Brown Thief Hood",    "A modest hood that hides your face.",             0, "hood1",         0x6C4828, 0, 1, 1, 0,  180),
    Wearable("brown_top.png",     "thief_wearables", "Brown Thief Vest",    "A worn leather vest, brown as forest dirt.",      1, "leathervest",   0x8C6438, 0, 1, 2, 0,  400),

    Wearable("master_boots.png",  "thief_wearables", "Master Thief Boots",  "Boots so silent they whisper to the floor.",    10, "boots",         0x1A1810, 0, 50, 3, 0, 12000),
    Wearable("master_bottom.png", "thief_wearables", "Master Thief Chaps",  "Charcoal chaps with hidden pockets.",            2, "leatherchaps",  0x1F1A0C, 0, 50, 3, 0, 18000),
    Wearable("master_cape.png",   "thief_wearables", "Master Thief Cape",   "A master thief's cape, blacker than night.",     3, "thievingcape",  0x1F1A0C, 0, 50, 1, 0,  9000),
    Wearable("master_gloves.png", "thief_wearables", "Master Thief Gloves", "Gloves so fine you can feel a coin's date.",     9, "leathergloves", 0x1A1810, 0, 50, 3, 0,  7200),
    Wearable("master_hood.png",   "thief_wearables", "Master Thief Hood",   "A hood that drinks the light.",                  0, "evilhoodie",    0x1A1810, 0, 50, 3, 0, 10800),
    Wearable("master_top.png",    "thief_wearables", "Master Thief Doublet","A reinforced doublet, midnight-black with faint gold warmth.", 1, "leatherarmour", 0x1F1A0C, 0, 50, 4, 0, 24000),

    Wearable("rogue_boots.png",   "thief_wearables", "Rogue Boots",         "Worn black boots a rogue would die in.",        10, "boots",         0x1A1A20, 0, 25, 2, 0,  3000),
    Wearable("rogue_bottom.png",  "thief_wearables", "Rogue Chaps",         "Dark leather chaps stained with city soot.",     2, "leatherchaps",  0x202028, 0, 25, 2, 0,  4500),
    Wearable("rogue_cape.png",    "thief_wearables", "Rogue Cape",          "A dark cape stained with a faint copper smell.", 3, "cape",          0x3A1010, 0, 25, 1, 0,  2250),
    Wearable("rogue_gloves.png",  "thief_wearables", "Rogue Gloves",        "Dark fingerless gloves with reinforced palms.",  9, "leathergloves", 0x1A1A20, 0, 25, 2, 0,  1800),
    Wearable("rogue_hood.png",    "thief_wearables", "Rogue Hood",          "A sinister hood. Few who see it live to recall.", 0, "evilhoodie",    0x1A1A20, 0, 25, 2, 0,  2700),
    Wearable("rogue_top.png",     "thief_wearables", "Rogue Vest",          "A dark leather vest for the working criminal.",  1, "leathervest",   0x202028, 0, 25, 3, 0,  6000),
]

# Dragonhide — alphabetical (black/blue/green/red) × (body/chaps/coif/vambraces).
# Ranged skill id = 5. Tier levels: green 40, blue 50, red 60, black 70.
DRAGONHIDE: list[Wearable] = [
    Wearable("black_d_hide_body.png",       "dragonhide", "Black Dragonhide Body",       "A leather body made from black dragonhide.",       1, "leatherarmour", 0x384048, 5, 70, 6, 18, 16000),
    Wearable("black_d_hide_chaps.png",      "dragonhide", "Black Dragonhide Chaps",      "Form-fitting chaps cut from black dragonhide.",    2, "leatherchaps",  0x384048, 5, 70, 5, 16, 12000),
    Wearable("black_d_hide_coif.png",       "dragonhide", "Black Dragonhide Coif",       "A hooded coif lined with black dragonhide.",       0, "hood1",         0x384048, 5, 70, 3, 10,  6000),
    Wearable("black_d_hide_vambraces.png",  "dragonhide", "Black Dragonhide Vambraces",  "Forearm guards plated with black dragonhide.",     9, "leathergloves", 0x384048, 5, 70, 3, 12,  5000),

    Wearable("blue_d_hide_body.png",        "dragonhide", "Blue Dragonhide Body",        "A leather body made from blue dragonhide.",        1, "leatherarmour", 0x3070C8, 5, 50, 5, 14,  9000),
    Wearable("blue_d_hide_chaps.png",       "dragonhide", "Blue Dragonhide Chaps",       "Form-fitting chaps cut from blue dragonhide.",     2, "leatherchaps",  0x3070C8, 5, 50, 4, 12,  6800),
    Wearable("blue_d_hide_coif.png",        "dragonhide", "Blue Dragonhide Coif",        "A hooded coif lined with blue dragonhide.",        0, "hood1",         0x3070C8, 5, 50, 2,  8,  3400),
    Wearable("blue_d_hide_vambraces.png",   "dragonhide", "Blue Dragonhide Vambraces",   "Forearm guards plated with blue dragonhide.",      9, "leathergloves", 0x3070C8, 5, 50, 2,  9,  2800),

    Wearable("green_d_hide_body.png",       "dragonhide", "Green Dragonhide Body",       "A leather body made from green dragonhide.",       1, "leatherarmour", 0x388928, 5, 40, 4, 12,  4000),
    Wearable("green_d_hide_chaps.png",      "dragonhide", "Green Dragonhide Chaps",      "Form-fitting chaps cut from green dragonhide.",    2, "leatherchaps",  0x388928, 5, 40, 3, 10,  3000),
    Wearable("green_d_hide_coif.png",       "dragonhide", "Green Dragonhide Coif",       "A hooded coif lined with green dragonhide.",       0, "hood1",         0x388928, 5, 40, 2,  7,  1500),
    Wearable("green_d_hide_vambraces.png",  "dragonhide", "Green Dragonhide Vambraces",  "Forearm guards plated with green dragonhide.",     9, "leathergloves", 0x388928, 5, 40, 2,  8,  1200),

    Wearable("red_d_hide_body.png",         "dragonhide", "Red Dragonhide Body",         "A leather body made from red dragonhide.",         1, "leatherarmour", 0xA82828, 5, 60, 5, 16, 12000),
    Wearable("red_d_hide_chaps.png",        "dragonhide", "Red Dragonhide Chaps",        "Form-fitting chaps cut from red dragonhide.",      2, "leatherchaps",  0xA82828, 5, 60, 4, 14,  9000),
    Wearable("red_d_hide_coif.png",         "dragonhide", "Red Dragonhide Coif",         "A hooded coif lined with red dragonhide.",         0, "hood1",         0xA82828, 5, 60, 3,  9,  4500),
    Wearable("red_d_hide_vambraces.png",    "dragonhide", "Red Dragonhide Vambraces",    "Forearm guards plated with red dragonhide.",       9, "leathergloves", 0xA82828, 5, 60, 2, 10,  3800),
]

ALL: list[Wearable] = THIEF_WEARABLES + DRAGONHIDE

# ID block reservations — assigned in list order, 1-1 with the items
# above. Burned in here so re-running the generator yields the same
# IDs even if you reorder the lists in code (which you shouldn't).
ITEM_ID_BASE     = 1705
# Sprite IDs 600-633 (cache slots 2750-2783) — chosen because:
#   1. They're inside the upstream cache's only big empty run (slot
#      2636-3149 / sprite.id 486-999), so we don't overwrite vanilla data.
#   2. They sit BELOW the entity-template loader's 3300+ range, so the
#      entity load pass won't stomp them after items load.
#   3. They mirror the wearable_id 600-633 range, which is a useful
#      mnemonic — sprite.id N → wearable_id N for each item in this batch.
SPRITE_ID_BASE   = 600
WEARABLE_ID_BASE = 600


def yaml_path(w: Wearable) -> Path:
    """Filename = sprite stem prefixed with category so they sort with
    siblings (thief_*.yaml lives next to other thieving items)."""
    stem = w.sprite_file[:-4]
    if w.sprite_dir == "thief_wearables":
        return CONTENT_ITEMS / f"thief_wearable_{stem}.yaml"
    if w.sprite_dir == "dragonhide":
        return CONTENT_ITEMS / f"ranger_{stem}.yaml"
    raise ValueError(w.sprite_dir)


def emit_yamls() -> int:
    written = 0
    for idx, w in enumerate(ALL):
        item_id    = ITEM_ID_BASE + idx
        sprite_id  = SPRITE_ID_BASE + idx
        wearable_id = WEARABLE_ID_BASE + idx
        out = yaml_path(w)
        if out.exists():
            print(f"  SKIP {out.name} (exists)")
            continue
        out.write_text(
            f"# OGRS wearable — {w.display_name}.\n"
            f"# Paperdoll batch 2026-05-25 (sparky). Vanilla template + pictureMask\n"
            f"# tint — no new worn-sprite art. See art/_specs/PAPERDOLL_MAPPING*.md\n"
            f"# and scripts/art/gen-wearables-batch.py for the full mapping table.\n"
            f"#\n"
            f"# Template: {w.template}   pictureMask: #{w.picture_mask:06X}  ({w.picture_mask})\n"
            f"# Inventory icon: art/items/{w.sprite_dir}/{w.sprite_file}\n"
            f"\n"
            f"id: {item_id}\n"
            f"name: {w.display_name}\n"
            f"description: {w.description}\n"
            f'command: ""\n'
            f"stackable: false\n"
            f"untradeable: false\n"
            f"members_only: false\n"
            f"noteable: true\n"
            f"base_price: {w.base_price}\n"
            f"picture_mask: 0x{w.picture_mask:06X}\n"
            f"wieldable: true\n"
            f"wearable_id: {wearable_id}\n"
            f"weapon:\n"
            f"  appearance_id: {wearable_id}\n"
            f"  wearable_id: {wearable_id}\n"
            f"  wear_slot: {w.wear_slot}\n"
            f"  required_skill: {w.required_skill}\n"
            f"  required_level: {w.required_level}\n"
            f"  armour_bonus: {w.armour_bonus}\n"
            + (f"  power_bonus: {w.ranger_bonus}   # ranged accuracy/power\n" if w.ranger_bonus else "")
            + f"sprite:\n"
            f"  id: {sprite_id}\n"
            f'  location: "items:{sprite_id}"\n'
        )
        written += 1
        print(f"  WROTE {out.name}")
    return written


def emit_animation_block() -> str:
    """The Java block to paste into client EntityHandler.java just
    after the last vanilla AnimationDef (index 558 = "amulet"). We
    leave a 41-index gap (559-599) so upstream can add more vanilla
    animations without colliding with our block."""
    lines = []
    lines.append("\t\t// OGRS wearables batch 2026-05-25 (sparky). Indices 600-633.")
    lines.append("\t\t// Gap 559-599 reserved for upstream merges. Order matches the")
    lines.append("\t\t// scripts/art/gen-wearables-batch.py mapping; do not reshuffle.")
    lines.append("\t\twhile (animations.size() < 600) {")
    lines.append("\t\t\tanimations.add(new AnimationDef(\"head1\", \"player\", 0, 0, true, false, 0));")
    lines.append("\t\t}")
    for idx, w in enumerate(ALL):
        wid = WEARABLE_ID_BASE + idx
        comment_name = f"{w.sprite_file[:-4]} ({w.display_name})"
        lines.append(
            f'\t\tanimations.add(new AnimationDef("{w.template}", "equipment", '
            f'{w.picture_mask}, 0, true, false, 0)); //{wid}  {comment_name}'
        )
    return "\n".join(lines)


def emit_sprite_pack_manifest() -> str:
    """Output a Python dict the sprite-pack script can consume directly."""
    rows = ["WEARABLES_BATCH = ["]
    for idx, w in enumerate(ALL):
        sprite_id = SPRITE_ID_BASE + idx
        rows.append(
            f'    ({sprite_id}, "{w.sprite_dir}/{w.sprite_file}"),'
        )
    rows.append("]")
    return "\n".join(rows)


if __name__ == "__main__":
    print("[gen-wearables] Generating YAMLs...")
    n = emit_yamls()
    print(f"[gen-wearables] {n} YAMLs written ({len(ALL)} total in batch).\n")
    print("[gen-wearables] AnimationDef Java block (paste after //558 in EntityHandler.java):")
    print()
    print(emit_animation_block())
    print()
    print("[gen-wearables] Sprite-pack manifest (for pack-wearables-batch.py):")
    print()
    print(emit_sprite_pack_manifest())
