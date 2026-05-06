# The RSC Contract

**Purpose:** This document defines what makes RuneScape Classic *feel like* RuneScape Classic. Every change to the engine, mechanics, or presentation must be checked against this contract. Anything we want to change that conflicts with the contract requires an **explicit amendment** to this doc — no silent drift.

If a feature would violate the contract, the answer is "no" by default. The bar to amend is: write down what changes, why, and what we lose.

**Status:** v0 draft, 2026-05-06. Will be revised after the OpenRSC audit confirms the actual mechanical baseline.

---

## Tier 1 — Inviolable (the project loses its identity without these)

These are not negotiable. They define the look and feel.

### Visual & spatial
- **2D isometric tile-based world.** No 3D models. No perspective camera changes. No free movement.
- **Fixed tile size.** Tiles are the unit of position. Pathing is per-tile.
- **Sprite-based characters and creatures.** Pre-rendered or hand-drawn sprite sheets. No real-time rigged 3D.
- **Original color palette and pixel density.** New sprites must match the existing palette and pixel scale; no HD/anti-aliased mismatches inside the classic UI.
- **Classic UI mode is pixel-perfect.** When the player chooses classic UI, every panel, font, and pixel matches the 2001 layout. This is a regression test target — automated screenshot diffs.

### Movement & time
- **Tick-based world.** The world advances on fixed ticks (**640ms canonical** in OpenRSC, configurable). All combat, NPC AI, skill actions, and projectile travel resolve on tick boundaries. No real-time or sub-tick mechanics.
- **Walk/run speed and stamina behave as in classic RSC.** No sprint, no mounts, no fast-travel beyond what already exists (teleports, ships).

### Stats & progression
- **Skill levels capped at 99.** XP curve and level thresholds match RSC.
- **Same skill set as preservation baseline** for existing skills. New skills are *additive*, never replacements.
- **Combat level formula** matches RSC. Adding a new combat skill requires amendment + a new formula.
- **Combat triangle** (melee/ranged/magic) is preserved as a balance principle even when adding new mechanics.

### Combat
- **Tick-based combat resolution.** Damage, accuracy, and special effects resolve on tick boundaries.
- **Server-authoritative.** Client never decides damage, hit/miss, XP gained, or item received.
- **No instant-cast / no animation cancel.** Action timing matches RSC pacing.

### Economy & items
- **Trade and Grand Exchange behavior** stays as the preservation baseline (RSC had no GE — direct trade only). Don't add a GE unless we amend.
- **Item stacking rules** match RSC.
- **Death drops and PvP rules** match preservation baseline.

---

## Tier 2 — Default-preserve, amendable with discussion

These are RSC defaults but we may consciously change some. Each change needs a written amendment in this doc.

- **Damage formula details** (max hit calculation, accuracy roll). Default = RSC formula. Pluggable in code so we can ship variants per zone/event without breaking the default.
- **Spell list, spell tiers, runes required.** Defaults match preservation. New spells are additive.
- **Projectile visuals** — currently hardcoded blue/green orbs. **Explicitly approved for change**: generic projectile entity (sprite + path + speed + impact) replaces the orbs. Default sprite for legacy spells must remain visually equivalent unless we're intentionally giving them new looks.
- **Window size and aspect ratio.** Default classic = 512×334. **Explicitly approved for change**: resizable window with integer-scale and free-scale options. Game world rendering scales; classic UI mode keeps the 512×334 framing.
- **UI layout and skin.** Classic UI is Tier 1 (must remain pixel-perfect). Modern UI is a separate skin selectable by player; layouts may differ but functionality must mirror.
- **NPC AI behavior.** Defaults preserved. Additive NPCs may have richer behavior trees as long as they don't violate tick timing.
- **Drop tables.** Defaults preserved for existing NPCs. New NPCs get original drop tables.
- **XP rates** for existing skills. Defaults preserved. Event/zone-specific multipliers allowed if clearly signposted.

---

## Tier 3 — Free to extend (additive content lane)

This is where most of the project lives. No amendment needed; just follow the data pipeline conventions.

- **New zones / lands** — new tile maps, new regions appended to the world.
- **New NPCs** — new monsters, new merchants, new questgivers.
- **New items** — weapons, armor, consumables, quest items.
- **New quests / events** — including holiday and time-limited world events.
- **New spells / prayers** — added to existing schools or in new schools (subject to combat triangle balance).
- **New skills** — additive only; existing skills untouched.
- **New status effects** — burn, freeze, stun, bleed, etc. Built on a generic effect system.
- **New projectile visuals** — once the generic projectile system lands, every spell/arrow can have unique look.

---

## Anti-pattern list (things we explicitly will NOT do)

These would violate Tier 1 and won't be entertained without rewriting this doc:

- 3D models for characters, NPCs, or world geometry
- Real-time / non-tick combat
- Mouse-aim or skill-shot targeting
- Auto-attack toggles that bypass tick decisions
- HD textures inside classic UI
- Fast-travel teleporters that bypass the existing magic teleport system
- Cosmetic-only microtransactions or paid stat boosts (this is a preservation server, not a cash shop)
- Cross-account trading restrictions weaker than RSC's
- Client-authoritative damage, XP, or item state — ever, at all, for any reason

---

## Amendment process

To amend any Tier 1 or Tier 2 item:

1. Open a PR titled `contract: amend <topic>`.
2. Edit this doc with a `### Amendment YYYY-MM-DD` block under the affected tier.
3. Include: what changes, why we want it, what we lose, what tests/regressions we add to compensate.
4. The amendment must be merged before any code change implementing it lands.

This is a forcing function — it makes us think before we drift.

---

## Verification gates

Each release should pass these before shipping:

- **Pixel-diff test** — classic UI mode renders identically to a captured baseline.
- **Tick-timing test** — combat, skill actions, NPC AI all resolve on tick boundaries; no sub-tick reads.
- **Server-authority test** — fuzz the client with malformed packets; server must never desync, leak XP, or duplicate items.
- **Palette test** — new sprites pass an automated palette check (only colors from the approved palette set).
- **Formula regression** — default damage/accuracy rolls produce statistically identical distributions to the preservation baseline.

---

## Open questions (resolve in v1)

- ~~Exact tick rate after OpenRSC audit~~ **Resolved 2026-05-06: 640ms** (OpenRSC default).
- **Which client protocol version is the "preservation baseline"?** OpenRSC supports 38/69/140/177/196/198/199/201/202/203/233/235. Need to pick one as canonical. Leaning **177** (mid-RSC1, widely cited as the "2001 feel" target) but TBD.
- Whether we want **two server modes** (strict preservation vs. extended) or just one extended server with toggleable rule packs.
- Anti-cheat: where does "client-side prediction for input responsiveness" stop and "client authority" begin? Need a clear line.
- Modding/plugin policy for end users (is the client moddable for personal use? what's auto-banned?).
- **Skills + quests are hardcoded Java in upstream.** Do we (a) leave that, accepting that new skills/quests need code, or (b) refactor them into data-driven systems? Affects whether "additive content is data" applies universally or only to NPCs/items/zones/spells.
- **Maps are binary `.jag` blobs with no editor.** Do we (a) reverse-engineer the format and build a binary editor, or (b) build a parallel JSON map format that compiles to `.jag` at server startup? Recommend (b).
