# OGRS UI Track — Artist Spec

> **For the artist.** Companion to `CODER_HANDOFF.md`. Lists the UI art OGRS needs, in priority order, with deliverables (size, count, naming, color hints) and what each unlocks engine-side.

---

## TL;DR

- Eight batches in priority order — Tier 1 closes gaps in features we already shipped; Tier 3 is branding polish.
- All sprites delivered as **32×32 native PNG + 256×256 x8 preview PNG** (same as existing item sprites), unless noted otherwise.
- Sync to `C:\OGRS_Art\ui\<batch>\` for review.
- Author the matching `_draw_*.py` next to each batch so anything can be regenerated/iterated.
- One `BOARD.png` per batch so sparky can eyeball the full set at once.

---

## Style guide

- **Palette:** RSC-era warm pixel art — earthy browns, muted greens, parchment cream, ember orange, deep blue, blood red. Avoid neon. Mind the 16-bit feel.
- **Outline:** 1px dark outline on icons that float over varied backgrounds (skill tab, tab strip). No outline for icons on a fixed UI panel.
- **Detail density:** readable at native 32×32, recognizable at 16×16. Don't pack detail that vanishes when small.
- **Negative space:** leave 1-2px padding inside the 32×32 frame so icons don't crowd each other in tight UI strips.
- **Consistency:** when a batch is multiple icons in a set (e.g. skill icons), use a shared visual language — same outline weight, same lighting direction, same color saturation.

---

## Tier 1 — Closes gaps in shipped features (high urgency)

### Batch UI-01: Poison status icon ⚡ TOP PRIORITY

- **Deliverables:** 1 sprite, 24×24 + 96×96 preview (smaller than items — overlays the HP bar)
- **What:** A small green skull or venom-drop icon shown above/beside the player's HP when poisoned. Pulses subtly (2 frames if you want animation).
- **Why now:** We just shipped the Crypt Spider Matron whose attacks apply poison. **There is currently no visual indicator the player is poisoned** — only the HP ticking down gives it away.
- **Color hint:** Sickly yellow-green (#8FBC2A or similar), darker outline.
- **Optional 2-frame anim:** drip falling / skull breathing. The engine can flip between frames every ~600ms.
- **Engine wire:** mudclient.java renders the icon over the HP bar when `player.isPoisoned()` returns true. Single sprite slot.

### Batch UI-02: Slayer task HUD widget

- **Deliverables:** 1 sprite, 48×24 (wider than tall — sits in a HUD corner) + preview
- **What:** A small floating widget — Slayer-gem icon on the left, then text area for "Goblin × 7" (NPC name × remaining count). Black-and-gold border, dark interior.
- **Why now:** The Slayer enchanted gem (item 1610) gives the count on "Rub" — but players want a glance, not a click. The widget renders persistently while a task is active.
- **Color hint:** Deep purple gem (matching the gem item's amethyst tint), gold border on near-black background. Text area transparent so the engine paints the dynamic count.
- **Engine wire:** mudclient.java reads SlayerService state per frame, paints the widget at a fixed HUD corner when a task is active.

### Batch UI-03: Skill icon set including Slayer

- **Deliverables:** **19 icons** — one per skill — at 16×16 native + 64×64 preview. (Skills tab uses 16px slots.)
  - Authentic 18: Attack, Defense, Strength, Hits, Ranged, Prayer, Magic, Cooking, Woodcutting, Fletching, Fishing, Firemaking, Crafting, Smithing, Mining, Herblaw, Agility, Thieving
  - New OGRS: **Slayer** (single new icon — dynamic skill we already added)
- **Why now:** Today's skill panel uses upstream's tiny pre-2003 icons. A unified set + the brand-new Slayer icon (which currently shows nothing custom) is a visible upgrade every time the player opens the Skills tab.
- **Color hint per skill:** match RSC's traditional skill colors (Attack=red, Mining=brown, Cooking=orange, Slayer=dark green/black, etc.). Keep the palette consistent across the set.
- **Engine wire:** sprite pack at known indices; mudclient.java's skill-tab render loop already iterates per skill — point it at the new sprite IDs.

### Batch UI-04: Combat tab style icons

- **Deliverables:** 4 icons, 24×24 + previews
  - Sword (Attack)
  - Shield (Defense)
  - Fist (Strength)
  - Sword + Shield together OR a target reticle (Ranged)
- **Why now:** Combat tab currently shows text labels ("ATK / DEF / STR / ALL" on Android, "Attack / Defense / Strength / Ranged" desktop). Icons read instantly — players don't have to parse text mid-fight to switch combat style.
- **Color hint:** metallic grey/silver weapons with red/blue/green/yellow accent stripe per style, matching RSC's traditional combat-style coloring.
- **Engine wire:** mudclient.java's combat tab dialog uses sprite slots in place of strings.

---

## Tier 2 — Visible every session (medium urgency, big polish payoff)

### Batch UI-05: Tab strip icons

- **Deliverables:** **9 icons**, 28×28 + previews (tabs are 32×32 frames with 2px inner padding)
  - Inventory (backpack)
  - Minimap (compass / map)
  - Skills (laurel wreath / quill)
  - Magic (spellbook / staff)
  - Prayer (folded hands / cross + dove)
  - Friends (two heads / shaking hands)
  - Combat (crossed swords)
  - Options (gear / wrench)
  - Keyboard (only used on Android — keyboard icon)
- **Why now:** The tab strip is visible literally every session, every screen. Custom OGRS-branded tabs differentiate the fork at first glance.
- **Color hint:** consistent muted parchment-cream icons against the dark tab background; gold highlight when active.
- **Engine wire:** swap the sprite IDs in mudclient.java's tab-strip render loop.

### Batch UI-06: Run-energy widget icon

- **Deliverables:** 1 sprite, 24×24 + preview. **Two variants:** running (red boot) + walking (grey boot).
- **What:** A boot/foot icon that replaces today's "RUN: 87%" text overlay. The numerical percent paints below as before.
- **Why now:** Today's widget is literally a colored box with the word "RUN" and a percent — functional but ugly. A boot icon plus the dynamic bar/percent feels like an actual game UI.
- **Color hint:** running = red leather boot with motion lines, walking = grey/brown standing boot. The energy bar below stays color-tiered (green → yellow → red).
- **Engine wire:** mudclient.java has the existing run icon at top of screen — swap the placeholder for the sprite, keep the bar/percent overlay.

### Batch UI-07: Cursor variants

- **Deliverables:** 4 cursors, 16×16 with hotspot marked + 64×64 preview
  - Walk (default — boot footprint)
  - Attack (crossed swords)
  - Talk (speech bubble)
  - Use (hand with sparkle / "use" gesture)
- **Why now:** Default cursors are upstream's stock. Contextual cursors are a "feels professional" upgrade — players know what their click will do before they click.
- **Color hint:** bright primary colors so they read on any background; bold black outline so they survive dark tiles.
- **Engine wire:** mudclient.java already has hover-action detection; just point the cursor draw at the new sprite based on the action context.

---

## Tier 3 — Branding / first impression (lower urgency, high "feels like ours" impact)

### Batch UI-08: Login splash background

- **Deliverables:** 1 painting, 512×384 (or 1024×768 if the engine supports it — check before authoring large)
- **What:** Full-screen art shown behind the login form. Suggested compositions (pick one):
  - Lumbridge skyline at dawn with the castle silhouette
  - The crypt entrance hatch with mist rising from it
  - The Grizzled Traveler standing on a cliff overlooking Gielinor
  - A wide-shot of the spider chamber's deepest pit
- **Why now:** First impression. You replaced the wolf splash with an OGRS banner — a real painting is the next step.
- **Color hint:** rich painterly style, warm dusk/dawn lighting, RSC-era color palette but with more painterly gradient than pure pixel art is fine here (login screen is a low-frequency surface).
- **Engine wire:** swap `client/Cache/video/library.orsc`'s login-bg entry, OR add as a new overlay if library.orsc is too rigid.

### Batch UI-09: Dialog box frame

- **Deliverables:** 1 frame asset — a 9-slice border (4 corners + 4 edges + 1 center) so the engine can tile it to any dialog box size. Each tile ~24×24.
- **What:** Replaces RSC's stock cream-and-brown chatbox border with an ornate OGRS frame.
- **Why now:** NPC dialog is the second-most-shown UI surface after the tab strip. Subtle but always there.
- **Color hint:** wood + brass ornament corners, parchment interior, slight aged-paper texture if it doesn't compress out at 24×24.
- **Engine wire:** mudclient.java's dialog renderer needs to switch from solid-color box to a 9-slice render — small code change.

---

## What's NOT in this spec (and why)

- **Achievement toast notifications** — needs an engine subsystem (event queue, toast manager) before art helps. Defer until the subsystem is in.
- **Hotbar / action bar** — same. Build the engine surface first; art comes after.
- **Quest log panel** — backlog item #17; not yet started.
- **Spellbook category tab icons** — wait for backlog #22 (alternate spellbooks) to land.
- **Healthbar over NPCs** — backlog item; needs engine work to render over NPC heads first.
- **Damage splat backgrounds** — current numbers work fine; visual upgrade is low ROI vs other tracks.

If sparky says "we're going to build X" and X is on this NOT list, ping the artist then — that's when the art becomes useful.

---

## Deliverable conventions (matching other art tracks)

Every batch ships:

1. **Native PNG** at the icon's working size (16, 24, 28, 32 — per batch above)
2. **x8 preview PNG** at 8× scale, for sparky to eyeball
3. **`BOARD.png`** — every icon in the batch laid out in a grid, labeled, so sparky can see the full set
4. **`_draw_<batch>.py`** — the authoring script. Re-runnable. Edit + re-run to iterate.
5. **Folder under `~/ogrs/art/ui/<batch_name>/`** plus a sync copy at `C:\OGRS_Art\ui\<batch_name>\`
6. **README.md** in the batch folder noting any deviations from this spec (e.g., "rangedlevel icon swapped to crosshair because target-reticle read poorly at 16×16")

---

## Naming convention

`<batch>_<item>_<size>.png` — e.g.:
- `ui03_skill_slayer_16.png`
- `ui03_skill_slayer_x8.png`
- `ui05_tab_inventory_28.png`
- `ui01_poison_status_24.png`
- `ui01_poison_status_x8.png`

If a sprite is animated, suffix with `_frame_NN`:
- `ui01_poison_status_frame_00.png`
- `ui01_poison_status_frame_01.png`

---

## Iteration loop

When sparky reviews a batch:
- "Looks great, ship it" → coder integrates per pattern in `CODER_HANDOFF.md`
- "Redo with X different" → edit the `_draw_*.py`, re-run, push the new BOARD.png
- "Scrap this batch" → mark in `_specs/UI_TRACK_SPEC.md` as "rejected: <reason>" so we don't re-author the same idea

---

## Quick-start for the artist

Tier 1 first. Within Tier 1, order is:

1. **UI-01 Poison status icon** — single sprite, ~30 min, immediately useful (matron fight today)
2. **UI-02 Slayer HUD widget** — single sprite, ~45 min, eliminates the "rub gem to check" friction
3. **UI-03 Skill icon set (19 icons)** — bigger batch, ~2-3 hours, hits every Skills-tab open
4. **UI-04 Combat tab icons (4)** — small batch, ~1 hour, every combat session

Then Tier 2, then Tier 3. Each batch lands as its own folder + BOARD.png + script + sync to Windows. Ping sparky when each batch is up for review.
