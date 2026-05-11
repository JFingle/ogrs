#!/usr/bin/env bash
# OGRS — DuckDNS auto-update for the home server's public IP.
#
# Reads token + subdomain from duckdns.conf (gitignored), calls
# DuckDNS's update endpoint with ip= empty so they auto-detect our
# public IP from the request. Logs result and exit code; cron pipes
# the output into a rotating log.
#
# Set up via duckdns-install.sh — installs a user crontab entry that
# runs this every 5 minutes.

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
CONF="$DIR/duckdns.conf"
LOG="$DIR/log/update.log"

if [ ! -f "$CONF" ]; then
    echo "$(date -Iseconds) ERROR no config at $CONF — copy duckdns.conf.example to duckdns.conf and fill in" >&2
    exit 2
fi

# Source the config — expects DUCKDNS_DOMAINS and DUCKDNS_TOKEN.
# shellcheck disable=SC1090
. "$CONF"

if [ -z "${DUCKDNS_DOMAINS:-}" ] || [ -z "${DUCKDNS_TOKEN:-}" ]; then
    echo "$(date -Iseconds) ERROR DUCKDNS_DOMAINS or DUCKDNS_TOKEN missing in $CONF" >&2
    exit 3
fi

# Empty ip= lets DuckDNS auto-detect from the request source — works
# whether you're on IPv4 or v6, and survives ISP IP changes without us
# having to discover them ourselves.
RESPONSE=$(curl -s --max-time 10 \
    "https://www.duckdns.org/update?domains=${DUCKDNS_DOMAINS}&token=${DUCKDNS_TOKEN}&ip=")

STAMP=$(date -Iseconds)
if [ "$RESPONSE" = "OK" ]; then
    echo "$STAMP OK ${DUCKDNS_DOMAINS}" >> "$LOG"
elif [ "$RESPONSE" = "KO" ]; then
    echo "$STAMP KO ${DUCKDNS_DOMAINS} — DuckDNS rejected: check token + domain" >> "$LOG"
    exit 1
else
    echo "$STAMP UNEXPECTED ${DUCKDNS_DOMAINS} response='$RESPONSE'" >> "$LOG"
    exit 1
fi
