# Development guide

> Phase 0: this is a living doc. Things will break. Update as you find them.

## Prerequisites

- **JDK 8** — required to build server and client. Temurin/Zulu both work. The Gradle wrapper bundled in `server/` expects 8 specifically; newer JDKs will fail with bytecode errors.
- **Docker + Docker Compose** — for the local MariaDB instance.
- **Python 3.10+** — for the content validator (`pip install pyyaml jsonschema`).
- **Ant** — `client/` builds with Ant (`apt install ant` / `brew install ant`).

## First-time setup

```bash
# 1. Bring up the database.
cd deploy
cp .env.example .env
# Edit .env and set strong passwords.
docker compose up -d
cd ..

# 2. Build the server (first time fetches dependencies).
cd server
./gradlew --no-daemon build -x test

# 3. Build the client.
cd ../client
ant -f build.xml
```

If a step fails, file an issue with the full output — we're still finding upstream-baseline issues.

## Running

### Server

```bash
cd server
./gradlew run -Dconf=ogrs    # runs the OGRS world config (will be created in Phase 0)

# Or temporarily run upstream's preservation config to confirm baseline works:
./gradlew run -Dconf=preservation
```

The `-Dconf=<name>` flag selects a `.conf` file from `server/<name>.conf`. World configs available out of the box:

- `default.conf`         — generic OpenRSC defaults
- `preservation.conf`    — RSC Preservation (closest to authentic 2001 RSC1)
- `2001scape.conf`       — alternate 2001 flavor
- `rsccabbage.conf`      — community fork
- `openpk.conf`          — PvP-focused
- `uranium.conf`         — custom flavor
- `ogrs.conf`            — **our world** (created from `preservation.conf` baseline)

### Client

The client expects to talk to a server on `localhost`. Connection settings live inside
`client/src/orsc/Config.java` and runtime config files. Phase 0 documents this when we
nail down the launcher flow.

## World configuration

OGRS is implemented as **a new OpenRSC world config (`server/ogrs.conf`)**, derived
from `preservation.conf`. We don't fork the engine to add our world — we add a config.

Key OGRS-specific settings (set in `ogrs.conf`):

- `game_tick: 640` — locked per the [contract](rsc-contract.md).
- `enforce_custom_client_version: true` — only OGRS-versioned clients connect.
- `client_version: <unique>` — distinct from upstream so old clients don't accidentally hit our world.
- `db_name: ogrs`
- `server_name: OGRS — Old Gielinor`
- Anti-cheat tunables (`max_connections_per_ip`, `max_packets_per_second`, etc.) tightened from preservation defaults during Phase 2.

## Adding content

### NPCs (current state)

Until the YAML loader lands in Phase 1, custom NPCs are added to:

```
server/conf/server/defs/NpcDefsCustom.json
```

Append to the `"npcs"` array. Use **id 5000+** for OGRS additions. After saving, restart
the server (no hot-reload yet).

The Phase-1 target is one NPC per file under `content/npcs/<name>.yaml`, validated by CI
and loaded automatically. See `content/npcs/example_custom_npc.yaml` for the target shape.

### Items

Same pattern: `server/conf/server/defs/ItemDefsCustom.json`, id 10000+, restart to apply.
YAML migration in Phase 1.

### Quests, skills, zones

These remain hardcoded Java in upstream. Phase 1 refactors them to data. Authoring
guides land alongside each refactor.

## Database migrations

Schema changes go in `server/database/mysql/patches/<YYYY_MM_DD>_<short_name>.sql`.
The patch applier (`server/src/com/openrsc/server/database/patches/JDBCPatchApplier.java`)
runs them at server startup in filename order.

## Content validator

```bash
python tools/content-validator/validate.py
```

CI runs this on every PR. Schema violations block merge.

## Logs

Server logs land in `server/logs/`. The retro/preservation worlds log heavily by default.

## Common issues

- **`Could not find tools.jar`** — JDK 8 not active. Check `java -version` and `JAVA_HOME`.
- **`Connection refused: 3306`** — MariaDB container not up. `docker compose ps` from `deploy/`.
- **`PayloadParser` mismatch on login** — client and server protocol versions disagree. We're targeting **177**; verify your client build matches.
