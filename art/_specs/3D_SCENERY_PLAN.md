# OGRS 3D World Scenery — Magic Track Design

> **Status:** Spec-only. No `.jag` files authored yet. This doc lays out **what** to build, **how** to build it, and **in what order** so the Blender pass can start with full context.

## 1. Toolchain (one-time setup)

### Required tools
1. **Blender** — install on Windows side at `/mnt/c/Program Files/Blender Foundation/Blender X.Y/` (or wherever convenient). WSL doesn't need it; we'll run Blender natively on Windows and just copy files in/out.
2. **`@2003scape/rsc-models`** — Node CLI that round-trips RSC `.jag` ↔ Wavefront `.obj`/`.mtl`. Install once:
   ```bash
   npm install -g @2003scape/rsc-models
   ```
3. **Reference web viewer** — https://2003scape/rsc-models/ (also runnable locally) shows every existing model in RSC. **Use this before authoring anything new** to check whether the model we want already exists.

### Workflow per model
1. **Check the viewer** — is there an existing RSC model close to what we want?
   - Yes → dump it with `rsc-models dump-obj`, edit in Blender, repack.
   - No → model from scratch in Blender.
2. **Blender authoring rules** (per `[[rsc-models-2003scape]]` memory):
   - Low-poly aesthetic (~50-200 tris per scenery object)
   - Flat-shaded faces, not Gouraud-smoothed
   - Material colors from RSC palette (limited 256-color)
   - Single mesh per scenery object (no instancing)
3. **Export to `.obj`** with `.mtl` for materials.
4. **Pack into `.jag`** via `rsc-models pack-obj`. Place in `client/Cache/video/models.orsc` as additions or in a new `Custom_Magic_Models.osar` override pack.
5. **YAML scenery def** — add the new scenery to `content/scenery/<zone>.yaml` referencing the model by name.

### File output naming convention
- New OGRS scenery models: `ogrs_<category>_<name>.obj` (e.g., `ogrs_altar_air.obj`)
- This keeps them grouped and avoids upstream collision.

---

## 2. Magic-themed 3D scenery catalog

### Phase A — Rune altars (15 models)

Each rune type needs an altar (the actual interactable scenery for runecrafting). They share a common base structure (stone pillar, ~3 tiles tall) but vary in **color + glow emanation + carved symbol**.

| Altar | Color | Glow | Carved symbol (top of pillar) |
|---|---|---|---|
| Air | pale cream | white wind streaks | swirl |
| Water | blue | cyan ripple | wave |
| Earth | brown | green moss | cross/X |
| Fire | red | orange flame | triangle (flame) |
| Mind | pale yellow | yellow shimmer | eye/dot-in-circle |
| Body | orange | warm | stick figure |
| Cosmic | purple | violet | 5-point star |
| Chaos | dark red | crimson flickers | zigzag |
| Nature | green | green leaves | leaf |
| Law | white | golden | scroll/scales |
| Death | dark purple | purple mist | skull |
| Blood | deep red | red mist | drop |
| Soul | pale blue-white | spirit wisps | spirit swirl |
| **Life (OGRS)** | pink | warm glow | heart/ankh |
| **Astral (OGRS)** | silver | lunar gleam | crescent moon |

**Geometry:** Each altar is ~3 game-tiles tall (one tile = ~16 game units). Pillar base + carved-top capital + floating glow halo.

**Inspiration:** Look at the existing `chaosaltar` model in the 2003scape viewer (https://2003scape.github.io/rsc-models#chaosaltar) — that's our visual baseline. We extend it by varying color and adding the per-rune carved symbol on the capital.

### Phase B — Spellbook libraries (3 models)

Free-standing lecterns/bookshelves where players read to switch spellbooks.

1. **Standard Bookshelf** — generic wooden bookshelf, several books visible. Brown wood.
2. **Ancient Tome Pedestal** — dark stone pedestal with a single floating purple book. Glows violet.
3. **Yahwist Altar Lectern** — gold/cream wooden lectern with a Bible-sized book chained to it. Faint warm glow.

**Geometry:** ~1 tile footprint, ~1.5 tiles tall.

### Phase C — Portals & doors (4 models)

1. **Standard Magic Portal** — circular stone arch with shimmering blue plane inside (animated UV).
2. **City Teleport Portal** — colored variants per city (Varrock blue, Lumbridge yellow, etc.) — uses Phase 7 of the spell-art track. 6 visual variants but ONE model with material swap. **Could be just 1 base model** if engine supports material recoloring.
3. **Wizard Tower Floor Portal** — flat circular tile on ground that teleports you up to the next floor. Concentric ring pattern.
4. **Ancient Mage Door** — runed stone door, dimly glowing. Used for quest gates.

### Phase D — Wizard tower props (6 models)

1. **Scrying Pool** — small stone basin filled with luminous liquid (animated). Used for divination/buff spells.
2. **Magical Brazier** — wrought-iron tripod with a flame on top. Continuously burning.
3. **Orb Stand** — pedestal with a floating crystal ball. Cast spells through it.
4. **Apprentice Workbench** — desk with parchment, quill, vials. Crafting station.
5. **Master's Throne** — ornate chair (quest interaction).
6. **Star Chart Globe** — stand with a rotating starfield sphere on top. Astronomical study item.

### Phase E — Training & Combat (4 models)

1. **Training Dummy** — wooden post with straw torso, wrapped in cloth. For Attack/Strength training.
2. **Magic Practice Dummy** — same shape but with a magical aura halo, robes painted on. For Magic training.
3. **Combat Ring Marker** — small flag/banner planted in the ground. Marks PvP arenas.
4. **Healing Pillar** — single tall stone obelisk with healing rune carved on it. Slowly restores HP for nearby players.

### Phase F — Galilee / Sacred (5 models) — long-term

Per project memory (project_ogrs.md item 20), OGRS has a biblical worldview. Sacred-themed magic scenery:

1. **Anointing Olive Press** — wooden press with stone basin. Produces anointing oil (potion).
2. **Communion Altar** — simple wooden table with bread + cup on it.
3. **Fig Tree** — gnarled tree with hanging figs. Quest/lore-relevant.
4. **Mustard Seed Garden** — small fenced patch with a single tiny seed in the middle. Visual representation of "faith of a mustard seed."
5. **Manna Stone** — pale white stone tablet half-buried in ground. Daily wilderness food spawn.

---

## 3. Recommended draw order

1. **Phase A — first 4 elemental altars** (Air/Water/Earth/Fire) — these enable Runecrafting MVP. The 11 other altars (Mind/Body/Cosmic/Chaos/Nature/Law/Death/Blood/Soul/Life/Astral) can be copies of the base altar with color/symbol changes.
2. **Phase C** — Standard Magic Portal (single model with material swap covers most city-teleport variants).
3. **Phase D** — Scrying Pool, Magical Brazier, Orb Stand (the most useful generic wizard-tower props).
4. **Phase B** — Bookshelf + Pedestal + Lectern.
5. **Phase E** — Training Dummies (Combat/Magic training).
6. **Phase F** — Sacred/Galilee items (long-term, post-quest-chain).

**Estimate:** Phase A's 4 base elemental altars = ~1 day of Blender work for an experienced modeler. The other 11 altars = ~1-2 hours each (copy + recolor + new carved symbol).

---

## 4. Integration plan

### Engine-side prereqs
1. New scenery defs in `content/scenery/<zone>.yaml` — schema:
   ```yaml
   id: 5000
   name: Air Altar
   model: ogrs_altar_air
   width: 1
   height: 1
   interactable: true
   action: runecraft
   element: air
   ```
2. Scenery loader reads YAML, adds to engine's scenery def list (parallel to `OgrsContentNpcLoader`).
3. Codegen script for client: `tools/codegen-client-scenery.py` reads same YAML, emits `client/.../scenery/generated/OgrsClientScenery.java` registering each model name.

### Asset packaging
1. Author `ogrs_altar_air.obj` + `.mtl` in Blender.
2. `rsc-models pack-obj ogrs_altar_air.obj > ogrs_altar_air.jag`
3. Drop into `client/Cache/video/spritepacks/Custom_Magic_Models.osar` (gzip-bundled).
4. Enable in `client/Cache/video/config.txt` with `Custom_Magic_Models:1`.

### Placement
- Each rune altar lives in a small dungeon/cave (one per element). Air Altar in northern wilderness, Water Altar in coastal cave, Earth Altar in mountain pass, etc. Spawn coordinates go in `content/scenery/altars.yaml`.

---

## 5. Reference imagery to gather (for the Blender modeler)

Before authoring, the modeler should:
1. **Browse https://2003scape.github.io/rsc-models** and identify these existing models:
   - `chaosaltar` — the visual template for all rune altars
   - `lectern`, `bookcase` (if they exist) — for Phase B
   - `door1`, `door2` — for Phase C
   - `tripod`, `pillar`, `column` — generic props that may exist for Phase D
2. **Dump those models** locally:
   ```bash
   rsc-models dump-obj --archive models.jag --out reference_models/
   ```
3. **Open in Blender** to study topology, scale, material setup before authoring new ones.

---

## 6. What this spec does NOT cover

- **NPC models** (wizards, monks, etc.) — separate track, more complex (skeletal animation)
- **Weapon/armor 3D models** — these are tied to player equipment rendering, different system
- **Terrain tiles** — landscape data is in `Authentic_Landscape.orsc`, totally different format
- **Animations** — even static scenery may need idle animations (brazier flame, portal swirl). Animation system is engine work, not in scope for this spec.

---

## 7. Open questions

- Should rune altars all be at the SAME size, or scale up for higher-tier altars (Death/Blood/Soul bigger than Air)?
- Should Galilee/Sacred scenery be gated behind quest completion, or visible to all players from day one?
- For city teleport portals — one model + material swap, or 6 unique models (each with the city's banner/heraldry)?

These are gameplay/lore decisions for Sparky; the modeler doesn't need to resolve them before starting on Phase A.
