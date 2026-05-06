# OGRS — Old Gielinor

> *Run, you fool.*

An additive extension of RuneScape Classic. New lands, new creatures, new quests, new skills, new spells — same 2001 feel.

**Project name:** OGRS, pronounced "ogres." Officially *Old Gielinor*. Short form has the double meaning we like — *OG* + *RS*.

**Status:** pre-alpha. Foundation phase.

---

## Vision

OGRS is a fork of [OpenRSC Core-Framework](https://github.com/Open-RSC/Core-Framework) that extends the world without changing it. The Gielinor you remember stays the Gielinor you remember — we add to it.

What "additive" means concretely:

- **New lands** appended to the unused regions of the world coordinate space
- **New creatures, NPCs, items, quests** — defined as data, not code
- **New skills** alongside the original 17, never replacing
- **New spells and prayers** with proper visual variety (no more single hardcoded blue orb)
- **Modern UI option** that toggles back to pixel-perfect classic at any time
- **Resizable client window**, with classic 512×334 always available
- **Heavy server-side anti-cheat** — never trust the client

What we will *not* change:
- 2D isometric tile-based world. No 3D.
- Tick-based combat (640ms). No real-time.
- 99 stat caps. No power creep.
- The combat triangle.
- The original Gielinor map and content.

The full set of "do not touch" rules lives in [`docs/rsc-contract.md`](docs/rsc-contract.md). Every change is checked against it.

---

## Repository layout

```
ogrs/
├── server/                # forked OpenRSC server (Java/Gradle)
├── client/                # forked OpenRSC Client_Base (Java)
├── content/               # additive content as data — NPCs, items, zones, quests, skills
├── tools/                 # editors, validators, importers
├── deploy/                # docker-compose stacks for dev / staging / prod
├── docs/                  # design docs and developer guides
├── .github/workflows/     # CI
├── UPSTREAM.md            # upstream pin + license note + adjacent repos
├── LICENSE                # AGPL-3.0
└── README.md
```

The `openrsc-upstream/` directory at the project root (gitignored) is a read-only reference clone of upstream. We do not edit it.

---

## License

OGRS is **AGPL-3.0**, inheriting from upstream OpenRSC. Network deployment requires source publication. We embrace this — the project is open source from day one.

If you operate a public OGRS server, you must publish your modifications. See [`LICENSE`](LICENSE) and [`UPSTREAM.md`](UPSTREAM.md).

---

## Quick start (local dev)

> Coming online during Phase 0. Until the dev compose stack lands, see [`docs/development.md`](docs/development.md) for the current state.

```bash
# Future state:
cd deploy
docker compose --profile dev up
```

---

## Status & roadmap

Phase 0 — **Foundation** *(active)*
- [x] Pin upstream commit
- [x] Draft `rsc-contract.md`
- [x] Fork `server/` and `client/` into project
- [ ] Project repo on GitHub, public, AGPLv3
- [ ] CI: build, test, lint, schema-validate content
- [ ] Local docker-compose dev stack with hot-reload where possible
- [ ] First custom NPC end-to-end via `content/npcs/`

Phase 1 — **Content pipeline**
- [ ] Migrate NPC/item defs to schema-validated YAML in `content/`
- [ ] Refactor skills to data-driven
- [ ] Refactor quests to data-driven
- [ ] OSRS quest import pipeline
- [ ] Parallel JSON map system + first new zone

Phase 2 — **Anti-cheat hardening** *(parallel, ongoing)*

Phase 3 — **Client modernization** *(resizable + modern UI toggle)*

Phase 4 — **Projectile system** *(replace the hardcoded orbs)*

Phase 5 — **Combat overhaul** *(pluggable formulas, status effects, spell schools)*

Phase 6 — **Content tooling** *(map painter, NPC editor, AI-assisted authoring)*

Detail in [`docs/`](docs/).

---

## Credits

- **OpenRSC Core-Framework** by the [Open-RSC](https://github.com/Open-RSC) preservation community — the base we're building on.
- **RSC Wiki** — lore source.
- All upstream contributors named in `openrsc-upstream/CONTRIBUTING.md`.

OGRS is a fan project. Not affiliated with Jagex Ltd. *RuneScape* is a trademark of Jagex Ltd; *RuneScape Classic* was retired in 2018. We claim no rights to Jagex IP and replace original assets where we can.
