# OGRS UI Art — Things the Engine Side Could Use

> This is the list of UI art that would have immediate value if you authored it. Organized by how easily the engine can integrate them today vs. needing work first.

---

## Ready to wire — immediate value, no engine surgery

These slot into existing rendering paths. Drop the sprite, point the existing render code at the new slot.

- **Skill icons** — current panel uses upstream's tiny sprites. A full skill-icon set, especially **a new Slayer icon** to match the dynamic skill we added. Also nice for any future skills (Languages, etc.). Pattern: drop PNGs, mudclient.java renders them in the skill tab.

- **Tab strip icons** (7-9 tabs: Inv / Map / Skills / Magic / Prayer / Friends / Combat / Options + Android keyboard tab). Today's tabs use upstream art, restyled positionally only. Custom OGRS-branded icons would visually differentiate the fork.

- **Combat tab style icons** — currently `Attack / Defense / Strength / Hits` are text labels. 4 small icons (sword, shield, fist, heart) would read instantly.

- **Run-energy widget icon** — today it's literally rendered as "RUN: 87%" text on a colored box. A boot/feet sprite + numerical overlay would be much better.

---

## Status / HUD widgets — small art, big gameplay clarity

- **Poison status icon** — we just added matron poison and there's NO visual indicator the player is poisoned. A small green skull/drop icon over the HP bar.

- **Slayer task progress widget** — mini-icon (the slayer gem?) + N-remaining counter, persistent in the corner so you don't have to rub the gem every fight.

- **Prayer point bar** — RSC has it but it's text. A glowing-bar widget would match modern dungeon-running expectations.

- **Active-buff icons** — when buffs land (potions, prayers, future masterwork effects) a row of small icons.

---

## Branding / first-impression art

- **Login splash screen** — you already replaced the wolf logo with an OGRS banner in-game; doing a proper login background painting (Lumbridge skyline at dawn, or the crypt entrance, etc.) would make first launch memorable.

- **Dialog box frame** — NPC chat boxes are upstream's stock cream-and-brown. A subtle ornate frame would brand it.

- **Cursor variants** — attack / talk / use / walk cursors (4 icons). Small ask, big polish.

---

## Future-content UI — worth queuing, but needs engine work too

These need an engine subsystem before art helps. Don't author yet — wait until the engine surface exists.

- **Quest log panel** — currently no quest log surface; if we ship one for OGRS quests we need icons + frame.

- **Spellbook category tab icons** — when alternate spellbooks land, each book needs its own header icon (Standard / Ancients / Lunars / Yahwist).

- **Achievement notifications** — when a player hits "first 99 Slayer" or "first crypt clear", a slide-in toast. Needs frame + checkmark icon + sound.

- **Hotbar** — if we expand the autocast picker into a proper N-slot hotbar, needs slot frames + drag-shadow art.

---

## My recommendation, in priority order if cycles are limited

1. **Poison status icon + Slayer task HUD widget** — closes feedback gaps in features we just shipped this week.
2. **Skill icons set including Slayer** — visible every time the player opens the skills tab.
3. **Combat tab style icons** — every combat session.
4. **Tab strip + run-energy icons** — every session.
5. **Login splash + dialog frame** — branding-level, players notice immediately.
6. **Cursor variants** — small ask, high polish-to-effort ratio.

**Skip / defer:** anything that needs a new UI subsystem before art helps (achievement toasts, hotbar). Build the subsystem first; commission art when the wire is in.
