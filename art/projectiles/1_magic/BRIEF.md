# Projectile 1 — MAGIC (Ice-themed)

## Where it appears in-game

`OgrsProjectileTypes.MAGIC` is the default and is routed to by:
- **Water spells** — Water Strike / Bolt / Blast / Wave
- **Fire spells** — Fire Strike / Bolt / Blast / Wave  *(collision: same sprite for now)*
- Default fallback for any spell the router doesn't recognize

## Element choice — Water/Ice

Going **ice** because:
- The MAGIC slot collides between Water and Fire today. Picking ice gives us a coherent water-element identity now; when the router gets extended to split FIRE into its own slot, we'll add a separate fire sprite then.
- Vanilla MAGIC (sprite 3161) is purple/blue — closer to water already, so swapping to ice is a believable evolution.
- Ice silhouette is more distinct from the ORB's round shape — important for visual differentiation at native render size.

## Vanilla baseline

`reference/proj_3161_MAGIC_x8.png` — a chunky 8-pointed purple/blue star. Reads "magic burst." We want something with a stronger frost identity.

## Design direction

- **Silhouette:** crystalline / diamond, NOT round — must read different from the ORB at 30×30
- **Core:** rhombus / 4-point crystal, icy-white center with cyan body
- **Halo:** thin pale-blue ring, slightly faceted (squarish rather than circular)
- **Streaks:** 4 short shards extending on the diagonals (between the core's points)
- **Motion:** core scales subtly each frame; shards extend & retract; halo brightens at peak

## Frame plan

| Frame | Visual |
|---|---|
| `frame_00.png` | **Base.** Diamond core, dim halo, shards at minimum extension. |
| `frame_01.png` | Shards extending, halo brightening. Core unchanged. |
| `frame_02.png` | **Peak.** White core center, halo at brightest, shards at max length, an extra ring of frost specks at the outermost edge. |
| `frame_03.png` | Pulling back: shards retracting, halo dimming, returning toward frame_00 state. |

## Palette

| Use | Hex |
|---|---|
| Core peak (frame 02 center) | `#FFFFFF` |
| Core highlight | `#E0F5FF` |
| Core base | `#A8DEFF` |
| Core shade | `#5BA8E5` |
| Halo bright | `#BAD6EE` |
| Halo dim | `#6E8CAA` |
| Shard bright | `#FFFFFF` |
| Shard mid | `#BAD6EE` |
| Shard dim | `#4A6680` |

All cool tones — no warm pixels anywhere on this sprite (that's what'll signal "Fire" when we add it later).

## Anti-patterns

- ❌ Round core (collides visually with ORB)
- ❌ Yellow / warm highlights (saves those for Fire/Saradomin)
- ❌ Long thin streaks like the ORB has — shards should be short and chunky to read as ice fragments not air motion
