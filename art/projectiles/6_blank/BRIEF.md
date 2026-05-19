# Projectile 6 — BLANK (tiny darts / micro-projectile flicker)

## Where it appears in-game

- **Bronze / Iron / Steel / Mithril throwing darts** (via `forArrow`)
- Engine source labels it "invisible/no-render" — the *intended* use is essentially nothing

## Design intent

Not literally invisible — that's boring. A **2-3 pixel flicker** that suggests a tiny projectile in flight without dominating the screen. Darts in OSRS are barely-visible because they're SMALL, fast, and silver — so we lean into that: micro silver streak.

## Vanilla baseline

`reference/proj_3166_BLANK_x8.png` — mostly empty. Reference has nothing to compete with — we just need to be appropriately tiny.

## Frame plan

| Frame | Visual |
|---|---|
| `frame_00.png` | 2-pixel silver streak — base |
| `frame_01.png` | Slight position shift, 1 trail pixel |
| `frame_02.png` | **Peak.** 3-pixel streak with white tip |
| `frame_03.png` | Single dim pixel (almost gone) |

## Palette

| Use | Hex |
|---|---|
| Streak tip | `#FFFFFF` |
| Streak body | `#D8D8D8` |
| Streak trail | `#808088` |
| Dim trail | `#4A4A52` |

Designed to be a subtle accent at native render size, almost imperceptible from a distance but clearly "something flew there" up close.
