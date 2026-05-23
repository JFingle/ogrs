# OGRS Art Session — Hand-off to Coder

> All art assets authored in this session, with the engine work needed to display them in-game. **NPC/goblin work is excluded** (we paused there pending better reference).

**Source of truth:** `~/ogrs/art/` (WSL).
**Windows mirror:** `C:\OGRS_Art\` (synced as work progressed).
**Authoring scripts:** every sprite folder has a `_draw_<name>.py` Python+PIL script. The scripts ARE the source of truth — re-running them regenerates the PNGs.

---

## 1. What's authored (the art deliverables)

### 1A — Router projectile replacements (7 slots)

The engine already has 7 hardcoded projectile sprite slots at `Authentic_Sprites.orsc` entries 3160-3166. Routed by `server/src/com/openrsc/server/util/OgrsProjectileTypes.java` (which exists and works). All 7 have been replaced with new art:

| Engine slot | Folder | What it covers |
|---|---|---|
| 3160 ORB | `projectiles/0_orb/` | Wind spells, Saradomin Strike, mithril arrows |
| 3161 MAGIC | `projectiles/1_magic/` | Water/Ice spells (Fire collides — see §3) |
| 3162 RANGED | `projectiles/2_ranged/` | All arrows, "bolt" mechanic |
| 3163 GNOMEBALL | `projectiles/3_gnomeball/` | Alch / Telegrab / Heal / Plank Make / Claws of Guthix |
| 3164 SKULL | `projectiles/4_skull/` | Curse / Weaken / Crumble / Flames of Zamorak / poison arrows |
| 3165 SPIKEBALL | `projectiles/5_spikeball/` | Earth spells / Snare / Bind / adamant arrows |
| 3166 BLANK | `projectiles/6_blank/` | Small thrown darts |

Each folder contains `frames/frame_00..03.png` (30×30 transparent, the actual game-size assets) plus `_x8.png` upscales for inspection.

**Reference image of what existed before:** `~/ogrs/art/reference/proj_3160_ORB.png` through `proj_3166_BLANK.png`.

### 1B — Combat-spell impact effects (48×48, 4-frame)

When a projectile lands on a target, the engine should play one of these radial-dissipate impact animations centered on the target's tile. **This is a new sprite slot category** (impacts are not part of the existing projectile-sprite range; they need their own indices in the cache).

| Spell family | Folder | Impact style |
|---|---|---|
| ORB | `projectiles/0_orb/impact/` | Gold sparkle burst |
| MAGIC | `projectiles/1_magic/impact/` | Ice shatter / cyan shards |
| GNOMEBALL | `projectiles/3_gnomeball/impact/` | Nature green leaves scatter |
| SKULL | `projectiles/4_skull/impact/` | Cursed purple wisps + ember |
| SPIKEBALL | `projectiles/5_spikeball/impact/` | Earth dirt clods + dust |
| FIRE (element split) | `projectiles/element_fire/impact/` | Flame splash + embers |
| Crumble Undead | `projectiles/debuff_crumble_undead/impact/` | Holy burst + bone fragments |

Each impact is a 4-frame arc: `frame_00` spawn → `frame_01` expand → `frame_02` peak (wraps target silhouette) → `frame_03` dissipate. **Peak frames intentionally have a humanoid-silhouette negative-space at center** so the effect wraps a player/NPC sprite.

### 1C — Unique spell projectiles (37 sprites)

Each is a self-contained 30×30 4-frame sprite for a specific spell. These need engine work to **expose more router slots** (see §3). Folder list:

#### Debuffs (5 unique)
| Spell | Folder | Visual |
|---|---|---|
| Confuse | `projectiles/debuff_confuse/frames/` | White "?" inside orbiting purple aura |
| Weaken | `projectiles/debuff_weaken/frames/` | Drooping olive droplet sapping down |
| Vulnerability | `projectiles/debuff_vulnerability/frames/` | Purple aura cracked with red fissures |
| Enfeeble | `projectiles/debuff_enfeeble/frames/` | Hazy yellow-green mist cloud |
| Stun | `projectiles/debuff_stun/frames/` | 8-bolt lightning radiating from white star |

#### Split debuffs (2)
| Spell | Folder | Visual |
|---|---|---|
| Crumble Undead | `projectiles/debuff_crumble_undead/frames/` | Holy white/gold orb + orbiting bone shards |
| Fear (retro) | `projectiles/debuff_fear/frames/` | Dark purple wisp with glowing red eye-dots |

#### Special bolts (4)
| Spell | Folder | Visual |
|---|---|---|
| Chill Bolt | `projectiles/bolt_chill/frames/` | Diagonal frozen arrow with ice crystals + mist trail |
| Shock Bolt | `projectiles/bolt_shock/frames/` | Vertical yellow lightning zigzag |
| Elemental Bolt | `projectiles/bolt_elemental/frames/` | Multi-hue swirling orb with 3 colored streaks |
| Iban Blast | `projectiles/bolt_iban/frames/` | Crimson chaos blast with dark rune flecks |

#### Element family (1 — closes the 4-element set)
| Spell | Folder | Visual |
|---|---|---|
| FIRE | `projectiles/element_fire/frames/` | Hot teardrop flame, yellow-white core, ember sparks |

#### Retro buffs (4)
| Spell | Folder | Visual |
|---|---|---|
| Thick Skin | `projectiles/buff_thick_skin/frames/` | Brown stone heater shield with stone particles |
| Burst of Strength | `projectiles/buff_burst_of_strength/frames/` | Red clenched fist with yellow power-sparks |
| Rock Skin | `projectiles/buff_rock_skin/frames/` | Stone sphere with 3-5 orbiting rock chunks |
| Camouflage | `projectiles/buff_camouflage/frames/` | Green leaf cluster with pale central glow |

#### Utility spells (7)
| Spell | Folder | Visual |
|---|---|---|
| Low Alchemy | `projectiles/util_low_alch/frames/` | Single gold coin + sparkles |
| High Alchemy | `projectiles/util_high_alch/frames/` | 3 gold coins in triangle + many sparkles |
| Telekinetic Grab | `projectiles/util_telegrab/frames/` | Reaching hand glyph with aura |
| Bones to Bananas | `projectiles/util_bones_to_bananas/frames/` | Yellow banana with orbiting specks |
| Bones to Bread | `projectiles/util_bones_to_bread/frames/` | Brown loaf with falling crumbs |
| Superheat Item | `projectiles/util_superheat/frames/` | Grey ore melting into hot drips |
| Charge | `projectiles/util_charge/frames/` | Lavender pulsing orb + upward energy beams |

#### Charge orbs (4)
| Spell | Folder | Visual |
|---|---|---|
| Charge Air Orb | `projectiles/charge_air_orb/frames/` | Empty glass orb filling with pale gold |
| Charge Water Orb | `projectiles/charge_water_orb/frames/` | Filling with ice-blue |
| Charge Earth Orb | `projectiles/charge_earth_orb/frames/` | Filling with brown/moss |
| Charge Fire Orb | `projectiles/charge_fire_orb/frames/` | Filling with red flame |

#### City teleports (6, unique per city)
| Spell | Folder | Visual |
|---|---|---|
| Varrock Teleport | `projectiles/tele_varrock/frames/` | Blue rune circle with cardinal glyphs |
| Lumbridge Teleport | `projectiles/tele_lumbridge/frames/` | Warm cottage silhouette + chimney smoke |
| Falador Teleport | `projectiles/tele_falador/frames/` | White Saradomin cross with gold accents |
| Camelot Teleport | `projectiles/tele_camelot/frames/` | Royal purple crown with 3 spikes + red jewel |
| Ardougne Teleport | `projectiles/tele_ardougne/frames/` | Forest tree with orbiting leaves |
| Watchtower Teleport | `projectiles/tele_watchtower/frames/` | Stone tower silhouette with light beam |

#### Enchant tiers (5, escalating)
| Spell | Folder | Visual |
|---|---|---|
| Enchant Lvl 1 | `projectiles/enchant_lvl1/frames/` | 1-2 pale blue sparkles |
| Enchant Lvl 2 | `projectiles/enchant_lvl2/frames/` | Cyan + secondary sparkles |
| Enchant Lvl 3 | `projectiles/enchant_lvl3/frames/` | Yellow-gold burst with beams |
| Enchant Lvl 4 | `projectiles/enchant_lvl4/frames/` | Purple beams + sparkle ring |
| Enchant Lvl 5 | `projectiles/enchant_lvl5/frames/` | White-hot center + full corona |

### 1D — Triple-helix swirl + hybrid impacts (5 debuffs × 2 variants)

Some debuffs have alternative "swirl impact" and "hybrid swirl→explode" sequences in addition to their radial impact. Use these for spells where the visual should wrap the target rather than burst outward.

| Spell | Radial impact | Triple-helix swirl | Hybrid (swirl + explode) |
|---|---|---|---|
| Stun | `debuff_stun/impact/` | `debuff_stun/impact_swirl/` | `debuff_stun/impact_hybrid/` |
| Enfeeble | `debuff_enfeeble/impact/` | `debuff_enfeeble/impact_swirl/` | `debuff_enfeeble/impact_hybrid/` |
| Vulnerability | `debuff_vulnerability/impact/` | `debuff_vulnerability/impact_swirl/` | `debuff_vulnerability/impact_hybrid/` |
| Confuse | `debuff_confuse/impact/` | `debuff_confuse/impact_swirl/` | `debuff_confuse/impact_hybrid/` |
| Weaken | `debuff_weaken/impact/` | `debuff_weaken/impact_swirl/` | `debuff_weaken/impact_hybrid/` |

- **Radial impact:** 48×48, 4 frames, explodes outward
- **Triple-helix swirl:** 48×48, 4 frames, 3 ribbons spiral up the target's body (Weaken's swirls DOWN — strength dripping out)
- **Hybrid:** 48×48, **8 frames** = swirl (frames 0-3) → explosion (frames 4-7)

### 1E — Directional sprite variants (16 sprites)

For projectiles that have a clear "leading direction," authored 8 directional variants matching compass directions. **Engine needs a direction-picker to use these** (see §3).

| Sprite | Variants | Folder |
|---|---|---|
| RANGED arrow | N / NE / E / SE / S / SW / W / NW | `projectiles/2_ranged/directions/` |
| FIRE flame | Same 8 directions | `projectiles/element_fire/directions/` |

Each variant is a 30×30 PNG named `arrow_<dir>.png` or `flame_<dir>.png`.

---

## 2. Quick reference — total asset count

| Category | Sprite identities | Frames | PNG files |
|---|---:|---:|---:|
| Router projectile replacements | 7 | 4 each | 56 (28 native + 28 x8) |
| Combat impacts (radial) | 7 | 4 each | 56 (28 native + 28 x6) |
| Unique spell projectiles | 37 | 4 each | 296 (148 native + 148 x8) |
| Swirl impacts | 5 | 4 each | 40 |
| Hybrid impacts | 5 | 8 each | 80 |
| Directional variants | 16 | 1 each | 32 |
| **Total** | **~77 distinct identities** | | **~560+ PNGs** |

Plus per-variant animated GIFs and comparison/catalog board PNGs.

---

## 3. Engine work needed (TODO for the coder)

These are the items the art ambition is waiting on. Each is small-to-moderate code work. Ordered by recommended sequence.

### 3A — Sprite-pack injection for the router replacements (FAST WIN)

The 7 router projectiles (§1A) can drop in immediately by overriding sprites 3160-3166. The existing `Custom_Sprites.osar` system supports this.

**Tasks:**
1. Write a packer script that reads `~/ogrs/art/projectiles/0_orb/frames/frame_00.png` etc. and encodes them as zip entries 3160-3166 (or as a separate `Custom_Projectiles.osar` overlay pack) matching the format in `client/src/com/openrsc/client/model/Sprite.java::unpack()`.
2. Drop the pack in `client/Cache/video/spritepacks/`.
3. Add `Custom_Projectiles:1` line to `client/Cache/config.txt`.
4. Verify in-game: cast Wind Strike, see new ORB sprite instead of red disk.

**No router changes needed** — same 7 slots, just new art. **Smallest possible engine win.**

### 3B — Extended OgrsProjectileTypes router

To use the 37 unique sprites in §1C, the router needs more types. Currently `OgrsProjectileTypes.java` defines 7 constants (ORB=0, MAGIC=1, ..., BLANK=6).

**Tasks:**
1. Add ~37 new constants: `WIND_STRIKE`, `WATER`, `FIRE`, `CONFUSE`, `WEAKEN`, `VULNERABILITY`, `ENFEEBLE`, `STUN`, `CRUMBLE_UNDEAD`, `FEAR`, `CHILL_BOLT`, `SHOCK_BOLT`, `ELEMENTAL_BOLT`, `IBAN_BLAST`, `THICK_SKIN`, `BURST_STRENGTH`, `ROCK_SKIN`, `CAMOUFLAGE`, `LOW_ALCH`, `HIGH_ALCH`, `TELEGRAB`, `BONES_BANANAS`, `BONES_BREAD`, `SUPERHEAT`, `CHARGE`, `CHARGE_AIR`, `CHARGE_WATER`, `CHARGE_EARTH`, `CHARGE_FIRE`, `TELE_VARROCK`, `TELE_LUMBRIDGE`, `TELE_FALADOR`, `TELE_CAMELOT`, `TELE_ARDOUGNE`, `TELE_WATCHTOWER`, `ENCHANT1`-`ENCHANT5`.
2. Refine `forSpellName()` to route each spell to its specific type instead of collapsing onto the 7-slot ceiling.
3. Bump `EntityHandler.loadProjectiles()` to register the additional `SpriteDef` entries.
4. Author packing for the additional sprites into the override pack.

**~80 lines of Java change** plus packer script extension.

### 3C — Generic impact-effect renderer (NEW)

The impact sprites (§1B, §1D) need a renderer that doesn't currently exist.

**Tasks:**
1. Define a new sprite slot category for "impact" sprites — e.g., cache entries 3300+ for 48×48 impact frames.
2. After a projectile lands (engine already has a hook for projectile-arrived event), spawn a 4-frame (or 8-frame for hybrids) sprite animation centered on the target's screen position.
3. Animation plays once and disappears.
4. For hybrid (8-frame) impacts, support optional double-length playback.

### 3D — Direction-picker for 8-variant sprites

`§1E` authored 8 directional variants for arrow + flame. Engine needs to pick which one to render based on flight angle.

```java
public static int directionIndex(int casterX, int casterY, int targetX, int targetY) {
    double angle = Math.atan2(targetY - casterY, targetX - casterX);
    int idx = (int) Math.round(angle / (Math.PI / 4));
    return ((idx % 8) + 8) % 8;
}
// Returns 0=E, 1=SE, 2=S, 3=SW, 4=W, 5=NW, 6=N, 7=NE (or rotate as engine expects)
```

Then pick from `directions/{N,NE,E,SE,S,SW,W,NW}.png` accordingly.

### 3E — Crumble Undead death animation

When `Crumble Undead` fatally damages an undead NPC, play the crumble impact (already authored at `~/ogrs/art/projectiles/debuff_crumble_undead/impact/`) at the NPC's position instead of the normal death animation.

**Tasks:**
1. Add `is_undead` tag to NPC defs (or a runtime ID list). Tag: Skeleton, Zombie, Ghost, Banshee, Lesser Demon, etc.
2. Hook combat damage resolver: `if (spell == Spells.CRUMBLE_UNDEAD && npc.isUndead() && damage >= npc.hp)` → call `playCrumbleDeath(npc)`.
3. `playCrumbleDeath` spawns the 4-frame crumble impact at the NPC's tile, then removes the NPC.
4. Bonus: anchor the effect to the NPC sprite center (not tile center) for the satisfying "this creature is breaking" feel.

### 3F — Tier-escalation (DEFERRED — see `_specs/ROUTER_NOTES.md`)

For the long-term "Wind Strike vs Wind Wave look different" vision, add ~16 more sprite slots (4 elements × 4 tiers each) plus refine the router again. **Mockup already authored at `C:\OGRS_Art\_mockups\wind_tier_escalation.png`.** Not blocking — generic-per-element art (§1C FIRE) ships first.

---

## 4. File path reference

### WSL (source of truth)
```
~/ogrs/art/
├── projectiles/                  ← all spell sprites
│   ├── 0_orb/                    ← router slot 0 (Wind/Sara)
│   │   ├── frames/               ← 30×30 projectile (4 frames)
│   │   ├── impact/               ← 48×48 impact (4 frames)
│   │   └── _draw_orb.py          ← authoring script
│   ├── 1_magic/, 2_ranged/, ...  ← other router slots
│   ├── debuff_*/                 ← debuff-specific projectiles
│   ├── bolt_*/                   ← special bolts
│   ├── buff_*/                   ← retro buff spells
│   ├── util_*/                   ← utility spells
│   ├── charge_*_orb/             ← charge orb spells
│   ├── tele_*/                   ← teleport spells
│   ├── enchant_lvl*/             ← enchant tier spells
│   ├── element_fire/             ← FIRE element + directions
│   ├── _draw_combat_impacts.py   ← batched combat-impact drawer
│   ├── _draw_hybrids.py          ← hybrid-impact stitcher
│   ├── _draw_special_bolts.py    ← 4 special bolts batch
│   ├── _draw_retro_buffs.py      ← 4 buffs batch
│   ├── _draw_utility_spells.py   ← 7 utility batch
│   ├── _draw_charge_orbs.py      ← 4 charge orbs batch
│   ├── _draw_teleports.py        ← 6 teleports batch
│   └── _draw_enchants.py         ← 5 enchant tiers batch
├── _specs/
│   ├── SPEC.md                   ← canvas + format spec
│   ├── ROUTER_NOTES.md           ← engine prereqs (this file's source of truth)
│   └── decode_orsc_sprites.py    ← reusable sprite-cache decoder
├── reference/                    ← vanilla sprites decoded for reference
└── HANDOFF.md                    ← this file
```

### Windows mirror
```
C:\OGRS_Art\
├── spells\
│   ├── <each spell folder>\frames\ + .gif + comparison.png
│   ├── BATCH_X_BOARD.png         ← per-batch comparison boards
│   ├── MASTER_CATALOG.png        ← all 37 spells in one image
│   ├── IMPACTS_BATCH.png         ← debuff impact boards
│   ├── FINAL_HYBRID_BOARD.png    ← hybrid swirl+explode boards
│   ├── BATCH3_BOARD.png          ← debuff splits + special bolts
│   └── ...
├── projectiles\                  ← router sprites + their impacts
│   ├── COMBAT_IMPACTS_BOARD.png
│   ├── DIRECTIONAL_ROSETTE.png   ← 8-direction arrow + flame
│   └── MASTER_COMPARISON.png     ← old vanilla vs new 7 router sprites
├── reference\                    ← decoded vanilla sprites
├── README.md
├── SPEC.md
├── ROUTER_NOTES.md               ← engine prereqs
└── SPELL_CATALOG.md              ← spell inventory
```

---

## 5. Recommended implementation order (sequence the coder should follow)

1. **§3A** — Pack the 7 router projectiles. Instant in-game payoff. 1 session.
2. **§3C** — Build the impact renderer. Unlocks every impact sprite we authored. 1 session.
3. **§3A again** — Pack the impacts using the renderer from step 2. 1 session.
4. **§3B** — Extend the router for the 37 unique spells. 1-2 sessions including packing.
5. **§3E** — Crumble Undead death animation. 1 session.
6. **§3D** — Direction-picker. 1 session.
7. **§3F** — Tier escalation (DEFERRED — only if/when desired).

**Estimated total engine work for steps 1-6: ~5-7 focused sessions.** All art is done; this is purely wiring.

---

## 6. Things the coder should know (gotchas + project context)

### Sprite cache format

The `Authentic_Sprites.orsc` archive is a ZIP. Each entry (named by numeric ID) is a single sprite blob with this format (from `client/src/com/openrsc/client/model/Sprite.java`):

```
int width  (4 bytes big-endian)
int height (4 bytes BE)
byte requiresShift (1 byte)
int xShift (4 bytes BE)
int yShift (4 bytes BE)
int something1 (4 bytes BE)
int something2 (4 bytes BE)
int[width*height] pixels (4 bytes ARGB each, BE)
```

Header = 25 bytes. PNG → this format conversion is straightforward.

The `Custom_Sprites.osar` pack format is different — gzipped + subspace/entry/frame structure. Documented in `client/src/orsc/graphics/two/SpriteArchive/Unpacker.java`. **Use whichever is convenient for the impact-effects pack; the engine reads both.**

### Color collisions to be aware of in the existing router

`OgrsProjectileTypes.java` currently maps:
- Wind & Saradomin Strike → both `ORB`
- Water & Fire → both `MAGIC`
- Earth & Snare/Bind → both `SPIKEBALL`
- Curse/Weaken & Flames of Zamorak & poison arrows → all `SKULL`

§3B fixes these by adding per-spell slots.

### What `_draw_*.py` scripts produce

All `_draw_*.py` scripts in the art tree produce both native-resolution PNGs (the game-size assets, e.g. 30×30) and upscaled `_x6.png` or `_x8.png` (for human inspection only — **do not pack the upscaled versions** into the sprite archive).

### Anti-patterns to avoid when packing

- Don't include the `_x6.png` / `_x8.png` upscales in the sprite pack. Only the native-resolution `frame_NN.png` files.
- Don't pre-multiply alpha. The archive format expects unpremultiplied RGBA.
- Don't crop tightly to the visible pixels — the engine uses the full canvas dimensions for positioning. A 30×30 sprite stays 30×30 even if most pixels are transparent.

---

## 7. Iteration / new art

If anything needs revision, the `_draw_*.py` scripts are the entry point — edit, re-run, the PNGs regenerate. The Windows mirror at `C:\OGRS_Art\` is not auto-synced; manual sync is fine since it's the reviewer/coder view, not the source of truth.
