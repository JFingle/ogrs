# Projectile 4 — SKULL (curse / death / chaos)

## Where it appears in-game

- **Curse**, **Weaken**, **Crumble Undead** — debuff spells
- **Flames of Zamorak** — chaos god spell
- All **poison-tipped arrows** (Poison Bronze through Poison Rune)
- Top-tier **Rune arrows** (visual menace)

## Vanilla baseline

`reference/proj_3164_SKULL_x8.png` — a cartoony red-and-tan skull. Reads more "pirate flag" than "instrument of death."

## Design direction

- **Actual skull silhouette** — small but recognizable, with two black eye sockets, nose hole, grinning teeth
- **Cursed flame trail rising above** — dark red flames (for Zamorak / poison association), 3 flickering wisps
- **Bone color violet-grey, not warm tan** — cold-bone aesthetic, not cartoony
- Skull is bottom-anchored on the canvas; flames burn upward (gives a sense of weight + drift)

## Frame plan — flames flicker

| Frame | Visual |
|---|---|
| `frame_00.png` | Skull + flames in baseline shape — short wisps |
| `frame_01.png` | Flames extend, second wisp gains a tongue offshoot |
| `frame_02.png` | **Peak.** Flames at maximum height; bright yellow core in flame tips |
| `frame_03.png` | Flames retracted, ember sparks lingering above |

## Palette

| Use | Hex |
|---|---|
| Bone outline | `#1A1020` |
| Bone shade | `#5A4860` |
| Bone base | `#9080A0` |
| Bone highlight | `#C8C0D0` |
| Skull cavity (eyes/nose/teeth gaps) | `#0A0410` |
| Flame deep | `#501020` |
| Flame outer | `#C0301F` |
| Flame mid | `#FF8030` |
| Flame core | `#FFE0A0` |
| Ember spark | `#FFFFFF` |
