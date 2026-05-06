# Contributing to OGRS

Welcome. OGRS is in the foundation phase — most work is architectural, the content pipeline isn't fully set up yet, and breaking changes happen weekly. If you're reading this, you're early.

## Ground rules

1. **Read [`docs/rsc-contract.md`](docs/rsc-contract.md) first.** It defines what we will and will not change about RSC. Most rejections of PRs come from contract violations. If you want to change a contract item, propose an amendment in a separate PR before the implementation PR.

2. **Additive content is data, not code.** New NPCs, items, zones, quests, skills, spells go in `content/<type>/<name>.yaml`. Code changes to add specific content are PR-rejected by default.

3. **Server-authoritative everything.** No PR adds client-trusted state. Damage, XP, item mutations, position — all server-decided.

4. **AGPL-3.0.** All contributions are AGPLv3. By submitting a PR you license your changes under it.

5. **No Jagex IP.** Don't copy sprite art, names, or text from official RuneScape. Original-IP additions only. Existing world preservation is the upstream OpenRSC baseline; we don't extend that.

## Branching

- `main` — production releases. Tagged. Protected.
- `develop` — integration branch. Feature work merges here. Auto-deploys to staging.
- `feature/<short-name>` — feature branches off `develop`.
- `content/<type>-<name>` — pure content additions (no code), faster review cycle.

## PR checklist

- [ ] Branched off `develop`
- [ ] Schema-validates (CI runs `tools/content-validator/`)
- [ ] If touching contract-Tier-1/2 behavior, amendment exists in `docs/rsc-contract.md`
- [ ] No secrets, no upstream-Jagex assets, no AGPL-incompatible code
- [ ] Tests added or updated where it's a code change
- [ ] CHANGELOG entry under `## Unreleased`

## Content authoring

For NPCs, items, zones, quests, skills, spells: see [`content/README.md`](content/README.md) for the schemas and the validator.

## Getting help

This is a small project. Open a GitHub Discussion or DM in the dev channel.
