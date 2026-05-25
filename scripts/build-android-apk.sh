#!/usr/bin/env bash
# OGRS — build the Android APK and copy to the Windows desktop.
#
# Pulls the upstream Android module, but redirects its Client_Base
# srcDir at our forked /client/src so the APK carries OGRS codegen
# (NPCs, items, scenery) and the wire-format extensions we ship.
#
# One-time setup needed before first run:
#   - openjdk-17 installed (sudo apt install openjdk-17-jdk-headless)
#   - Android SDK at /home/sparky/android-sdk with build-tools;34.0.0
#     and platforms;android-34 packages (already present on this box).
#
# Output: /mnt/c/Users/sparky.AD/Desktop/OGRS-Client.apk

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ANDROID_TREE="$REPO_ROOT/openrsc-upstream/Android_Client"
APK_OUT="$ANDROID_TREE/Open RSC Android Client/build/outputs/apk/debug/openrsc.apk"
DESKTOP_OUT="/mnt/c/Users/sparky.AD/Desktop/OGRS-Client.apk"

if [ ! -f /usr/lib/jvm/java-17-openjdk-amd64/bin/java ]; then
    echo "ERROR: openjdk-17 not installed. Run: sudo apt install -y openjdk-17-jdk-headless" >&2
    exit 1
fi
if [ ! -d /home/sparky/android-sdk ]; then
    echo "ERROR: Android SDK not at /home/sparky/android-sdk" >&2
    exit 1
fi
if [ ! -f "$ANDROID_TREE/local.properties" ]; then
    echo "Writing local.properties..."
    echo "sdk.dir=/home/sparky/android-sdk" > "$ANDROID_TREE/local.properties"
fi

# OGRS — targeted overlays. Bundle ONLY the cache files we've patched
# (sparky 2026-05-21 / extended 2026-05-25). Full-cache bundle previously
# hung the phone on "Unpacking Library", so we ship just these as overlay
# files. CacheUpdater downloads everything from rsc.vet normally, then
# overwrites these with the bundled OGRS versions:
#   Authentic_Landscape.orsc — crypt sector patch + walkable tiles
#   Authentic_Sprites.orsc   — UI icons (slots 3837-3890) + new item sprites
ASSETS_DEST="$ANDROID_TREE/Open RSC Android Client/src/main/assets"
# Clean any prior big bundle.
if [ -d "$ASSETS_DEST/video" ] || [ -d "$ASSETS_DEST/audio" ]; then
    echo "Removing stale bundled cache from Android assets..."
    rm -rf "$ASSETS_DEST/video" "$ASSETS_DEST/audio"
fi
# Bundle landscape + sprites overlay archives.
mkdir -p "$ASSETS_DEST/ogrs-overlay"
for OVERLAY_FILE in Authentic_Landscape.orsc Authentic_Sprites.orsc; do
    SRC="$REPO_ROOT/client/Cache/video/$OVERLAY_FILE"
    if [ -f "$SRC" ]; then
        cp "$SRC" "$ASSETS_DEST/ogrs-overlay/$OVERLAY_FILE"
        echo "  Bundled $OVERLAY_FILE overlay: $(du -sh "$SRC" | cut -f1)"
    else
        echo "  WARN: $SRC not found — overlay skipped"
    fi
done

echo "Building APK (Java 17 + Android SDK 34)..."
cd "$ANDROID_TREE"
chmod +x gradlew
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    ANDROID_HOME=/home/sparky/android-sdk \
    OGRS_CLIENT_SRC="$REPO_ROOT/client/src" \
    ./gradlew --no-daemon --no-configuration-cache assembleDebug

if [ ! -f "$APK_OUT" ]; then
    echo "ERROR: APK output not found at $APK_OUT" >&2
    exit 1
fi

echo "Copying APK to Windows desktop..."
cp "$APK_OUT" "$DESKTOP_OUT"

SIZE=$(stat -c%s "$DESKTOP_OUT")
echo
echo "Done. APK: $DESKTOP_OUT (${SIZE} bytes)"

# --- Auto-publish to GitHub releases for Obtainium auto-update ---
#
# Obtainium on the phone polls https://github.com/JFingle/ogrs/releases
# and pulls the newest release whose asset name matches a configured
# regex. Publishing here means every APK build is available to the
# phone within Obtainium's poll interval (default 15 min).
#
# Skips silently if gh isn't installed or not authenticated, so the
# script still works on a fresh checkout without the publish path.
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    cd "$REPO_ROOT"
    TAG="mobile-$(date +%Y%m%d-%H%M)"
    HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    TITLE="Mobile build $(date +'%Y-%m-%d %H:%M') ($HASH)"
    LAST_COMMIT=$(git log -1 --pretty=%s 2>/dev/null || echo "")
    NOTES="Auto-built OGRS Android client.

Commit: $HASH ($LAST_COMMIT)

Obtainium picks up the OGRS-Client.apk asset attached below — no
manual sideload needed once Obtainium is configured to watch this
repo."
    echo
    echo "Publishing release $TAG..."
    if gh release create "$TAG" "$APK_OUT" --title "$TITLE" --notes "$NOTES" --latest; then
        echo "Release published: https://github.com/JFingle/ogrs/releases/tag/$TAG"
        echo "Obtainium-configured phones will pull it within their poll interval."
    else
        echo "WARN: gh release create failed; APK is still local at $DESKTOP_OUT" >&2
    fi
else
    echo
    echo "(gh not authed -> skipping GitHub release publish; APK is local only.)"
    echo "To enable phone auto-update via Obtainium, run: gh auth login"
fi

echo
echo "Sideload (manual fallback if not using Obtainium):"
echo "  1) Move OGRS-Client.apk to your Android phone"
echo "  2) Enable 'Install unknown apps' for the file manager"
echo "  3) Tap the APK to install"
echo "  4) On first launch the client asks for a server IP — see scripts/setup-windows-portforward.ps1 output"
