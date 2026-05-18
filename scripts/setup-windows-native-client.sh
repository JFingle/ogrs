#!/usr/bin/env bash
# OGRS — set up the Windows-native client at C:\OGRS\.
#
# Why native instead of WSLg: the WSL launcher chain (wsl.exe → bash →
# launch-client.sh → WSLg display) has too many failure points
# (UTF-16 vs UTF-8 in cmd, Windows username drift, WSLg session staleness)
# and most importantly, it loops back through 4 process boundaries just
# to render a Swing window on a screen that Windows already owns.
#
# This script reproduces today's manual setup:
#
#   1. Creates C:\OGRS\
#   2. Downloads Eclipse Temurin JDK 8 (OpenRSC's target version) zip,
#      extracts to C:\OGRS\jdk-8\, deletes the zip
#   3. Copies the prebuilt jar from client/ to C:\OGRS\
#   4. Copies the client Cache/ tree from client/ to C:\OGRS\Cache\
#      (the client cannot start without library.orsc et al)
#   5. Writes C:\OGRS\OGRS Client.bat with absolute paths
#   6. Deploys a copy of the .bat to the user's Windows Desktop
#
# Idempotent: re-running skips the download if jdk-8/ already exists.
# Use --reinstall to force a fresh download.
#
# Server must be running separately in WSL (see scripts/dev-server.sh).
# The client connects to localhost:43594; WSL2 forwards localhost
# transparently between Windows and the WSL distro.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OGRS_WIN_ROOT="/mnt/c/OGRS"
JDK_URL="https://api.adoptium.net/v3/binary/latest/8/ga/windows/x64/jdk/hotspot/normal/eclipse?project=jdk"

REINSTALL=0
DESKTOP_OVERRIDE=""
for arg in "$@"; do
  case "$arg" in
    --reinstall) REINSTALL=1 ;;
    --desktop=*) DESKTOP_OVERRIDE="${arg#--desktop=}" ;;
    -h|--help)
      sed -n '2,30p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

# 0. Sanity: are we inside WSL with /mnt/c reachable?
if [[ ! -d /mnt/c ]]; then
  echo "ERROR: /mnt/c not found — is this WSL with default drive mounting?" >&2
  exit 1
fi

# 1. C:\OGRS\ root
mkdir -p "$OGRS_WIN_ROOT"
echo "[ogrs] Working in $OGRS_WIN_ROOT"

# 2. JDK 8 (Temurin)
if [[ "$REINSTALL" -eq 1 ]]; then
  rm -rf "$OGRS_WIN_ROOT/jdk-8"
fi
if [[ ! -x "$OGRS_WIN_ROOT/jdk-8/bin/javaw.exe" ]]; then
  echo "[ogrs] Downloading Temurin JDK 8 (~100MB)..."
  curl -fL --progress-bar -o "$OGRS_WIN_ROOT/temurin-8.zip" "$JDK_URL"
  echo "[ogrs] Extracting..."
  (cd "$OGRS_WIN_ROOT" && unzip -q temurin-8.zip)
  # The zip extracts to jdk8uXXXX-bXX — rename to a stable jdk-8 path
  EXTRACTED="$(find "$OGRS_WIN_ROOT" -maxdepth 1 -type d -name 'jdk8u*' | head -1)"
  if [[ -z "$EXTRACTED" ]]; then
    echo "ERROR: extracted JDK dir not found under $OGRS_WIN_ROOT" >&2
    exit 1
  fi
  mv "$EXTRACTED" "$OGRS_WIN_ROOT/jdk-8"
  rm -f "$OGRS_WIN_ROOT/temurin-8.zip"
  echo "[ogrs] JDK 8 installed at $OGRS_WIN_ROOT/jdk-8"
else
  echo "[ogrs] jdk-8/ already present — skipping download (use --reinstall to force)"
fi

# 3. Client jar
if [[ ! -f "$REPO_ROOT/client/Open_RSC_Client.jar" ]]; then
  echo "ERROR: client/Open_RSC_Client.jar missing — build the client first (ant compile in client/)." >&2
  exit 1
fi
cp "$REPO_ROOT/client/Open_RSC_Client.jar" "$OGRS_WIN_ROOT/Open_RSC_Client.jar"
echo "[ogrs] Copied Open_RSC_Client.jar ($(stat -c%s "$OGRS_WIN_ROOT/Open_RSC_Client.jar") bytes)"

# 4. Cache assets (required at boot: library.orsc, models.orsc, sprites, etc)
# Don't wipe an existing Cache/ — it holds credentials.txt, uid.dat, server
# IP/port for resume-on-login. Only seed if missing or on --reinstall.
if [[ ! -d "$REPO_ROOT/client/Cache" ]]; then
  echo "ERROR: client/Cache/ missing — has the client ever been run?" >&2
  exit 1
fi
if [[ "$REINSTALL" -eq 1 || ! -d "$OGRS_WIN_ROOT/Cache" ]]; then
  rm -rf "$OGRS_WIN_ROOT/Cache"
  cp -r "$REPO_ROOT/client/Cache" "$OGRS_WIN_ROOT/Cache"
  echo "[ogrs] Seeded Cache/ ($(du -sh "$OGRS_WIN_ROOT/Cache" | cut -f1))"
else
  echo "[ogrs] Cache/ already present — preserving user state (uid/credentials)"
fi

# 5. Launcher .bat
cat > "$OGRS_WIN_ROOT/OGRS Client.bat" <<'BAT'
@echo off
REM OGRS — Windows-native client launcher.
REM
REM Runs Open_RSC_Client.jar via bundled JDK 8 — no WSL, no WSLg.
REM Server must already be running (in WSL on localhost:43594).

setlocal
cd /d C:\OGRS
start "" "C:\OGRS\jdk-8\bin\javaw.exe" -jar "C:\OGRS\Open_RSC_Client.jar"
endlocal
BAT
echo "[ogrs] Wrote launcher: $OGRS_WIN_ROOT/OGRS Client.bat"

# 6. Deploy to Windows desktop
if [[ -n "$DESKTOP_OVERRIDE" ]]; then
  DESKTOP="$DESKTOP_OVERRIDE"
else
  # Heuristic: pick the most lived-in real user Desktop (largest cumulative
  # byte size of contents), skipping Windows built-in profiles and the
  # $-prefixed proxy profile stubs. Size beats mtime — running this script
  # touches the chosen Desktop, so mtime gets misleading after first run.
  # On domain-joined machines there can be both C:\Users\sparky and
  # C:\Users\sparky.AD — the active one has all the real files.
  DESKTOP=""
  best_size=0
  for d in /mnt/c/Users/*/Desktop; do
    [[ -d "$d" ]] || continue
    name="$(basename "$(dirname "$d")")"
    case "$name" in
      Public|Default|"Default User"|"All Users") continue ;;
      \$*) continue ;;
    esac
    size="$(du -sb "$d" 2>/dev/null | awk '{print $1}')"
    size="${size:-0}"
    if (( size > best_size )); then
      best_size="$size"
      DESKTOP="$d"
    fi
  done
fi

if [[ -z "$DESKTOP" || ! -d "$DESKTOP" ]]; then
  echo "[ogrs] Could not auto-detect Windows desktop. Skipping desktop deploy."
  echo "       Pass --desktop=/mnt/c/Users/<you>/Desktop to deploy."
else
  cp "$OGRS_WIN_ROOT/OGRS Client.bat" "$DESKTOP/OGRS Client.bat"
  echo "[ogrs] Deployed launcher to $DESKTOP/OGRS Client.bat"
fi

echo
echo "Done. Server must be running (scripts/dev-server.sh) for the client"
echo "to connect to localhost:43594. Double-click the desktop launcher to"
echo "play."
