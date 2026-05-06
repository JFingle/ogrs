# Upstream pin

We are forking from **OpenRSC Core-Framework**.

- **Source:** https://github.com/Open-RSC/Core-Framework (mirror of https://gitlab.com/open-runescape-classic/core)
- **Pinned commit:** `fc74d38e2ead0a5864b48ae191b7184a391777cf`
- **Pin date:** 2026-04-11
- **Local clone:** `./openrsc-upstream/` (gitignored from our fork once we initialize it)

## License (important)

OpenRSC Core-Framework is **AGPLv3**. This is network copyleft: if we run a public server, we must publish all our modifications under AGPLv3. For a private/personal server this does not trigger.

**Implication:** the "public server eventually" goal means the fork will be public source. Plan accordingly — no proprietary features, no embedded secrets, design as if every commit is going to GitHub.

## Pin policy

We do not chase upstream. New upstream commits are reviewed and cherry-picked only when:
1. They fix a security issue we're affected by, or
2. They fix a bug in code we have not yet replaced.

Once we replace a subsystem (e.g., projectile rendering, content loading), upstream changes to that subsystem are ignored.

## Adjacent OpenRSC repos worth tracking

| Repo | Purpose | Notes |
|---|---|---|
| `rsc-c` | RSC client ported to C | Alternative client base if Java becomes painful |
| `rscplus` | Active RSC client mod platform | Already has resize/UI features — study before reimplementing |
| `RSC-OpenGL-Map-Viewer` | Landscape/model viewer | Reference for our map editor |
| `Custom-Sprite-Collection` | Community sprites | Asset source (verify licensing) |
| `Wiki` | Preservation wiki | Lore source for AI content generation prompts |

## When to re-pin

Plan a re-pin review every ~6 months unless we're stable and have diverged enough that re-pin no longer makes sense.
