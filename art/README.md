# OGRS Art Workspace

Pure art track — author here without touching server/client code. Integration into the running game (encoding PNGs into `.osar` sprite packs, wiring `config.txt`, rebuilding the client cache) is a separate engine pass and is **not blocking** this work.

## Layout

```
art/
├── _specs/
│   └── SPEC.md           ← canvas size, palette, frame conventions
├── reference/             ← extracted vanilla sprites (decoded from the .orsc archives)
└── projectiles/
    ├── 0_orb/            ← Wind/Air spells, Saradomin Strike, mithril arrows
    │   ├── BRIEF.md
    │   └── frames/
    │       ├── frame_00.png   ← author here
    │       ├── frame_01.png
    │       ├── frame_02.png
    │       └── frame_03.png
    ├── 1_magic/          ← default magic, Water/Ice/Fire (until elements split)
    ├── 2_ranged/         ← arrows, default bolts
    ├── 3_gnomeball/      ← Alch / Telegrab / Heal / Plank Make, Claws of Guthix
    ├── 4_skull/          ← Curse / Crumble / Weaken / poison arrows / Flames of Zamorak
    ├── 5_spikeball/      ← Earth/Rock spells, Snare/Bind/Entangle, adamant arrows
    └── 6_blank/          ← intentional no-render (small darts)
```

## Workflow

1. Read `_specs/SPEC.md` once — canvas is **30×30 transparent PNG**, classic RSC palette feel.
2. Pick a projectile folder. Read its `BRIEF.md`.
3. Open the seeded `frame_NN.png` files in your editor (Aseprite / Photoshop / Krita / GIMP). Draw.
4. Save back over the same filenames in `frames/`.
5. When a projectile set feels done, tell me — I'll encode it into a `Custom_Projectiles.osar` pack and wire it into `client/Cache/video/spritepacks/` so you can see it in-game.

## Why projectiles first

`server/src/com/openrsc/server/util/OgrsProjectileTypes.java` already routes 7 distinct projectile types through the engine — `forArrow(ammoId)`, `forSpellName(name)`, `forGodSpell(spell)`. **All 7 currently map to the same vanilla blue/green orb** because no custom art exists yet. Replacing the art is the highest-leverage visual upgrade in the project: every spell cast, every arrow fired, every god-spell — all instantly differentiate without a single line of engine code changing.
