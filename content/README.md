# OGRS content

Everything in `content/` is **data**, not code. Add a file, restart the server, and a new NPC / item / quest / skill / slayer task / dialog tree / spell appears in the world. (Most of these are still being wired up — see status table below.)

## Layout

```
content/
├── npcs/                 NPC definitions, one YAML per creature
├── items/                weapons, armor, consumables — coming
├── zones/                new lands, parallel JSON map system — coming
├── quests/               quest definitions + dialog trees — coming
├── skills/
│   └── slayer/
│       └── tasks.yaml    slayer task pool (single shared file)
├── spells/               — coming
├── prayers/              — coming
├── projectiles/          — coming
├── dialog/               NPC dialog trees — coming
├── drops/                shared drop tables — coming
├── shops/                shop inventories — coming
└── events/               holiday + world events — coming
```

## What's wired up today (2026-05-06)

| Type | Authoring location | Hot-reload? | Client work also needed? |
|---|---|---|---|
| **NPCs** | `content/npcs/<name>.yaml` | No, restart | ⚠️ Yes — also add to `client/src/.../EntityHandler.java` (see backlog #6) |
| **Slayer tasks** | `content/skills/slayer/tasks.yaml` | No, restart | ❌ No — tasks are server-only |
| Items | `server/conf/server/defs/ItemDefsCustom.json` (legacy) | No | ⚠️ Yes (similar story to NPCs) |
| Quests | Hardcoded Java plugins (legacy) | No, recompile | ❌ No |
| Skills (registry) | Hardcoded Java enum (legacy) | No, recompile | ⚠️ Yes (skill panel UI) |
| Zones / maps | Binary `.jag` (upstream) | No | n/a |
| Dialog | Hardcoded Java plugins (legacy) | No, recompile | ❌ No |

## Adding a new NPC

1. **Pick the next sequential id.** Open the project memory — until backlog #9 (EntityHandler HashMap refactor) lands, NPC ids must be sequential. Today the next available id is determined by `npcs.size()` at YAML-load time. Currently that's **837** (794 stock + 42 upstream-custom + 1 OGRS YAML).
2. **Create `content/npcs/<snake_case_name>.yaml`** mirroring the schema in `grizzled_traveler.yaml`.
3. **Add the matching client-side entry** to `client/src/com/openrsc/client/entityhandling/EntityHandler.java` near the existing `npcs.add(new NPCDef(...))` block. Without this, the client falls back to "Ana (not in a barrel)" with the helpful "I should update my client" hint.
4. **Add a spawn** in `server/conf/server/defs/locs/NpcLocsCustom.json` if you want the NPC to appear in the world.
5. **Optionally add a Talk-to plugin** under `server/plugins/com/openrsc/server/plugins/custom/npcs/` implementing `TalkNpcTrigger`. (See `GrizzledTraveler.java`.)
6. **Restart server, rebuild client.**

## Adding a new slayer task

Easiest content addition right now — single YAML edit, one server restart. No code, no client.

1. Open `content/skills/slayer/tasks.yaml`.
2. Append an entry:
   ```yaml
   - name: Cow
     npc_ids: [6]                 # all NPC defs that count for this task
     count: { min: 8, max: 12 }
     area: lumbridge              # narrative hint, not yet enforced
   ```
3. **Family ids matter.** Most creatures have multiple defs in `NpcDefs.json` (Goblin alone is 5). Look up every variant and list them all, otherwise kills won't register. Quick check:
   ```bash
   python3 -c "
   import json
   with open('server/conf/server/defs/NpcDefs.json') as f:
       for n in json.load(f)['npcs']:
           if 'cow' in n['name'].lower():
               print(f\"id={n['id']:4d} {n['name']} attackable={n.get('attackable')}\")"
   ```
4. Restart server. Talk to a Slayer Master. The new task is in the random rotation.

## Naming conventions

- File names: `snake_case.yaml`
- IDs in code (when needed): `snake_case`, scoped (`ogrs_dragon_lich`, not `dragon_lich`, to avoid collisions with future upstream additions).
- New numeric NPC ids: must be sequential after the last loaded id. Phase 1 work (#9) lifts this constraint and lets us claim id range 5000+.

## Reserved ID strategy

- **NPCs:** sequential after upstream's 836. **#9 backlog** moves us to a HashMap so we can claim id range 5000+ for any OGRS NPC.
- **Items:** TBD — Phase 1 will audit the item id space.
- **Zone region IDs:** 100+ for OGRS new lands.

## Validator

```bash
python3 tools/content-validator/validate.py
```

CI runs this on every PR. Schema violations block merge. The validator is intentionally simple right now (id format, unique ids per type); richer schema validation lands as the pipeline grows.
