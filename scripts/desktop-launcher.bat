@echo off
REM OGRS — Old Gielinor client launcher.
REM Hands off from the Windows desktop into the WSL2-hosted Java 8 client.
REM The OGRS server runs continuously inside WSL (per the uptime rule);
REM this just opens a client window. WSLg renders the Swing GUI.
REM
REM CANONICAL COPY of the desktop shortcut. The actual file is deployed at
REM   C:\Users\<user>\Desktop\OGRS Client.bat
REM Re-deploy with:  cp /home/sparky/ogrs/scripts/desktop-launcher.bat "/mnt/c/Users/sparky.AD/Desktop/OGRS Client.bat"
REM
REM Earlier version used `start "" wsl.exe bash <path>` which detached the
REM cmd window before WSLg could hook up the display, so the client window
REM never appeared. This version invokes wsl.exe inline (no `start`) with
REM an explicit -d distro flag so the cmd window stays attached for the
REM lifetime of the client and any errors are visible in it.

title OGRS Client
echo Launching OGRS client via WSL...
echo.

REM Explicit distro avoids ambiguity if WSL ever has more than one installed.
wsl.exe -d Ubuntu-24.04 -- /home/sparky/ogrs/scripts/launch-client.sh

REM Stay open on error so the user can read the failure message.
if errorlevel 1 (
    echo.
    echo Client exited with error code %errorlevel%.
    echo Common fixes:
    echo   - Server not running? Re-run the dev server inside WSL.
    echo   - Wrong distro? Check 'wsl --list' and adjust the line above.
    echo   - JAVA_HOME path? Verify /usr/lib/jvm/java-8-openjdk-amd64 exists.
    echo.
    pause
)
