# OGRS — Sharded World Architecture

> Status: **design doc, not implemented.** Capturing the framework so we
> don't paint ourselves into a corner while we ship single-world. We'll
> revisit when a single world starts approaching its tick budget.
>
> Owner: sparky. Last touched: 2026-05-25.

## Target

5–10 worlds × ~1000 concurrent each = **5,000–10,000 total capacity.**

The hard ceiling on a single OGRS world is the 640ms single-threaded
game tick. Modern Java OpenRSC realistically sustains 1000–2000
concurrent before tick overrun. To go higher, we run multiple JVM
processes ("worlds") that share a database. This is exactly what
authentic RSC did — they ran ~12 worlds.

## Decisions on the table

| Question | Decision | Why |
|---|---|---|
| Guild membership scope | **Cross-world** | Social cohesion. One identity, one friends list, regardless of which world you log into. |
| Worlds at launch | **Identical** | No themed (PvP-only / hardcore / etc.) variants for v1. Revisit once we have real player data. |
| Launch sequencing | **Single-world soft launch first** | Validates the engine + features under real load before paying for 5–10 boxes. |
| Character model | **One character per world** | Authentic RSC pattern. Avoids needing a "character move between worlds" pipeline that takes seconds and locks the player out mid-transfer. |
| Cross-world chat bridge | **DB-polling outbox** (v1) | No new infrastructure (Redis, MQ). Polling every 1–2s gives chat-acceptable latency. Upgrade path to Redis pub/sub if/when latency matters. |
| Plot scope | **Per-world** | Plots are physical tiles. A plot on World 3 cannot also exist on World 7. |
| Contract scope | **Per-world** | Resource deliveries, mentorship bonds, construction jobs, bounties — all anchor to in-world physical proximity or PvP kills. |

## Topology

```
                          ┌─────────────┐
                          │  Launcher   │   serves cache + website
                          │  box        │   + world-list API
                          └──────┬──────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
       ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
       │  World 1    │    │  World 2    │    │  World N    │
       │  JVM        │    │  JVM        │    │  JVM        │
       │  port 43594 │    │  port 43594 │    │  port 43594 │
       └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                          ┌──────▼──────┐
                          │  Shared DB  │   accounts, friends, PMs,
                          │  (MariaDB)  │   guilds, chat outbox
                          └─────────────┘

                Each world ALSO has its own per-world DB
                for inventory/skills/plots/contracts/etc.
```

Hosting cost at full 10-world buildout: ~$170/mo (Hetzner-class).

## Schema split

### Shared DB (one instance, all worlds connect)

| Table | Owner | Notes |
|---|---|---|
| `players` | upstream | Account auth: username, hash, salt, email, banned flags. Per-player, not per-character. |
| `friends`, `private_messages` | upstream | Friends list works across worlds. PMs route via outbox (see below). |
| `ogrs_guilds`, `ogrs_guild_members`, `ogrs_guild_invites`, `ogrs_guild_bank` | OGRS | Already designed; just move the connection. |
| `ogrs_chat_outbox` *(new)* | OGRS | Cross-world chat fan-out. See "Chat bridge" below. |
| `ogrs_world_status` *(new)* | OGRS | Each world heartbeats here every ~5s: `(world_id, name, online_count, max, last_heartbeat_ms)`. Launcher's world-list API reads from this. |

### Per-world DB (one instance per world)

| Table | Owner | Notes |
|---|---|---|
| All upstream player-state tables | upstream | inventory, bank, skills, equipment, position, fatigue, quest stages. Save key = `(player_id, world_id)`. |
| `ogrs_plots`, `ogrs_plot_bids`, `ogrs_plot_features` | OGRS | Physical tiles → per-world. |
| `ogrs_contracts`, `ogrs_contract_delivery`, `ogrs_contract_*_payouts` | OGRS | All scoped to in-world activity. |

### Character model

One character per `(account, world)` pair. Same login, different
character on each world — like authentic RSC. Players can have a
maxed slayertest on World 1 and a fresh slayertest on World 2.

Skill totals, ironman flag, etc. are per-character (per-world).

Guild membership, friends, PM history are per-account (cross-world).

## Cross-world chat bridge (v1: DB outbox)

```sql
CREATE TABLE ogrs_chat_outbox (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    posted_ms    BIGINT NOT NULL,
    channel_kind TINYINT NOT NULL,        -- 0=guild, 1=PM
    channel_id   INT NOT NULL,            -- guild_id or recipient_player_id
    sender_name  VARCHAR(20) NOT NULL,
    sender_world INT NOT NULL,            -- so we don't re-deliver to the source world
    body         VARCHAR(255) NOT NULL,
    INDEX idx_posted (posted_ms)
);
```

Each world JVM polls every 1–2s (a `ChatBridgeTick` GameTickEvent)
for new rows since its last seen `id`. For each row:

- **channel_kind=0 (guild):** deliver to every locally-online member of
  `channel_id` whose world is NOT `sender_world` (to avoid double-echo
  — the sender's world already showed the message locally).
- **channel_kind=1 (PM):** if the recipient is online on this world,
  deliver and mark recipient's last-read pointer.

Retention sweep on the same tick: delete rows older than 60s.

When/if latency matters more than simplicity, swap the polling for
Redis pub/sub. The application-level interface stays the same.

## Login + world-selection flow

1. Client connects to **any world** (or a dedicated thin login proxy
   running on the launcher box).
2. Sends username + hashed password.
3. Server checks **shared** `players` table.
4. On success: server returns the world list (read from
   `ogrs_world_status`) + a short-lived session token.
5. Client picks a world; renders the chosen world's IP:port from the
   list.
6. Client reconnects directly to chosen world's game port using the
   session token (no re-auth needed).
7. World loads/creates that account's character in its per-world DB.

## Migration from current single-world

The current setup is a single JVM + single DB (`ogrs`). The transition
plan, when sharding becomes worth doing:

1. **Schema cleave** — create `ogrs_shared` database. Move accounts +
   guild tables + friends + PMs into it. Update connection config so
   the existing world reads guild/account state from `ogrs_shared`
   instead of `ogrs`. **Single-world keeps running** through this.
2. **Add world-status heartbeat** — every world writes its
   `ogrs_world_status` row every ~5s. Single-world phase = one row
   in the table.
3. **Build the launcher box** — static-file serve cache + world-list
   API endpoint. Domain + TLS.
4. **Build the chat bridge** — `ogrs_chat_outbox` table +
   `ChatBridgeTick` polling GameTickEvent. With one world, the
   outbox is just a redundant pipe (still works correctly).
5. **Spin up World 2** — new VM, new per-world DB
   (`ogrs_world_2`), same shared DB. Confirm guild chat reaches it,
   plot/contract systems work in isolation.
6. **World 3+** as demand justifies.

Steps 1–4 can ship while single-world is live in production. Steps
5–6 require a maintenance window per world add.

## Non-decisions / TBD

- **Trade across worlds**: explicitly NOT supported (each character is
  per-world).
- **Hiscore aggregation**: per-world for now. Combined "best across all
  worlds" page is a later launcher feature.
- **Wilderness PvP across worlds**: not possible (wilderness is physical
  tiles, can only kill players on the same world).
- **Account suspension propagation**: must be shared-DB-level; banning
  a player blocks them from every world automatically.

## Reading order for the implementer

1. This doc.
2. `project_ogrs_sharding.md` memory (the higher-level "what + why").
3. `OgrsPersistence.java` (the existing in-process persistence layer
   that becomes the per-world layer).
4. `GuildRegistry.java` + `ogrs_guilds*` tables (the first batch that
   moves cross-DB).
