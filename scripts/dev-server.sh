#!/usr/bin/env bash
# OGRS dev server runner.
#
# Pins JAVA_HOME to JDK 8 (required by upstream OpenRSC) without affecting
# the system default. Other projects (bh-dashboard, etc.) keep their JDK 21.
#
# Usage:
#   ./scripts/dev-server.sh             # boot ogrs world
#   ./scripts/dev-server.sh build       # gradle build only
#   ./scripts/dev-server.sh -Dconf=preservation   # boot upstream preservation world for comparison

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JDK8="/usr/lib/jvm/java-8-openjdk-amd64"

if [[ ! -d "$JDK8" ]]; then
  echo "ERROR: JDK 8 not found at $JDK8" >&2
  echo "Install with: sudo apt install -y openjdk-8-jdk" >&2
  exit 1
fi

# Ensure the database is up.
if ! sudo docker compose -f "$REPO_ROOT/deploy/docker-compose.yml" ps --status running --quiet | grep -q .; then
  echo "[ogrs] Database not running — starting..."
  sudo docker compose -f "$REPO_ROOT/deploy/docker-compose.yml" up -d
  echo "[ogrs] Waiting for MariaDB to become healthy..."
  for _ in {1..30}; do
    status=$(sudo docker inspect --format '{{.State.Health.Status}}' ogrs-mariadb 2>/dev/null || echo none)
    [[ "$status" == "healthy" ]] && break
    sleep 1
  done
fi

cd "$REPO_ROOT/server"

case "${1:-}" in
  build)
    JAVA_HOME="$JDK8" ./gradlew --no-daemon build -x test
    ;;
  test)
    JAVA_HOME="$JDK8" ./gradlew --no-daemon test
    ;;
  "")
    echo "[ogrs] Booting OGRS world (game_tick=640ms, port 43594)..."
    JAVA_HOME="$JDK8" ./gradlew --no-daemon run
    ;;
  *)
    # First arg starts with -P: pass through to gradle.
    # Otherwise treat as world name shortcut: `dev-server.sh preservation` -> `-Pconf=preservation`.
    if [[ "$1" == -P* || "$1" == --* ]]; then
      JAVA_HOME="$JDK8" ./gradlew --no-daemon run "$@"
    else
      JAVA_HOME="$JDK8" ./gradlew --no-daemon run -Pconf="$1"
    fi
    ;;
esac
