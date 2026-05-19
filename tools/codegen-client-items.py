#!/usr/bin/env python3
"""OGRS client ITEM table codegen.

Reads `content/items/*.yaml`, emits Java source at:

    client/src/com/openrsc/client/entityhandling/generated/OgrsClientItems.java

The generated class exposes `register(items, nextId) -> int` that the
client's `EntityHandler.java` calls after the upstream-coded
`items.add(new ItemDef(...))` block. Adding a new item becomes a single
YAML file plus a re-run of this script.

Sprites: each YAML carries a `sprite: { id, location }` and an optional
`picture_mask`. Reusing an upstream sprite slot with a tint is the
quick-win path — adding genuinely new sprites needs the sprite-archive
work (separate task).

Usage:
    python3 tools/codegen-client-items.py

Run from the repo root. Re-run any time `content/items/*.yaml` changes.

The generated file MUST be committed — it's a build input.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. `pip install pyyaml`", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parents[1]
ITEMS_DIR = REPO_ROOT / "content" / "items"
OUTPUT = REPO_ROOT / "client" / "src" / "com" / "openrsc" / "client" / "entityhandling" / "generated" / "OgrsClientItems.java"


def parse_int(v, default: int = 0) -> int:
    """Decimal int, or 0xAA hex string."""
    if v is None:
        return default
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if s.startswith("0x") or s.startswith("0X"):
        return int(s, 16)
    return int(s)


def jstr(s: str) -> str:
    """Java string-literal escape."""
    return s.replace("\\", "\\\\").replace("\"", "\\\"")


def emit_java(items: list[dict]) -> str:
    out: list[str] = []
    out.append("// === GENERATED FILE — DO NOT EDIT BY HAND ===")
    out.append("// Source: content/items/*.yaml")
    out.append("// Regenerate: python3 tools/codegen-client-items.py")
    out.append("")
    out.append("package com.openrsc.client.entityhandling.generated;")
    out.append("")
    out.append("import com.openrsc.client.entityhandling.defs.ItemDef;")
    out.append("import java.util.ArrayList;")
    out.append("")
    out.append("public final class OgrsClientItems {")
    out.append("")
    out.append("\tprivate OgrsClientItems() { /* no instances */ }")
    out.append("")
    out.append("\t/**")
    out.append("\t * Append every OGRS YAML-defined item to the client's ItemDef list.")
    out.append("\t * Returns the next free id. Caller threads `i` through:")
    out.append("\t *   <pre>i = OgrsClientItems.register(items, i);</pre>")
    out.append("\t * The 14-arg ItemDef constructor signature is:")
    out.append("\t *   (name, description, command, basePrice, spriteID, spriteLocation,")
    out.append("\t *    stackable, wieldable, wearableID, pictureMask, membersItem,")
    out.append("\t *    untradeable, noteable, id)")
    out.append("\t */")
    out.append("\tpublic static int register(final ArrayList<ItemDef> items, int i) {")
    out.append("")

    for item in items:
        name = item["name"]
        desc = item.get("description", "")
        cmd = item.get("command", "") or ""
        sprite = item.get("sprite", {}) or {}
        sprite_id = parse_int(sprite.get("id", 0))
        sprite_loc = sprite.get("location", f"items:{sprite_id}")

        stackable = bool(item.get("stackable", False))
        members = bool(item.get("members_only", False))
        untradeable = bool(item.get("untradeable", False))
        noteable = bool(item.get("noteable", True))
        base_price = parse_int(item.get("base_price", 1))
        picture_mask = parse_int(item.get("picture_mask", 0))
        # OGRS — wieldable items also need a wearable_id (the appearance
        # ID that controls the in-world model when equipped). Server-side
        # weapon stats (aim/power/required-skill) still live in the
        # parallel ItemDefsCustom.json entry; this codegen only handles
        # client-side display.
        wieldable = bool(item.get("wieldable", False))
        wearable_id = parse_int(item.get("wearable_id", 0))

        out.append(f"\t\t// id {item['id']} — from content/items/{item['_source']}")
        out.append(
            "\t\titems.add(new ItemDef("
            f"\"{jstr(name)}\", \"{jstr(desc)}\", \"{jstr(cmd)}\", "
            f"{base_price}, {sprite_id}, \"{jstr(sprite_loc)}\", "
            f"{str(stackable).lower()}, {str(wieldable).lower()}, {wearable_id}, "
            f"0x{picture_mask & 0xFFFFFF:06X}, "
            f"{str(members).lower()}, {str(untradeable).lower()}, {str(noteable).lower()}, "
            "i++));"
        )
        out.append("")

    out.append("\t\treturn i;")
    out.append("\t}")
    out.append("}")
    out.append("")
    return "\n".join(out)


def main() -> int:
    if not ITEMS_DIR.is_dir():
        print(f"ERROR: {ITEMS_DIR} not found", file=sys.stderr)
        return 1

    files = sorted(ITEMS_DIR.glob("*.yaml"))
    items: list[dict] = []
    for f in files:
        with f.open() as fh:
            data = yaml.safe_load(fh)
        if data is None:
            continue
        data["_source"] = f.name
        if "id" not in data:
            print(f"ERROR: {f.name} is missing `id`", file=sys.stderr)
            return 1
        items.append(data)

    items.sort(key=lambda d: d["id"])
    # Sequential constraint — mirrors server-side loader.
    for idx in range(1, len(items)):
        if items[idx]["id"] != items[idx - 1]["id"] + 1:
            print(
                f"ERROR: non-sequential ids: {items[idx - 1]['id']} ({items[idx - 1]['_source']}) "
                f"-> {items[idx]['id']} ({items[idx]['_source']})",
                file=sys.stderr,
            )
            return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(emit_java(items))
    print(f"OK — wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(items)} item(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
