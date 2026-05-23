# OGRS Sprite Spec — Projectile + Impact Pack

Two sprite categories with two canvas sizes:

| Category | Canvas | Frames | What it is |
|---|---|---|---|
| **Projectile** | 30 × 30 | 4 | What flies through the air from caster → target |
| **Impact effect** | 48 × 48 | 4 | What plays on the target square AFTER the projectile lands — wraps + dissipates around the model |

Impact effects are authored as 4-frame sequences with a strict shape arc:
1. **frame_00** — small at impact point (just landed)
2. **frame_01** — expanding outward (energy spreading)
3. **frame_02** — peak: wraps around target silhouette (max size)
4. **frame_03** — dissipating (fading wisps, ember remnants)

The 48×48 canvas is large enough to engulf a player/NPC sprite. The engine pass that wires up impact rendering (different sprite slot from projectiles) is **not blocking** authoring — sprites can sit staged.

## Canvas (projectile — 30 × 30)

| Property | Value |
|---|---|
| Frame size | **30 × 30 pixels** |
| Bounds box | 32 × 32 (1-px transparent margin all sides) |
| Format | PNG, RGBA, 8-bit per channel |
| Background | **Fully transparent** (alpha = 0) — DO NOT use magenta-key; engine pack format honors PNG alpha |
| Color depth | Author in true color, palette quantization happens at pack time |

The 30×30 size matches the vanilla projectile entries (verified by decoding `3160` from `Authentic_Sprites.orsc`). Keep the actual drawn pixels within a ~28×28 inner area so rotation / flight motion doesn't clip.

## Frames per projectile

| Frame | Purpose |
|---|---|
| `frame_00.png` | Default static — used by the current engine without further work |
| `frame_01.png` | Flight pulse 1 — slight intensity variation, ~25% rotation if applicable |
| `frame_02.png` | Flight pulse 2 — peak intensity, ~50% rotation |
| `frame_03.png` | Flight pulse 3 — fading edge, ~75% rotation |

The engine today only shows `frame_00`. Authoring 4 frames now means when the projectile-animation system lands (memory backlog item, Phase 4), we already have the assets for cycling flight animation. **Just want to author frame_00 and stop? That's fine — leave 01-03 as the blank seeded canvases.**

## Palette guidance (classic RSC feel)

RSC sprites are pre-2002 — limited palette, no anti-aliasing in the modern sense, chunky pixels. To stay on-style:

- **Limit palette to ~16-32 colors per sprite.** Sparky has authored RSC clone art — he knows the look.
- **No sub-pixel detail** below the 1px grid. No translucent edges except a single ring of darker pixels for shape suggestion.
- **High value contrast** — RSC sprites read at small render sizes by relying on light/dark separation, not subtle hue shifts.
- **Saturated, slightly desaturated jewel tones** — picture Sea Slug-era graphics, not late OSRS rebake quality.

## Anti-pattern checklist

- ❌ Full-opacity background pixels (anywhere outside the actual orb/arrow/effect)
- ❌ Modern soft-glow with multiple alpha gradients (kills the RSC feel)
- ❌ Drawing past the 30×30 boundary (will clip at pack time)
- ❌ Using "magenta = transparent" — the `.osar` pack format reads PNG alpha directly

## Integration (deferred — not blocking authoring)

When a projectile set is ready:

1. I pack the PNGs into `Custom_Projectiles.osar` using the `Entry`/`Frame` schema from `client/src/orsc/graphics/two/SpriteArchive/`.
2. Pack lands in `client/Cache/video/spritepacks/Custom_Projectiles.osar`.
3. Add `Custom_Projectiles:1` line to the client's `config.txt`.
4. On next client launch, `mudclient.loadSprites()` reads the pack via `Unpacker.unpackArchive()` and overrides the authentic sprite entries by ID.
5. Spells/arrows/god spells immediately render with the new art — no engine changes needed because `OgrsProjectileTypes` already routes them.

This integration step lives outside this `art/` workspace and is engine work for later.
