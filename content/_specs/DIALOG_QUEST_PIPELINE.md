# Dialog + Quest Pipeline — Design Doc

Status: **DRAFT — not yet implemented.** Backlog items **#5 (dialog as data)** and **#8 (quest as data)**, designed together because quest stages dispatch dialog.

Goal: an OGRS author can add an NPC dialog, a multi-stage quest, or import an OSRS-style quest by editing YAML files only — no Java. Existing hand-coded plugins keep working; conversion is opt-in per NPC.

---

## Current state (one paragraph)

`OgrsContentQuestLoader` + `AbstractOgrsQuest` already exist. Quest YAMLs carry metadata (id, name, points, journal text, XP/item/coin rewards). Concrete subclasses (`OldWatsSeedPouch.java`) hand-code dialog branches, stage transitions, and kill-drop triggers in Java. Pure dialog NPCs (Old Aric, shopkeepers, ambient villagers) are 100% Java today — there is no dialog loader. The four existing content loaders (NPCs, Items, Scenery, Quests) are the pattern this doc copies.

---

## Non-goals (explicit)

- **Not replacing all Java plugins.** NPCs whose interaction can't be expressed in YAML (custom animations, unusual server-state writes, multi-NPC choreography) stay as Java plugins. The runner is opt-in per NPC slug.
- **Not adding an editor UI.** Editor lives in your text editor.
- **Not auto-importing OSRS quests yet.** This doc's schema is *expressive enough* for them, but the converter is a separate task.

---

## YAML schemas

### Dialog file — `content/dialog/<npc_slug>.yaml`

One file per NPC, keyed by the NPC's content/npcs slug (e.g., `old_aric.yaml` matches `content/npcs/old_aric.yaml`).

```yaml
# Required. Matches an NPC slug under content/npcs/.
npc: old_aric

# Required. The 'start' list is evaluated top-to-bottom on every Talk-to;
# the first matching entry's `go:` is the entry node. No match → no
# dialog runs (and the runner falls through so other plugins can handle).
start:
  - go: greet

# All dialog nodes. Each node has: npc lines, optional choices, optional
# actions, optional flow control (go / end / loop).
nodes:

  greet:
    # Plain string OR list of strings. List = sequential lines.
    npc:
      - "Easy now, friend. Sit a moment."
      - "I've walked these roads since before the river found its bed."
    # `loop: true` means after any child branch hits `end:`, return here.
    # Combined with `choices`, builds the classic "main menu" pattern.
    loop: true
    choices:
      - text: "What should I do next?"
        go: next_step
      - text: "Tell me about this place."
        go: world_flavor
      - text: "Any tips for the fight?"
        go: combat_tips
      - text: "Just passing through."
        # `bye: <text>` is a shortcut for an npc line + end:true.
        bye: "Walk well. The road remembers those who walk it kindly."

  # Conditional sub-nodes. The runner picks the FIRST entry whose `when:`
  # matches, or the first entry with no `when:` (the default). Skill names
  # mirror lowercase Skill enum values; `combat_level` is the computed
  # combat level, not a stored skill.
  next_step:
    branches:
      - when: { combat_level: { lt: 10 } }
        go: tip_combat_low
      - when:
          all:
            - { skill: cooking,  lt: 10 }
            - { skill: fishing,  lt: 10 }
        go: tip_food_and_fishing
      - when: { skill: cooking,    lt: 10 }
        go: tip_cooking
      - when: { skill: mining,     lt: 15 }
        go: tip_mining
      - when: { skill: woodcutting, lt: 15 }
        go: tip_woodcutting
      - when: { skill: firemaking,  lt: 10 }
        go: tip_firemaking
      # Fallback — no `when:` means always matches.
      - go: tip_general

  tip_combat_low:
    npc:
      - "You've fight in you yet, but not the practice for it."
      - "The cows north of the river are forgiving teachers."
      - "When they grow easy, the goblins east of town will test you proper."
    end: true

  # ... (other tip_* nodes omitted for brevity)

  world_flavor:
    npc:
      - "This is Old Gielinor. Older than the maps name it."
      - "There are kingdoms north — Varrock for swords, Falador for steel."
      - "Karamja burns to the south, all jungle and ash."
      - "And the wilderness past the hedge — that's no place to die for nothing."
    end: true

  combat_tips:
    npc:
      - "Three things keep a man alive in a scrap."
      - "First — know when to walk away. You can run now, did you know that?"
      - "Second — armor before glory."
      - "Third — feed yourself between fights. Don't trust a full health bar; trust your pack."
    end: true
```

#### Conditions vocabulary (`when:` block)

```yaml
# Single condition
when: { combat_level: { lt: 10 } }                    # < 10
when: { skill: cooking, eq: 99 }                      # cooking == 99
when: { skill: mining, gte: 15 }                      # mining >= 15
when: { quest_stage: { quest: old_wats_seed_pouch, eq: 1 } }
when: { has_item: { id: 1598, count_gte: 1 } }
when: { quest_complete: old_wats_seed_pouch }
when: { cache_key: ogrs_crypt_lord_killed, eq: true }
when: { random: { chance: 0.3 } }                     # 30% pick

# Boolean composition
when:
  all: [ ... conditions ... ]
  any: [ ... conditions ... ]
  not: { ... condition ... }
```

#### Actions vocabulary (`actions:` block, runs in order)

```yaml
actions:
  - set_quest_stage: { quest: old_wats_seed_pouch, value: 1 }
  - complete_quest: old_wats_seed_pouch         # fires handleReward
  - give_item:   { id: 1598, amount: 1 }
  - take_item:   { id: 1598, amount: 1 }
  - require_item: { id: 1598, amount: 1, else_go: missing_pouch }
  - add_xp:      { skill: farming, amount: 250 }
  - set_cache:   { key: ogrs_aric_first_talk, value: true }
  - teleport:    { x: 122, y: 645 }
  - sound:       victory
  - message:     "The gem hums softly."
  - open_shop:   slayer
```

#### Variable interpolation in `npc:` strings

```yaml
nodes:
  searching:
    npc:
      # Refs:
      #   {player_name}                 — player's display name
      #   {quest.<name>.stage}          — current stage (-1 = complete)
      #   {skill.<name>.level}          — current level
      #   {item.<id>.count}             — inventory count
      #   {slayer.task.remaining}       — slayer service state (if present)
      #   {slayer.task.name}
      npc: "You've still got {slayer.task.remaining} {slayer.task.name} to slay, {player_name}."
    end: true
```

### Quest file — `content/quests/<slug>.yaml` (EXTENDED)

Existing metadata stays. New top-level keys:

```yaml
id: 52
name: "Old Wat's Missing Seed Pouch"
quest_points: 1
members: false

journal:
  0: "Old Wat in Lumbridge mentioned he's lost his seed pouch..."
  1: "Find Old Wat's seed pouch. The goblins east of Lumbridge have it."
  2: "I have the pouch. Take it back to Old Wat."

rewards:
  xp:
    - { skill: farming, amount: 250 }
  items:
    - { id: 1594, amount: 10 }
    - { id: 1596, amount: 5  }
    - { id: 10,   amount: 100 }

# === NEW ===

# NPC dialog is owned by content/dialog/<npc>.yaml files. The quest YAML
# just declares which NPCs are involved and which stages they react to.
# The runner wires it together at load time.
npcs:
  - slug: old_wat
    role: quest_giver
  - slug: goblin_shaman
    role: optional_lore

# Kill-based stage transitions. The runner installs a synthetic
# KillNpcTrigger that fires for any of the npc ids (single int OR
# `family: [slug...]` for cross-id sets).
on_kill:
  - npc_ids: [62, 153, 154]    # rank-and-file goblin family
    when: { quest_stage: 1 }
    drop:
      item: { id: 1598, amount: 1 }   # Seed Pouch
      chance: 0.30
      then:
        - set_quest_stage: 2

# Use-on-NPC, use-on-item, use-on-loc — extension points for puzzle
# quests later. Same shape as on_kill (when + then actions).
on_use_item_on_npc:  []
on_use_item_on_item: []
```

---

## Worked example — `OldWatsSeedPouch` as fully data-driven

**`content/dialog/old_wat.yaml`** (new):

```yaml
npc: old_wat

start:
  # Route by quest stage. Stage -1 = complete; falls through to chat.
  - when: { quest_stage: { quest: old_wats_seed_pouch, eq: 0 } }
    go: stage0_intro
  - when:
      all:
        - { quest_stage: { quest: old_wats_seed_pouch, eq: 1 } }
        - { has_item: { id: 1598, count_gte: 1 } }
    go: stage1_with_pouch       # player picked up the pouch silently
  - when: { quest_stage: { quest: old_wats_seed_pouch, eq: 1 } }
    go: stage1_searching
  - when: { quest_stage: { quest: old_wats_seed_pouch, eq: 2 } }
    go: stage2_return
  - go: chat                     # default / -1 complete

nodes:
  stage0_intro:
    npc:
      - "Lost in thought, that one."
      - "I keep misplacing my seed pouch. It's a curse."
    choices:
      - text: "Anything I can help with?"
        go: stage0_accept
      - text: "I should be going."
        bye: "Aye, aye."

  stage0_accept:
    npc:
      - "Well... it's out east somewhere. Past the goblin shacks."
      - "Find it, bring it back. I'll see you right with seed."
    actions:
      - set_quest_stage: { quest: old_wats_seed_pouch, value: 1 }
    end: true

  stage1_searching:
    npc: "Any luck finding that pouch?"
    end: true

  stage1_with_pouch:
    npc:
      - "Is that... is that my pouch in your hand?"
    choices:
      - text: "Yes — here you go."
        go: stage2_return
      - text: "Just looks like one. Sorry."
        end: true

  stage2_return:
    npc:
      - "Oh! Thank you, thank you. I owe you proper."
    actions:
      - take_item: { id: 1598, amount: 1 }
      - complete_quest: old_wats_seed_pouch
    end: true

  chat:
    npc:
      - "Beautiful day. Crops nearly ready."
    end: true
```

**`content/quests/old_wats_seed_pouch.yaml`** (extended):

```yaml
id: 52
name: "Old Wat's Missing Seed Pouch"
quest_points: 1
members: false

journal:
  0: "Old Wat in Lumbridge mentioned he's lost his seed pouch..."
  1: "Find Old Wat's seed pouch. The goblins east of Lumbridge have it."
  2: "I have the pouch. Take it back to Old Wat."

rewards:
  xp:
    - { skill: farming, amount: 250 }
  items:
    - { id: 1594, amount: 10 }
    - { id: 1596, amount: 5 }
    - { id: 1597, amount: 3 }
    - { id: 10,   amount: 100 }

npcs:
  - slug: old_wat
    role: quest_giver

on_kill:
  - npc_ids: [62, 153, 154]
    when: { quest_stage: 1 }
    drop:
      item: { id: 1598, amount: 1 }
      chance: 0.30
      then:
        - set_quest_stage: 2
```

**`OldWatsSeedPouch.java`** shrinks from ~200 lines to ~0 — the YAML+runner replaces it entirely. The `AbstractOgrsQuest` base class is no longer subclassed for this quest; the runner registers the QuestInterface directly from the YAML.

---

## Architecture

### Loaders (boot-time, one-shot)

| Loader | Reads | Exposes |
|--------|-------|---------|
| `OgrsContentDialogLoader` (new) | `content/dialog/*.yaml` | `byNpcSlug(slug) → DialogTree` |
| `OgrsContentQuestLoader` (existing, extend) | `content/quests/*.yaml` | `byFilename`, new `getStageTriggers()`, `getKillTriggers()` |

### Runners (plugin classes registered with PluginHandler)

| Runner | Implements | Owns |
|--------|------------|------|
| `OgrsDialogRunner` | `TalkNpcTrigger` | All NPC slugs with a YAML dialog. Returns true from `blockTalkNpc` ONLY if the NPC is YAML-owned (avoids stomping hand-coded plugins). |
| `OgrsQuestRunner` | `QuestInterface` (one per YAML quest with no Java subclass) + `KillNpcTrigger` | Quest stage progression + handleReward; installs kill triggers per quest's `on_kill` block. |

### Coexistence with hand-coded plugins

The dialog runner consults `OgrsContentNpcLoader` for the slug→id mapping. If an NPC has BOTH a YAML dialog AND a hand-coded `TalkNpcTrigger`, **the runner deliberately does not load that NPC's YAML** — Java wins to avoid silent double-dispatch. A boot warning is logged so the conflict is visible.

(This is intentional: the migration plan is to delete the Java handler in the same commit that adds the YAML dialog. Until then, Java is authoritative.)

### Condition / action evaluator

A pair of small evaluator classes (`DialogCondition`, `DialogAction`) in `server/src/com/openrsc/server/external/dialog/`. Each is a switch over the YAML keys, dispatching to the engine. Adding a new condition or action is one branch + a doc-comment update here.

---

## Migration plan (post-design)

| Phase | Scope | Effort |
|-------|-------|--------|
| **A — Schemas + this doc.** | _(this session)_ | done |
| **B — Dialog loader + runner + first conversion.** | Build `OgrsContentDialogLoader`, `OgrsDialogRunner`, condition + action evaluators. Convert `OldAric` (most complex pure-dialog NPC). Delete `OldAric.java`. | 1 session |
| **C — Extend quest loader + quest runner.** | Add stage trigger + kill-drop block parsing to `OgrsContentQuestLoader`. Build `OgrsQuestRunner` that installs synthetic KillNpcTriggers and routes Talk dispatch through the dialog runner. Convert `OldWatsSeedPouch`. Delete its `.java`. | 1-2 sessions |
| **D — Bulk dialog migration.** | Convert shopkeepers (Edith, Garth, Marigold, Old Wat's farming chat), Wendel, the ambient Man.java OGRS lines, Grizzled Traveler. Behavior parity verified by manual playtest. | 1-2 sessions |
| **E — OSRS quest import.** | `tools/import-osrs-quest.py` reads an OSRS quest definition and emits OGRS dialog + quest YAML. Run against 2-3 starter quests for validation. | 2+ sessions |

Hard-stop gate between B and C: get one dialog converted and *played in-game* before extending to quests. Schemas often need tuning after first contact.

---

## Open questions / tradeoffs

1. **Custom Java escape hatch in YAML.** Should a node be able to declare `java_action: com.openrsc...MyHelper#runIt` for one-off logic that doesn't fit the action vocabulary? **Recommendation: no for v1.** Forces vocabulary discipline. Add later if real cases demand it.

2. **Variable interpolation engine.** Simple `{a.b.c}` regex or a real expression parser? **Recommendation: regex for v1.** Real expressions (`{player.combat_level + 5}`) are tempting but unbounded.

3. **NPC-family lookups in `on_kill`.** `npc_ids: [62, 153, 154]` is verbose; `family: goblin` would auto-expand. **Recommendation: add a `families:` registry under `content/_registries/npc_families.yaml` in phase C.** Solves the Goblin-spans-5-ids gotcha from the engine notes.

4. **Quest stage shorthand.** `when: { quest_stage: { quest: foo, eq: 1 } }` is wordy. Shorthand `when: { stage[foo]: 1 }` is shorter but parser-ugly. **Recommendation: keep verbose for v1.** Optimize after we've written 5+ quests.

5. **Dialog "loop" semantics.** Current proposal: `loop: true` returns to that node after a child `end:`. Alternative: explicit `back:` action. **Recommendation: keep `loop:` — covers the 95% case (NPC menus with bye option).**

6. **Hot-reload.** Boot-only or watcher-based reload? **Recommendation: boot-only.** Hot-reload is a separate concern; restart is fast (~3s).

7. **Schema validation tool.** `tools/content-validator/validate.py` already exists for items. Extend it to validate dialog + quest schemas at CI time. **Recommendation: yes, in phase B.**

---

## Sign-off

If this design holds together, phase B starts the implementation. Schema is the load-bearing thing; once shipped, downstream phases are mechanical.
