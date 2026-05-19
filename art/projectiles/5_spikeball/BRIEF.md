# Projectile 5 — SPIKEBALL (earth / weight / bind)

## Where it appears in-game

- **Earth Strike / Bolt / Blast / Wave** — earth element spells
- **Snare / Bind / Entangle / Hold** — physical-restraint spells (collision with Earth in router)
- **Adamantite arrows** — tier-themed weight read

## Vanilla baseline

`reference/proj_3165_SPIKEBALL_x8.png` — a brown spiked ball. Functional but bland; no terrain feel.

## Design direction

- **Tumbling boulder silhouette** — asymmetric, jagged, NOT round
- Brown stone + mossy green patches (earth + nature read)
- Reads as **heavy / physical / grounded** — counterpoint to ORB's airy lightness and MAGIC's brittle ice
- Frame cycle = tumbling rotation: 4 distinct rock orientations + small dust trail particles behind

## Frame plan

| Frame | Visual |
|---|---|
| `frame_00.png` | Boulder orientation A — spikes upper-right, moss patch on left |
| `frame_01.png` | Boulder orientation B (rotated ~90°) — spikes upper-left, moss patch on bottom |
| `frame_02.png` | Boulder orientation C (rotated ~180°) — spikes lower-left, **peak**: extra highlight + dust kick |
| `frame_03.png` | Boulder orientation D (rotated ~270°) — spikes lower-right, dust trail visible |

## Palette

| Use | Hex |
|---|---|
| Stone outline | `#1A140C` |
| Stone deep | `#3A2818` |
| Stone base | `#6B4520` |
| Stone highlight | `#A07050` |
| Stone peak (lit edge) | `#D49870` |
| Moss bright | `#688030` |
| Moss shade | `#3A4A18` |
| Dust particle | `#8B6A45` |
| Dust trail dim | `#4A3520` |
