# Projectile 2 — RANGED (arrow / bolt)

## Where it appears in-game

- All default arrows (bronze → adamant when not tier-flagged in router)
- The "bolt" spell mechanic via `forSpellName("bolt")`
- Most-used projectile sprite by usage volume — every basic bow shot

## Vanilla baseline

`reference/proj_3162_RANGED_x8.png` — a green 8-pointed star (identical shape to MAGIC, just recolored). This is genuinely the worst vanilla sprite: an arrow that doesn't look like an arrow.

## Design direction

- **Actual arrow silhouette** — wood shaft + iron tip + fletching at tail
- Diagonal orientation, tip toward upper-right (most-common projectile travel angle in isometric view)
- Reads in motion regardless of flight direction (the sprite doesn't rotate per shot)
- Motion suggested by **glint cycle** moving along the shaft frame by frame

## Frame plan

| Frame | Visual |
|---|---|
| `frame_00.png` | Base arrow — no glint, plain wood + iron tip + white fletching |
| `frame_01.png` | White glint pixel midway up the shaft |
| `frame_02.png` | **Peak.** Glint at the tip; tip has a pure-white flash pixel |
| `frame_03.png` | Speed lines behind the fletching (2-3 short trailing pixels) |

## Palette

| Use | Hex |
|---|---|
| Wood shaft highlight | `#A8723A` |
| Wood shaft base | `#8B5A2B` |
| Wood shaft shade | `#5C3A1A` |
| Iron tip highlight | `#D0D0D0` |
| Iron tip shade | `#6A6A6A` |
| Fletching | `#E8E8E8` |
| Fletching shade | `#888888` |
| Glint / peak flash | `#FFFFFF` |
| Motion trail | `#888888` |
