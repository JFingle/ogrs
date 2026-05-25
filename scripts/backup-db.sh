#!/usr/bin/env bash
# OGRS — daily MariaDB backup.
#
# Dumps every database from the ogrs-mariadb container to a gzipped
# .sql.gz file. Keeps the last 14 days; older dumps are deleted.
#
# Intended schedule: nightly via cron or systemd timer. Examples below.
#
# Restore (test before relying on this):
#   gunzip < /var/backups/ogrs/ogrs-YYYY-MM-DD.sql.gz \
#     | docker exec -i ogrs-mariadb mariadb -uroot -p<root-pass>
#
# Cron entry (add via `crontab -e`):
#   15 3 * * *  /home/sparky/ogrs/scripts/backup-db.sh >> /var/log/ogrs-backup.log 2>&1
#
# Systemd timer alternative — write two unit files to /etc/systemd/system/:
#   ogrs-backup.service:
#     [Service]
#     Type=oneshot
#     ExecStart=/home/sparky/ogrs/scripts/backup-db.sh
#   ogrs-backup.timer:
#     [Timer]
#     OnCalendar=*-*-* 03:15:00
#     Persistent=true
#     [Install]
#     WantedBy=timers.target

set -euo pipefail

BACKUP_DIR="${OGRS_BACKUP_DIR:-/var/backups/ogrs}"
RETENTION_DAYS="${OGRS_BACKUP_RETENTION:-14}"
CONTAINER="${OGRS_DB_CONTAINER:-ogrs-mariadb}"

# Root credentials are baked into the container env. Read them straight
# from there rather than duplicating in a script — same source of truth.
ROOT_PASS=$(sudo docker exec "$CONTAINER" sh -c 'echo "$MARIADB_ROOT_PASSWORD"' 2>/dev/null || true)
if [ -z "$ROOT_PASS" ]; then
    echo "ERROR: couldn't read MARIADB_ROOT_PASSWORD from container $CONTAINER" >&2
    exit 1
fi

sudo mkdir -p "$BACKUP_DIR"
sudo chown "$USER":"$USER" "$BACKUP_DIR"

STAMP=$(date +%Y-%m-%d_%H%M)
OUT="$BACKUP_DIR/ogrs-$STAMP.sql.gz"

echo "[ogrs-backup] Starting dump -> $OUT"
sudo docker exec "$CONTAINER" mariadb-dump -uroot -p"$ROOT_PASS" \
    --all-databases --single-transaction --quick --routines --triggers \
    --events --add-drop-database 2>/dev/null \
    | gzip -9 > "$OUT"

SIZE_HUMAN=$(du -h "$OUT" | cut -f1)
echo "[ogrs-backup] Dump complete: $OUT ($SIZE_HUMAN)"

# Verify the dump isn't empty / truncated. A failed mariadb-dump still
# produces an output file because we redirected through gzip — guard
# against that by checking the gzip is valid and large enough to be
# real.
if ! gzip -t "$OUT" 2>/dev/null; then
    echo "[ogrs-backup] ERROR: dump is not a valid gzip — keeping for inspection" >&2
    exit 2
fi
BYTES=$(stat -c%s "$OUT")
if [ "$BYTES" -lt 1024 ]; then
    echo "[ogrs-backup] ERROR: dump is suspiciously small ($BYTES bytes) — keeping for inspection" >&2
    exit 3
fi

# Retention sweep — drop dumps older than RETENTION_DAYS.
DELETED=$(find "$BACKUP_DIR" -maxdepth 1 -name "ogrs-*.sql.gz" -type f -mtime "+$RETENTION_DAYS" -print -delete | wc -l)
if [ "$DELETED" -gt 0 ]; then
    echo "[ogrs-backup] Retention sweep: deleted $DELETED dump(s) older than $RETENTION_DAYS days"
fi

# Summary of what we have on disk now.
TOTAL=$(find "$BACKUP_DIR" -maxdepth 1 -name "ogrs-*.sql.gz" | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
echo "[ogrs-backup] Backups on disk: $TOTAL files, $TOTAL_SIZE total"
