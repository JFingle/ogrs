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
