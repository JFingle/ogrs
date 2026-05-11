#!/usr/bin/env bash
# OGRS — install / refresh the DuckDNS user-crontab entry.
#
# Runs duckdns-update.sh every 5 minutes from sparky's crontab. Idempotent:
# replaces any prior OGRS DuckDNS entry without touching other crontab
# lines. Run once after editing duckdns.conf.

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
UPDATE_SCRIPT="$DIR/duckdns-update.sh"
TAG="# OGRS DuckDNS auto-update — managed by duckdns-install.sh"

if [ ! -f "$DIR/duckdns.conf" ]; then
    echo "ERROR: $DIR/duckdns.conf missing." >&2
    echo "       Copy duckdns.conf.example to duckdns.conf and fill in values first." >&2
    exit 2
fi

chmod +x "$UPDATE_SCRIPT"

# Sanity-check the config + token now so we fail loud here rather than
# silently in cron.
echo "Running an initial update so we know the token works..."
if ! "$UPDATE_SCRIPT"; then
    echo "ERROR: initial DuckDNS update failed. Check log/update.log." >&2
    exit 3
fi
echo "Initial update succeeded."

# Strip any prior OGRS DuckDNS lines, append the fresh one.
CURRENT=$(crontab -l 2>/dev/null || true)
FILTERED=$(printf "%s\n" "$CURRENT" | awk -v tag="$TAG" '
    BEGIN { skip = 0 }
    /^# OGRS DuckDNS auto-update/ { skip = 1; next }
    skip && /duckdns-update.sh/ { skip = 0; next }
    { print }
')

NEW_ENTRY="$TAG
*/5 * * * * $UPDATE_SCRIPT >/dev/null 2>&1"

{
    if [ -n "$FILTERED" ]; then printf "%s\n" "$FILTERED"; fi
    printf "%s\n" "$NEW_ENTRY"
} | crontab -

echo
echo "Installed crontab entry. Verify with: crontab -l"
echo "Updater runs every 5 min and logs to: $DIR/log/update.log"
