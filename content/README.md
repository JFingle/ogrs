# OGRS content

Everything in `content/` is **data**, not code. NPCs, items, zones, quests, skills, spells, drops, projectiles — all defined as YAML files, validated against schemas, and loaded by the server at startup (eventually with hot-reload).

This is the heart of the project. Most contributions live here.

## Layout

```
content/
├── npcs/           # NPCs and creatures
├── items/          # weapons, armor, consumables, quest items, junk
├── zones/          # new lands (parallel JSON map format)
├── quests/         # quest definitions + dialog trees
├── skills/         # skill action tables, XP curves, level unlocks
├── spells/         # spells, runes, animations, projectile bindings
├── prayers/        # prayer definitions, drain rates, effects
├── projectiles/    # generic projectile entities (sprite, path, impact)
├── drops/          # shared drop tables (referenced by NPCs)
├── shops/          # shop inventories, restock rates
├── events/         # holiday and world events with schedules
└── README.md
```

## Authoring an NPC (current state — schemas evolving)

Today, NPCs use upstream OpenRSC's `NpcDefsCustom.json` format. We will migrate to per-NPC YAML files under `content/npcs/<name>.yaml` during Phase 1.

For now, see `content/npcs/example_custom_npc.yaml` for the target schema and `server/conf/server/defs/NpcDefsCustom.json` for what actually gets loaded.

## Validator

```bash
# Coming online in Phase 0
./tools/content-validator/validate
```

CI runs this on every PR. Schema violations block merge.

## Hot-reload (planned)

In Phase 1, the server gains a `/reload content` admin command and a file-watcher for dev mode. For now, restart the server after content changes.

## Naming conventions

- File names: `snake_case.yaml`
- IDs: `snake_case`, scoped (`ogrs_dragon_lich`, not `dragon_lich`, to avoid collisions with future upstream additions)
- New IDs in additive content **must not** collide with upstream. Current ID strategy for OGRS additions:
  - **NPCs: 836+** (sequential after upstream's last custom NPC at id 835)
  - **Items: next-available** (TBD — Phase 1 audits the item id space)
  - Zone region IDs: 100+
  - **Why sequential, not high-range?** OpenRSC's `EntityHandler.getNpcDef(int)` indexes a `List<NPCDef>` by id. Sparse ids (e.g., 5000) return null → NPEs in spawn code. Phase 1 plans a `HashMap<Integer, NPCDef>` refactor that lets us claim a high reserved range (5000+) safely; until then we use sequential ids starting at 836.
