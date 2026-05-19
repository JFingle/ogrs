# Projectile 0 — ORB

## Where it appears in-game

`OgrsProjectileTypes.ORB` is routed to by `OgrsProjectileTypes.java`:

- **Wind / Air spells** — `Wind Strike`, `Wind Bolt`, `Wind Blast`, `Wind Wave` (via `forSpellName("wind"|"air")`)
- **Saradomin Strike** — the god spell (light/holy via `forGodSpell`)
- **Mithril arrows** — visual upgrade for mid-tier arrows (via `forArrow`)

So this single sprite has to read as both *moving air* and *holy light* depending on the caster. That's actually friendlier than it sounds — both ideas converge on **pale, fast, weightless, slightly luminous**. Think "blessed gust."

## The vanilla baseline we're replacing

`reference/proj_3160_ORB_x8.png` — a solid orange disk with a chunky red ring. Reads as generic "magic ball." No motion, no character, no element. Every Wind spell and Saradomin Strike in the entire game uses this exact sprite today.

## Design direction

| Quality | Target |
|---|---|
| Silhouette | Round-ish core with **streaks trailing behind** (the "wind" tell) |
| Core color | Pale gold / cream / off-white — luminous, not orange |
| Ring color | Soft warm white or very faint cyan-white halo (NOT red, that's vanilla's identity) |
| Streak color | Whitish-blue or pure white, semi-transparent feel done via dithering |
| Motion read | Should feel like it's *moving toward the target* even when shown static |

## Frame plan (4 frames)

The engine currently shows `frame_00` only — drawing 4 lets us cycle when the multi-frame projectile system lands later (see project_ogrs.md backlog "projectile system").

| Frame | Visual |
|---|---|
| `frame_00.png` | **Base.** Bright cream core (~10 px diameter), 2-3 short streaks trailing **upper-left** (assuming projectile flies toward lower-right). Faint halo. The "default" frame the engine will use right now. |
| `frame_01.png` | Streaks rotated ~90° (now trailing upper-right). Core slightly smaller. Halo slightly brighter. |
| `frame_02.png` | **Peak.** Core at brightest (touch of pure white in the middle). Streaks rotated ~180°. Halo at widest. |
| `frame_03.png` | Streaks rotated ~270°. Core dim again. Halo fading. Loops back to 00. |

Goal is a 4-tick **breathing / rotating** loop that reads as airborne, not a strobe.

## Palette suggestion (5-7 colors)

| Use | Hex | Where |
|---|---|---|
| Core highlight | `#FFF7D0` | Center 2-3 px |
| Core base | `#F5E6A0` | Inner ring of core |
| Core shade | `#D9C268` | Outer ring of core |
| Halo bright | `#E8EDF5` | Inner halo |
| Halo dim | `#B9C4D4` | Outer halo / streak shadow |
| Streak | `#FFFFFF` | Streak highlight |
| Streak shadow | `#7A8FAD` | Streak edge / dither |

Use sparingly — RSC sprites at 30×30 lose hue distinctions fast. **Value contrast > hue contrast.**

## Anti-patterns (specific to this orb)

- ❌ Don't make it look like the existing red/orange orb just retinted — needs a different shape language
- ❌ Don't add a full corona / soft glow — won't survive paletization, looks "modern" not RSC
- ❌ Don't make streaks longer than ~6 px — they clip and confuse the silhouette
- ❌ Don't center the core dead-middle — bias toward the leading edge so the motion read is clear

## Reference imagery

- `~/ogrs/art/reference/proj_3160_ORB_x8.png` — the thing we're replacing (8× upscale for visibility)
- For wind-feel: OSRS air rune icon, classic RSC magic-rune sprites
- For holy-light-feel: any Saradomin imagery you have on hand from the source material

## Canvas

`frames/frame_00.png` through `frames/frame_03.png` are pre-seeded as 30×30 fully-transparent PNGs. Open in your editor, draw, save back over the same filename.

Read `~/ogrs/art/_specs/SPEC.md` if you haven't yet for the format constraints.
