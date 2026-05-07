#!/usr/bin/env python3
"""OGRS client scenery (GameObject) table codegen.

Mirrors `codegen-client-npcs.py` for scenery. Reads
`content/scenery/*.yaml`, sorts by declared id, validates ids are
sequential, emits Java source at:

    client/src/com/openrsc/client/entityhandling/generated/OgrsClientScenery.java

The generated class exposes a single static `register(objects, nextId) -> int`
that the client's `EntityHandler.java` calls in place of hand-coded
`objects.add(new GameObjectDef(...))` calls. Adding a new scenery becomes
a single YAML file plus a re-run of this script.

Usage:
    python3 tools/codegen-client-scenery.py
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
SCENERY_DIR = REPO_ROOT / "content" / "scenery"
OUTPUT = REPO_ROOT / "client" / "src" / "com" / "openrsc" / "client" / "entityhandling" / "generated" / "OgrsClientScenery.java"


def emit_java(scenery: list[dict]) -> str:
    lines: list[str] = []
    lines.append("// === GENERATED FILE — DO NOT EDIT BY HAND ===")
    lines.append("// Source: content/scenery/*.yaml")
    lines.append("// Regenerate: python3 tools/codegen-client-scenery.py")
    lines.append("")
    lines.append("package com.openrsc.client.entityhandling.generated;")
    lines.append("")
    lines.append("import com.openrsc.client.entityhandling.defs.GameObjectDef;")
    lines.append("import java.util.ArrayList;")
    lines.append("")
    lines.append("public final class OgrsClientScenery {")
    lines.append("")
    lines.append("\tprivate OgrsClientScenery() { /* no instances */ }")
    lines.append("")
    lines.append("\t/**")
    lines.append("\t * Append every OGRS YAML-defined scenery def to the client's")
    lines.append("\t * GameObjectDef list, keeping id == list-index alignment with the")
    lines.append("\t * server-side append order. Returns the next free id. Caller threads")
    lines.append("\t * `i` through:")
    lines.append("\t *   <pre>i = OgrsClientScenery.register(objects, i);</pre>")
    lines.append("\t */")
    lines.append("\tpublic static int register(final ArrayList<GameObjectDef> objects, int i) {")
    lines.append("")

    for s in scenery:
        name = s["name"]
        desc = s.get("description", "")
        c1 = s.get("command1", "WalkTo")
        c2 = s.get("command2", "Examine")
        type_ = int(s.get("type", 1))
        width = int(s.get("width", 1))
        height = int(s.get("height", 1))
        gv = int(s.get("ground_item_var", 0))
        model = s["model"]

        def esc(t: str) -> str:
            return t.replace("\\", "\\\\").replace("\"", "\\\"")

        lines.append(f"\t\t// id {s['id']} — from content/scenery/{s['_source']}")
        lines.append(
            "\t\tobjects.add(new GameObjectDef("
            f"\"{esc(name)}\", \"{esc(desc)}\", \"{esc(c1)}\", \"{esc(c2)}\", "
            f"{type_}, {width}, {height}, {gv}, \"{esc(model)}\", ++i));"
        )
        lines.append("")

    lines.append("\t\treturn i;")
    lines.append("\t}")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not SCENERY_DIR.is_dir():
        print(f"OK — {SCENERY_DIR} does not exist; nothing to generate.")
        # Still emit a no-op generated file so the client compiles cleanly.
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(emit_java([]))
        return 0

    files = sorted(SCENERY_DIR.glob("*.yaml"))
    scenery = []
    for f in files:
        with f.open() as fh:
            data = yaml.safe_load(fh)
        if data is None:
            continue
        data["_source"] = f.name
        if "id" not in data:
            print(f"ERROR: {f.name} missing `id`", file=sys.stderr)
            return 1
        scenery.append(data)

    scenery.sort(key=lambda d: d["id"])
    for idx in range(1, len(scenery)):
        if scenery[idx]["id"] != scenery[idx - 1]["id"] + 1:
            print(
                f"ERROR: non-sequential ids: {scenery[idx - 1]['id']} ({scenery[idx - 1]['_source']}) "
                f"-> {scenery[idx]['id']} ({scenery[idx]['_source']})",
                file=sys.stderr,
            )
            return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(emit_java(scenery))
    print(f"OK — wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(scenery)} scenery def(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
