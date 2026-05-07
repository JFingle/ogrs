#!/usr/bin/env bash
# OGRS — install / refresh the Windows-side launchers on the user's desktop.
#
# Two flavours are deployed because Windows can be picky about which one
# survives SmartScreen / antivirus / shell associations:
#
#   "OGRS Client.lnk"  — a real Windows shortcut pointing directly at
#                         C:\Windows\System32\wsl.exe with the launch args.
#                         Most native option; usually the right click target.
#
#   "OGRS Client.bat"  — debug-friendly batch file that prints each step
#                         and pauses on exit. Use this if the .lnk silently
#                         does nothing — it surfaces what's failing.
#
# Both ultimately invoke ~/ogrs/scripts/launch-client.sh inside WSL2.
# Re-run this script any time those paths change.

set -euo pipefail

DESKTOP="/mnt/c/Users/sparky.AD/Desktop"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "$DESKTOP" ]; then
    echo "ERROR: Windows desktop not found at $DESKTOP" >&2
    echo "Edit this script if your Windows username differs." >&2
    exit 1
fi

echo "Installing OGRS Client.bat..."
cp "$REPO_ROOT/scripts/desktop-launcher.bat" "$DESKTOP/OGRS Client.bat"

echo "Installing OGRS Client.lnk..."
powershell.exe -NoProfile -Command "
\$WshShell = New-Object -ComObject WScript.Shell
\$Shortcut = \$WshShell.CreateShortcut('C:\Users\sparky.AD\Desktop\OGRS Client.lnk')
\$Shortcut.TargetPath = 'C:\Windows\System32\wsl.exe'
\$Shortcut.Arguments = '-d Ubuntu-24.04 -- /home/sparky/ogrs/scripts/launch-client.sh'
\$Shortcut.Description = 'OGRS — Old Gielinor client'
\$Shortcut.WorkingDirectory = 'C:\Users\sparky.AD'
\$Shortcut.Save()
" >/dev/null

echo "Done. Two launchers on the desktop:"
echo "  OGRS Client.lnk  (try first — clean shortcut)"
echo "  OGRS Client.bat  (try second — debug output)"
