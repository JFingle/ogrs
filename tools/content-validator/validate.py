#!/usr/bin/env python3
"""OGRS content validator.

Walks `content/` and validates each YAML file. Run from repo root:

    python tools/content-validator/validate.py

Exit code 0 = clean, 1 = at least one error.

File shapes recognised:

  * `npcs/<name>.yaml` — single-entity, requires `id` (>=836) and `name`.
  * `skills/slayer/tasks.yaml` — container, expects a `tasks: [...]` list
    where each entry has `name` and `npc_ids: [...]`.
  * Other dirs — single-entity by default, requires `id` and `name`.

This is intentionally simple. Phase 1 will replace it with JSON-Schema
validation once the schemas are stable.
"""
from __future__ import annotations

import sys
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. `pip install pyyaml`", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTENT = REPO_ROOT / "content"

# Lowest legal id for OGRS additions per kind.
# Until backlog #9 (EntityHandler HashMap refactor), NPC ids must be sequential
# starting after upstream's last (id 835); first OGRS slot is 836.
RESERVED_MIN = {
    "npcs": 836,
    "items": 10000,
}

CONTAINER_FILES = {
    ("skills", "tasks.yaml"): "slayer_tasks",
}


def kind_of(p: Path) -> str:
    rel = p.relative_to(CONTENT)
    return rel.parts[0]  # top-level dir under content/


def container_kind(p: Path) -> str | None:
    rel = p.relative_to(CONTENT)
    parts = rel.parts
    if len(parts) >= 2 and (parts[0], parts[-1]) in CONTAINER_FILES:
        return CONTAINER_FILES[(parts[0], parts[-1])]
    return None


def validate_single_entity(kind: str, path: Path, data, errors, seen_ids):
    rel = path.relative_to(REPO_ROOT)
    if not isinstance(data, dict):
        errors.append(f"{rel}: top-level must be a mapping")
        return
    if "id" not in data:
        errors.append(f"{rel}: missing 'id'")
    if "name" not in data:
        errors.append(f"{rel}: missing 'name'")

    if kind in RESERVED_MIN and isinstance(data.get("id"), int):
        if data["id"] < RESERVED_MIN[kind]:
            errors.append(
                f"{rel}: numeric id {data['id']} below reserved minimum "
                f"{RESERVED_MIN[kind]} for {kind}"
            )
    nid = data.get("id")
    if nid is not None:
        if nid in seen_ids[kind]:
            errors.append(f"{rel}: duplicate id {nid!r} within {kind}/")
        seen_ids[kind].add(nid)


def validate_slayer_tasks(path: Path, data, errors):
    rel = path.relative_to(REPO_ROOT)
    if not isinstance(data, dict) or "tasks" not in data:
        errors.append(f"{rel}: expected top-level mapping with `tasks: [...]`")
        return
    tasks = data["tasks"]
    if not isinstance(tasks, list):
        errors.append(f"{rel}: `tasks` must be a list")
        return
    seen_names = set()
    for i, t in enumerate(tasks):
        ctx = f"{rel}[task #{i}]"
        if not isinstance(t, dict):
            errors.append(f"{ctx}: must be a mapping")
            continue
        name = t.get("name")
        npc_ids = t.get("npc_ids")
        if not name:
            errors.append(f"{ctx}: missing `name`")
        elif name in seen_names:
            errors.append(f"{ctx}: duplicate `name` {name!r}")
        else:
            seen_names.add(name)
        if not isinstance(npc_ids, list) or not npc_ids:
            errors.append(f"{ctx} ({name}): `npc_ids` must be a non-empty list")
        elif not all(isinstance(x, int) for x in npc_ids):
            errors.append(f"{ctx} ({name}): all `npc_ids` must be integers")
        count = t.get("count")
        if count is not None:
            if not isinstance(count, dict):
                errors.append(f"{ctx} ({name}): `count` must be a mapping {{min, max}}")
            else:
                mn, mx = count.get("min"), count.get("max")
                if not isinstance(mn, int) or not isinstance(mx, int):
                    errors.append(f"{ctx} ({name}): `count.min` and `count.max` must be ints")
                elif mx < mn:
                    errors.append(f"{ctx} ({name}): count.max ({mx}) < count.min ({mn})")


def main() -> int:
    errors: list[str] = []
    seen_ids: dict[str, set] = defaultdict(set)

    if not CONTENT.exists():
        print("No content/ — nothing to validate.")
        return 0

    files = sorted(CONTENT.rglob("*.yaml"))
    if not files:
        print("No YAML files in content/ — nothing to validate.")
        return 0

    for f in files:
        if f.name.startswith("."):
            continue
        try:
            with f.open() as fh:
                data = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            errors.append(f"{f.relative_to(REPO_ROOT)}: YAML parse error: {e}")
            continue
        if data is None:
            continue

        cont = container_kind(f)
        if cont == "slayer_tasks":
            validate_slayer_tasks(f, data, errors)
        else:
            validate_single_entity(kind_of(f), f, data, errors, seen_ids)

    if errors:
        print(f"FAIL — {len(errors)} error(s) across {len(files)} file(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK — {len(files)} content file(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
