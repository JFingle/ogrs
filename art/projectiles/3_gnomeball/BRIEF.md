# Projectile 3 — GNOMEBALL (nature / balance)

## Where it appears in-game

- **Claws of Guthix** — god spell, balance/nature
- **Alchemy** (Low/High), **Telegrab**, **Heal Other**, **Plank Make** — utility spells
- Currently a catch-all for "non-elemental, non-combat" spell mechanics

## Vanilla baseline

`reference/proj_3163_GNOMEBALL_x8.png` — orange-and-tan striped ball (it's literally the gnomeball quest item). Doesn't read as nature or balance — just looks like a stitched leather ball.

## Element / mood

**Nature green** — moss, leaf, vine. Round-orb silhouette so it reads as Guthix's claws-of-nature, plus stands as a "magic utility orb" for the alchemy/telegrab use cases. Differentiates from ORB (gold/cream wind) and MAGIC (cyan ice diamond) by hue alone.

## Design direction

- **Silhouette:** round orb (similar to ORB shape language — both are "magic orbs", distinguish by color + petal pattern)
- **Petals not streaks** — instead of long thin wind streaks, draw 4 small leaf/petal lobes at the cardinal positions (chunky, 2-3 px wide × 2 px tall)
- **Motion:** petals rotate around the orb each frame (0°, 90°, 180°, 270° in 8 directions = 8 frames, but we only need 4)
- **Core:** moss-green with pale-yellow-green highlight
- **Halo:** soft chartreuse ring

## Frame plan

| Frame | Visual |
|---|---|
| `frame_00.png` | **Base.** Petals at N/E/S/W positions, dim halo |
| `frame_01.png` | Petals rotated 22.5° (NE/SE/SW/NW shifted), halo brightening |
| `frame_02.png` | **Peak.** Petals at NE/SE/SW/NW (full diagonals), white core center, halo widest |
| `frame_03.png` | Petals returning, halo dimming |

## Palette

| Use | Hex |
|---|---|
| Core peak | `#FFFFFF` |
| Core highlight | `#E8F5C0` |
| Core base | `#A8D060` |
| Core shade | `#5A8A28` |
| Halo bright | `#C5E5A0` |
| Halo dim | `#7AA050` |
| Petal bright | `#E8F5C0` |
| Petal base | `#A8D060` |
| Petal shade | `#3A5818` |

All cool-to-warm greens, no blue (that's MAGIC) and no yellow-gold (that's ORB).
