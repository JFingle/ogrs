# OGRS Spell Visual Catalog

Source: `server/src/com/openrsc/server/constants/Spells.java` (62 entries, 3 hidden/unused).
Goal: every visible spell has a distinctive on-cast visual. Per Sparky 2026-05-19:
- **Generic element spells share a shape, differ by hue** (Wind/Water/Earth/Fire each = one shape language across all tiers).
- **Utility / debuff / unique spells get their own unique design** (Confuse, Weaken, Enfeeble, Stun, Vulnerability, etc.).
- **God spells with engine-custom animations are a separate later pass** (Saradomin Strike, Claws of Guthix, Flames of Zamorak).

Status legend: ✅ done · 🟡 partial (using a shared/router sprite) · ❌ not yet drawn · ⏸️ deferred.

---

## A — Element spell families (4 sprites, share shape per element)

Tier escalation (Strike→Bolt→Blast→Wave) is **deferred** (see `_specs/ROUTER_NOTES.md` + `_mockups/wind_tier_escalation.png`). All tiers within a family render the same sprite for now, distinguished by name + hue.

| Family | Sprite | Tiers using it | Status |
|---|---|---|---|
| **Wind / Air** | `0_orb` (cream-gold) | Wind Strike / Bolt_R / Bolt / Blast / Wave | ✅ |
| **Water / Ice** | `1_magic` (ice diamond) | Water Strike / Bolt / Blast / Wave; Chill Bolt | ✅ |
| **Earth / Stone** | `5_spikeball` (mossy boulder) | Earth Strike / Bolt / Blast / Wave | ✅ |
| **Fire / Flame** | `7_fire` (NEW — needs draw) | Fire Strike / Bolt / Blast / Wave; Iban Blast | ❌ |

**Note:** Currently the router collides Water & Fire onto `MAGIC`. Splitting is engine work (Sparky pass). Art-side, we draw the Fire sprite anyway so the asset is ready.

---

## B — Special bolts (each unique)

These look bolt-like but aren't simple element variants.

| Spell | Visual idea | Status |
|---|---|---|
| **Chill Bolt** | A frozen *arrow* (not a wind streak) — could share shape with our RANGED arrow but white/blue | ❌ |
| **Shock Bolt** | Jagged yellow lightning zig-zag — angular silhouette, very different from element orbs | ❌ |
| **Elemental Bolt** | Multi-colored swirling orb (rainbow tint) — neutral fallback bolt | ❌ |
| **Iban Blast** | Crimson chaos blast — could lean on the Fire shape language with extra dark-red runes | ❌ |

---

## C — Debuff / curse spells (each unique per Sparky's request)

Sparky 2026-05-19: "weaken, enfeeble, those things should look unique."

| Spell | Visual idea | Status |
|---|---|---|
| **Confuse** | Dark-purple swirl with floating question-mark glyphs | ❌ |
| **Confuse_R** (retro) | Same family as Confuse, dimmer | ❌ |
| **Weaken** | Drooping olive-grey droplet trailing downward (sapping strength) | ❌ |
| **Vulnerability** | Cracked purple aura with red fissures (defense splitting) | ❌ |
| **Enfeeble** | Sickly-yellow misty cloud (worse than Weaken) | ❌ |
| **Stun** | Bright yellow lightning fork wrapping a small star (classic stun) | ❌ |
| **Curse** | Currently uses `4_skull` (shared with Crumble + Flames of Zamorak) | 🟡 |
| **Crumble Undead** | White holy energy bursting from a cracked skull — distinct from Curse's purple flames | ❌ |
| **Fear** (retro) | Dark-purple wisp recoiling backward | ❌ |

---

## D — Buff spells (each unique)

Retro spells from pre-launch OGRS, all four exist in the Spells enum.

| Spell | Visual idea | Status |
|---|---|---|
| **Thick Skin** (retro) | Brown-stone shield outline | ❌ |
| **Burst of Strength** (retro) | Red clenched-fist sparkle | ❌ |
| **Rock Skin** (retro) | Grey stone armor wrap | ❌ |
| **Camouflage** (retro) | Faded green leaf cluster fading at the edges | ❌ |

---

## E — Utility spells (each unique)

Some have target-sparkle animations rather than fly-through-air projectiles.

| Spell | Visual idea | Status |
|---|---|---|
| **Bones to Bananas** | Yellow-curve glyph (banana silhouette) | ❌ |
| **Bones to Bread** (retro) | Brown loaf glyph | ❌ |
| **Low Alchemy** | Single gold coin sparkle | ❌ |
| **High Alchemy** | Triple gold coin sparkle, brighter | ❌ |
| **Telekinetic Grab** | Translucent reaching hand glyph | ❌ |
| **Superheat Item** | Orange ore-melt drip | ❌ |
| **Charge** | Lavender energy pulse (god-spell prep) | ❌ |

---

## F — Charge orb spells (4)

These are the rune-charging spells — each casts on the corresponding obelisk.

| Spell | Visual idea | Status |
|---|---|---|
| **Charge Air Orb** | Pale gold swirl entering an orb shape | ❌ |
| **Charge Water Orb** | Cyan swirl into orb | ❌ |
| **Charge Earth Orb** | Brown-green swirl into orb | ❌ |
| **Charge Fire Orb** | Red swirl into orb | ❌ |

---

## G — Enchant spells (5 tiers)

| Spell | Visual idea | Status |
|---|---|---|
| **Enchant Lvl1** | Pale-blue sparkle on amulet | ❌ |
| **Enchant Lvl2** | Cyan sparkle, brighter | ❌ |
| **Enchant Lvl3** | Yellow-gold sparkle | ❌ |
| **Enchant Lvl4** | Purple sparkle | ❌ |
| **Enchant Lvl5** | White-hot sparkle with rays | ❌ |

---

## H — Teleport spells (6 — could share a single design OR each unique)

Open question for Sparky: do teleports each get their own town-themed visual, or do they all use one generic teleport effect?

| Spell | Status |
|---|---|
| Varrock / Lumbridge / Falador / Camelot / Ardougne / Watchtower Teleport | ❌ |

---

## I — God spells (DEFERRED — engine has custom animations)

Sparky 2026-05-19: "we will want to do that also at some point" — flagged as later pass.

| Spell | Current sprite | Status |
|---|---|---|
| Saradomin Strike | `0_orb` (shared with Wind) | ⏸️ |
| Claws of Guthix | `3_gnomeball` (shared with utility) | ⏸️ |
| Flames of Zamorak | `4_skull` (shared with Curse) | ⏸️ |

---

## J — Hidden / unused (skip)

`CALL_ANIMAL`, `RAISE_SKELETON`, `SUMMON_DEMON` — hidden in early clients, not castable. No art needed.

---

## Counts summary

| Category | # spells | # art assets needed |
|---|---:|---:|
| A — Elements (share per family) | 16 spells | 4 sprites (3 done, 1 to go: FIRE) |
| B — Special bolts | 4 | 4 |
| C — Debuffs | 9 | ~8 (Curse already has art) |
| D — Buffs | 4 | 4 |
| E — Utilities | 7 | 7 |
| F — Charge orbs | 4 | 4 |
| G — Enchants | 5 | 5 |
| H — Teleports | 6 | 1-6 (TBD) |
| I — Gods | 3 | deferred |
| J — Hidden | 3 | skip |
| **TOTAL** | **62** | **~37-42 unique sprites** |

---

## Recommended draw order

1. **FIRE element** — closes the 4-element set, completes our foundation
2. **Stun + Confuse + Weaken + Vulnerability + Enfeeble** — the 5 most-used debuffs, each unique
3. **Special bolts** (Chill, Shock, Elemental, Iban) — fills out combat spell variety
4. **Buffs** (Thick Skin / Burst of Strength / Rock Skin / Camouflage) — completes retro spell coverage
5. **Crumble Undead + Fear** — split out of the SKULL shared sprite
6. **Utilities + Charge orbs + Enchants + Teleports** — long tail
7. **God spells (later, separate pass)**

Engine prereq: many of these new sprites require extending the `OgrsProjectileTypes` router to support more types. That's a **future engine session by Sparky**, not blocking the art authoring. See `_specs/ROUTER_NOTES.md`.
