# Projectile Router — Future Extension Plan

> **Not art work.** This is an engine note kept inside the art workspace because it caps what art can accomplish. Read this *before* opening a PR to extend `OgrsProjectileTypes.java`.

## Current state (7 types)

`server/src/com/openrsc/server/util/OgrsProjectileTypes.java` defines 7 projectile types: `ORB`, `MAGIC`, `RANGED`, `GNOMEBALL`, `SKULL`, `SPIKEBALL`, `BLANK`. The router (`forArrow`, `forSpellName`, `forGodSpell`) maps every in-game projectile to one of these 7 sprites.

## Collisions today

These pairs collide in the current router and **cannot be visually differentiated** without engine work:

| Sprite | Used by (collision pair) |
|---|---|
| `ORB`       | Wind spells **+** Saradomin Strike |
| `MAGIC`     | Water/Ice spells **+** Fire spells |
| `SPIKEBALL` | Earth spells **+** Snare/Bind/Entangle |
| `SKULL`     | Curse/Weaken/Crumble **+** Flames of Zamorak **+** poison arrows |
| `RANGED`    | Default arrows **+** the spell mechanic "Bolt" (any spell with "bolt" in name) |

So although the ORB art deliberately reads "wind / holy light", the same sprite is what plays for *both* Wind Strike and Saradomin Strike — fine for now, but the user has expressed wanting per-spell differentiation.

## Tier collapse

Within an element family, all tiers share one sprite. Wind Strike, Wind Bolt, Wind Blast, Wind Wave → all `ORB`. The user wants strike/bolt/blast/wave to look distinct.

## What unlocks the full vision

Extending `OgrsProjectileTypes` to add ~12 more sprite slots + refining the routing logic. Roughly:

```
Existing 7:
  ORB, MAGIC, RANGED, GNOMEBALL, SKULL, SPIKEBALL, BLANK

Add (element split):
  WIND, WATER, EARTH, FIRE          # split MAGIC and split SPIKEBALL
  HOLY (Sara), NATURE (Guthix), CHAOS (Zamorak)  # split god spells out of ORB/GNOMEBALL/SKULL
  CURSE_BLACK                       # split Curse/Weaken out of SKULL
  POISON_GREEN                      # poison arrows get their own visual

Add (tier within element — optional, deeper):
  WIND_BOLT, WIND_BLAST, WIND_WAVE  # tiers grow visually
  WATER_BOLT, WATER_BLAST, WATER_WAVE
  EARTH_BOLT, EARTH_BLAST, EARTH_WAVE
  FIRE_BOLT, FIRE_BLAST, FIRE_WAVE
```

That's potentially **~20 distinct sprite slots**, up from 7. The router would then choose based on (a) spell element, (b) spell tier (strike/bolt/blast/wave detected from name), (c) god identity.

## Engine changes required

1. **Server: `OgrsProjectileTypes.java`** — add new int constants, refine `forSpellName` to branch on tier-within-element. ~40 LOC.
2. **Client: `mudclient.java`** — currently treats `spriteProjectile (3160) + type` as the sprite index. Adding more types just needs `loadProjectiles()` to load more entries from the cache. No core rendering changes.
3. **Sprite archive** — add the new sprite entries to `Custom_Sprites.osar` (or a new `Custom_Projectiles.osar` override pack).
4. **`EntityHandler.loadProjectiles()`** — currently registers 7 `SpriteDef` entries. Bump to N. Single integer change.

**Estimate:** half a session of engine code + however long the art takes. Not a multi-week project.

## Recommended sequencing

1. **Ship the current 7-sprite art first** — pack `Custom_Projectiles.osar`, wire `config.txt`, verify in-game. Get the visual baseline live. (Engine code: just the pack-wiring, no router changes.)
2. **Then decide if extension is worth it** — the 7-sprite version is already a massive upgrade over vanilla. The deeper differentiation is polish, not necessity.
3. **If extending**: do it AFTER `OgrsContentNpcLoader` / quest-as-data lands, so the YAML/data-driven pattern can apply to spell definitions too. A `content/spells/<book>/<spell>.yaml` per-spell file declaring `projectile: WIND_BLAST` is cleaner than continuing to grow the Java router.

This dovetails with project memory item #22 ("More spells / new spellbook") which already calls for moving spell defs to YAML.

---

## Engine prereqs queued by art ambition (do these during the engine pass)

### Crumble Undead — bones-crumble death animation (Sparky 2026-05-19)

**Player desire:** When Crumble Undead's damage is fatal to an undead NPC, the NPC should visually crumble apart (bones break, dust rises) instead of playing the standard NPC death animation.

**Engine work:**
1. Hook in the combat resolver where NPC death is detected. Find where `npc.die()` (or equivalent) is invoked from spell damage.
2. Branch: `if (spell == Spells.CRUMBLE_UNDEAD && npc.isUndead() && damage >= npc.hp)` → call `playCrumbleDeath(npc)` instead of standard death animation.
3. `playCrumbleDeath(npc)` triggers the crumble impact effect (already authored in `art/projectiles/debuff_crumble_undead/impact/`) at the NPC's tile, then removes the NPC.
4. The "isUndead" check needs an NPC tag — either a flag in `NpcDefs` (`is_undead: true`) or a list of undead NPC ids checked at runtime. Skeleton/Zombie/Ghost/Banshee/Lesser Demon/etc. should be tagged.

**Art prereq satisfied:** Crumble impact already authored — 48×48 4-frame radial showing bones breaking apart + holy energy dissipating.

**Bonus visual:** if the engine supports playing a sprite animation centered on the NPC's position (vs. center of tile), the crumble effect should follow the NPC sprite's center for the satisfying "this specific creature is breaking" feel.

### Generic impact-effect renderer

Multiple impact sprites authored (`art/projectiles/*/impact/`) but engine doesn't yet have an impact-sprite renderer. Need:
1. New sprite slot category in the cache: "impact" sprites at indices [3170+]
2. After projectile lands, spawn a 4-frame (or 8-frame for hybrids) sprite animation at the target's screen position
3. Animation plays once then disappears (no looping)

### Stackable item sprite tiers (Sparky 2026-05-20)

Stackable items should change appearance with quantity — "the more you have, the more it looks like you have." Authored 6-tier coins + 4-tier seeds for potato/onion/tomato (18 sprites total) at `art/items/`.

**Engine work:**

1. **Add `sprite_tiers` field to ItemDef** (or runtime equivalent): list of sprite IDs per quantity threshold.
2. **In the inventory render path,** when drawing an item with quantity Q, pick the sprite tier whose threshold ≤ Q (highest one that fits).
3. **Recommended thresholds** (match OSRS convention):

   | Tier | Coin threshold | Seed threshold |
   |---|---|---|
   | 1 | 1 | 1 |
   | 2 | 2 | 2 |
   | 3 | 3 | 10 |
   | 4 | 4 | 50 |
   | 5 | 5 | (n/a) |
   | 6 | 25+ | (n/a) |

   Coins use 6 tiers because they're the canonical stack item; seeds use 4 (smaller realistic range).

4. **Per-item override** — let ItemDef pin custom thresholds for items where the default doesn't fit.

**Art file structure (already authored):**

```
art/items/
├── coins/
│   └── tiers/
│       ├── tier_1_single.png    (1)
│       ├── tier_2_pair.png      (2-3)
│       ├── tier_3_cluster.png   (4-9)
│       ├── tier_4_pile.png      (10-49)
│       ├── tier_5_heap.png      (50-249)
│       └── tier_6_overflow.png  (250+)
└── seeds/
    ├── potato/tiers/tier_1..4.png
    ├── onion/tiers/tier_1..4.png
    └── tomato/tiers/tier_1..4.png
```

**Item IDs already in the engine** that should adopt these:
- Coins (id 10) — use the 6 coin tiers
- Potato Seed (id 1594) — use potato 4 tiers
- Onion Seed (id 1596) — use onion 4 tiers
- Tomato Seed (id 1597) — use tomato 4 tiers

The art replaces the current tinted-fallback sprites flagged in `project_ogrs.md` memory (items currently reuse mithril-seed sprite 270 + bird-feed sprite 276).

### Direction-picker for 8-variant sprites

Authored 8 directional variants for `2_ranged` arrow and `element_fire` flame in `directions/` folders. Engine work:
```java
int directionIndex(double caster_x, double caster_y, double target_x, double target_y) {
    double angle = Math.atan2(target_y - caster_y, target_x - caster_x);
    // Snap to nearest of 8 directions (N=-π/2, NE=-π/4, E=0, SE=π/4, S=π/2, SW=3π/4, W=π, NW=-3π/4)
    int idx = (int) Math.round(angle / (Math.PI / 4));
    return ((idx % 8) + 8) % 8;
}
```
Then pick `directions/arrow_{N,NE,E,SE,S,SW,W,NW}.png` accordingly.
