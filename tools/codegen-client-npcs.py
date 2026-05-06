#!/usr/bin/env python3
"""OGRS client NPC table codegen.

Reads `content/npcs/*.yaml`, emits Java source at:

    client/src/com/openrsc/client/entityhandling/generated/OgrsClientNpcs.java

The generated class exposes a single static `register(npcs, nextId) -> int`
that the client's `EntityHandler.java` calls in place of the hand-coded
`npcs.add(new NPCDef(...))` block. Adding a new NPC becomes a single YAML
file plus a re-run of this script.

Usage:
    python3 tools/codegen-client-npcs.py

Run from the repo root. Re-run any time `content/npcs/*.yaml` changes.

The generated file MUST be committed — it's a build input. The header marks
it "DO NOT EDIT" so reviewers don't waste time on hand changes.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. `pip install pyyaml`", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parents[1]
NPCS_DIR = REPO_ROOT / "content" / "npcs"
OUTPUT = REPO_ROOT / "client" / "src" / "com" / "openrsc" / "client" / "entityhandling" / "generated" / "OgrsClientNpcs.java"


def to_int_list(v) -> list[int]:
    if not isinstance(v, list) or len(v) != 12:
        raise ValueError(f"sprites must be a 12-entry list, got {v!r}")
    return [int(x) for x in v]


def parse_color(v) -> int:
    """Decimal int, or 0xAA hex string."""
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if s.startswith("0x") or s.startswith("0X"):
        return int(s, 16)
    return int(s)


def emit_java(npcs: list[dict]) -> str:
    lines: list[str] = []
    lines.append("// === GENERATED FILE — DO NOT EDIT BY HAND ===")
    lines.append("// Source: content/npcs/*.yaml")
    lines.append("// Regenerate: python3 tools/codegen-client-npcs.py")
    lines.append("// See backlog #6(a) — build-time codegen for the client NPC table.")
    lines.append("")
    lines.append("package com.openrsc.client.entityhandling.generated;")
    lines.append("")
    lines.append("import com.openrsc.client.entityhandling.defs.NPCDef;")
    lines.append("import java.util.ArrayList;")
    lines.append("")
    lines.append("public final class OgrsClientNpcs {")
    lines.append("")
    lines.append("\tprivate OgrsClientNpcs() { /* no instances */ }")
    lines.append("")
    lines.append("\t/**")
    lines.append("\t * Append every OGRS YAML-defined NPC to the client's NPCDef list,")
    lines.append("\t * keeping id == list-index alignment with the server-side load order.")
    lines.append("\t * Returns the next free id. Caller threads `i` through:")
    lines.append("\t *   <pre>i = OgrsClientNpcs.register(npcs, i);</pre>")
    lines.append("\t */")
    lines.append("\tpublic static int register(final ArrayList<NPCDef> npcs, int i) {")
    lines.append("\t\tint[] sprites;")
    lines.append("")

    for npc in npcs:
        name = npc["name"]
        desc = npc.get("description", "")
        cmd = npc.get("command", "")
        cmd2 = npc.get("command2", "")
        stats = npc.get("stats", {}) or {}
        flags = npc.get("flags", {}) or {}
        colors = npc.get("colors", {}) or {}
        camera = npc.get("camera", {}) or {}
        models = npc.get("models", {}) or {}

        att = int(stats.get("attack", 0))
        st = int(stats.get("strength", 0))
        hits = int(stats.get("hits", 1))
        deff = int(stats.get("defense", 0))
        ranged = bool(stats.get("ranged", False))

        sprites = to_int_list(npc["sprites"])
        hair = parse_color(colors.get("hair", 0))
        top = parse_color(colors.get("top", 0))
        bottom = parse_color(colors.get("bottom", 0))
        skin = parse_color(colors.get("skin", 15523536))

        cam_x = int(camera.get("x", 160))
        cam_y = int(camera.get("y", 220))
        walk = int(models.get("walk", 6))
        combat = int(models.get("combat", 6))
        combat_sprite = int(models.get("combat_sprite", 5))

        # Java string escaping
        name_j = name.replace("\\", "\\\\").replace("\"", "\\\"")
        desc_j = desc.replace("\\", "\\\\").replace("\"", "\\\"")
        cmd_j = cmd.replace("\\", "\\\\").replace("\"", "\\\"")
        cmd2_j = cmd2.replace("\\", "\\\\").replace("\"", "\\\"")

        lines.append(f"\t\t// id {npc['id']} — from content/npcs/{npc['_source']}")
        lines.append(f"\t\tsprites = new int[]{{{', '.join(str(s) for s in sprites)}}};")
        if cmd2:
            # Emit the 6-arg-prefix constructor with both commands, so the
            # right-click menu shows BOTH options on this NPC.
            lines.append(
                "\t\tnpcs.add(new NPCDef("
                f"\"{name_j}\", \"{desc_j}\", \"{cmd_j}\", \"{cmd2_j}\", "
                f"{att}, {st}, {hits}, {deff}, {str(ranged).lower()}, sprites, "
                f"0x{hair & 0xFFFFFF:06X}, 0x{top & 0xFFFFFF:06X}, 0x{bottom & 0xFFFFFF:06X}, 0x{skin & 0xFFFFFF:06X}, "
                f"{cam_x}, {cam_y}, {walk}, {combat}, {combat_sprite}, i++));"
            )
        else:
            lines.append(
                "\t\tnpcs.add(new NPCDef("
                f"\"{name_j}\", \"{desc_j}\", \"{cmd_j}\", "
                f"{att}, {st}, {hits}, {deff}, {str(ranged).lower()}, sprites, "
                f"0x{hair & 0xFFFFFF:06X}, 0x{top & 0xFFFFFF:06X}, 0x{bottom & 0xFFFFFF:06X}, 0x{skin & 0xFFFFFF:06X}, "
                f"{cam_x}, {cam_y}, {walk}, {combat}, {combat_sprite}, i++));"
            )
        lines.append("")

    lines.append("\t\treturn i;")
    lines.append("\t}")
    lines.append("}")
    lines.append("")  # trailing newline
    return "\n".join(lines)


def main() -> int:
    if not NPCS_DIR.is_dir():
        print(f"ERROR: {NPCS_DIR} not found", file=sys.stderr)
        return 1

    files = sorted(NPCS_DIR.glob("*.yaml"))
    npcs = []
    for f in files:
        with f.open() as fh:
            data = yaml.safe_load(fh)
        if data is None:
            continue
        data["_source"] = f.name
        if "id" not in data:
            print(f"ERROR: {f.name} is missing `id`", file=sys.stderr)
            return 1
        npcs.append(data)

    npcs.sort(key=lambda d: d["id"])
    # Sanity: ids must be sequential — same constraint as the server-side loader.
    for idx in range(1, len(npcs)):
        if npcs[idx]["id"] != npcs[idx - 1]["id"] + 1:
            print(
                f"ERROR: non-sequential ids: {npcs[idx - 1]['id']} ({npcs[idx - 1]['_source']}) "
                f"-> {npcs[idx]['id']} ({npcs[idx]['_source']})",
                file=sys.stderr,
            )
            return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(emit_java(npcs))
    print(f"OK — wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(npcs)} NPC(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
