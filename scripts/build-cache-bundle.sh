#!/usr/bin/env bash
# OGRS — package the client cache for self-hosted distribution.
#
# rsc.vet currently serves the base cache for every OpenRSC client.
# If it goes down (or we get rate-limited), our players can't install
# or update. This script assembles a self-contained cache directory
# that we can upload to our own launcher box / CDN.
#
# Output layout (mirrors rsc.vet's /downloads/ tree):
#   dist/cache/
#     MD5.SUM           — per-file md5 manifest the CacheUpdater reads
#     video/*.orsc      — sprite + landscape archives
#     video/spritepacks/*
#     audio/*.wav
#
# Deploy step (once we have a domain):
#   1. rsync dist/cache/ <user>@launcher-box:/var/www/ogrs/downloads/
#   2. Update osConfig.DL_URL from "rsc.vet" to our domain
#   3. Bump osConfig.ANDROID_CLIENT_VERSION + rebuild APK
#
# For now: produces the directory locally so we can verify content
# layout before renting infrastructure.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE_SRC="$REPO_ROOT/client/Cache"
DIST_DIR="$REPO_ROOT/dist/cache"

if [ ! -d "$CACHE_SRC" ]; then
    echo "ERROR: cache source $CACHE_SRC missing" >&2
    exit 1
fi

echo "[ogrs] Assembling cache bundle (assets only — local config skipped)..."
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
# Copy ONLY the asset directories. The other files in client/Cache/
# (credentials.txt, uid.dat, ip.txt, etc.) are PER-USER local state and
# must NEVER be distributed — credentials.txt in particular contains
# the developer's last logged-in account.
for dir in video audio; do
    if [ -d "$CACHE_SRC/$dir" ]; then
        cp -r "$CACHE_SRC/$dir" "$DIST_DIR/"
    fi
done
# Drop dev-only backups / scratch files that snuck in via copy.
find "$DIST_DIR" -type f \( -name "*.bak" -o -name "*.crypt-backup" -o -name "*.tmp" \) -delete

echo "[ogrs] Generating MD5.SUM manifest..."
cd "$DIST_DIR"
# Mirror upstream rsc.vet's MD5.SUM format: "<md5>  <relative-path>"
# Skip the manifest itself + dotfiles.
rm -f MD5.SUM
find . -type f ! -name "MD5.SUM" ! -name ".*" -printf "%P\n" | sort | \
    while read -r f; do
        md5=$(md5sum "$f" | awk '{print $1}')
        printf "%s  %s\n" "$md5" "$f"
    done > MD5.SUM

FILE_COUNT=$(wc -l < MD5.SUM)
SIZE_BYTES=$(du -sb "$DIST_DIR" | cut -f1)
SIZE_MB=$((SIZE_BYTES / 1024 / 1024))

echo "[ogrs] Bundle complete:"
echo "  Path:  $DIST_DIR"
echo "  Files: $FILE_COUNT"
echo "  Size:  ${SIZE_MB}MB"
echo
echo "[ogrs] Top-level entries:"
ls -la "$DIST_DIR" | tail -n +2
echo
echo "To deploy when launcher box is ready:"
echo "  rsync -a $DIST_DIR/ <user>@launcher:/var/www/ogrs/downloads/"
echo "Then in openrsc-upstream/Android_Client/.../orsc/osConfig.java:"
echo "  change DL_URL from \"rsc.vet\" to your launcher's hostname"
