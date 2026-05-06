#!/usr/bin/env python3
"""OGRS content validator.

Walks `content/` and validates each YAML file against its schema.
Run from repo root:

    python tools/content-validator/validate.py

Exit code 0 = clean, 1 = at least one error.

This is a stub. Real schemas land in Phase 1 alongside the data-driven
NPC/quest/skill loaders. For now we validate basic shape:
  - YAML parses
  - top-level `id` and `name` exist on every content file
  - no duplicate ids within a content type
  - reserved id ranges respected (NPCs >= 5000, items >= 10000, regions >= 100)
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

# Reserved ID ranges for OGRS additions. Ranges may shift; check content/README.md.
RESERVED_MIN = {
    "npcs": 5000,
    "items": 10000,
    # zones: region id, validated separately
}


def collect_files() -> dict[str, list[Path]]:
    out: dict[str, list[Path]] = defaultdict(list)
    if not CONTENT.exists():
        return out
    for sub in sorted(CONTENT.iterdir()):
        if not sub.is_dir():
            continue
        for f in sorted(sub.rglob("*.yaml")):
            out[sub.name].append(f)
    return out


def validate_one(kind: str, path: Path, errors: list[str], seen_ids: dict[str, set]) -> None:
    rel = path.relative_to(REPO_ROOT)
    try:
        with path.open() as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as e:
        errors.append(f"{rel}: YAML parse error: {e}")
        return
    if data is None:
        return  # empty placeholder is fine
    if not isinstance(data, dict):
        errors.append(f"{rel}: top-level must be a mapping")
        return

    if "id" not in data:
        errors.append(f"{rel}: missing 'id'")
    if "name" not in data:
        errors.append(f"{rel}: missing 'name'")

    # Reserved id range
    if kind in RESERVED_MIN and isinstance(data.get("id"), int):
        if data["id"] < RESERVED_MIN[kind]:
            errors.append(
                f"{rel}: numeric id {data['id']} below reserved minimum "
                f"{RESERVED_MIN[kind]} for {kind}"
            )

    # Region check for zones
    if kind == "zones" and isinstance(data.get("region"), int):
        if data["region"] < 100:
            errors.append(
                f"{rel}: zone region {data['region']} below reserved minimum 100"
            )

    # Duplicate ids
    nid = data.get("id")
    if nid is not None:
        if nid in seen_ids[kind]:
            errors.append(f"{rel}: duplicate id {nid!r} within {kind}/")
        seen_ids[kind].add(nid)


def main() -> int:
    errors: list[str] = []
    seen_ids: dict[str, set] = defaultdict(set)
    files = collect_files()
    if not files:
        print("No content/ files yet — nothing to validate.")
        return 0

    total = 0
    for kind, paths in files.items():
        for p in paths:
            if p.name.startswith("."):
                continue
            total += 1
            validate_one(kind, p, errors, seen_ids)

    if errors:
        print(f"FAIL — {len(errors)} error(s) across {total} file(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK — {total} content file(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
