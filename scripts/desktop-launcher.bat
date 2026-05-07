@echo off
REM OGRS — Old Gielinor client launcher (debug-friendly).
REM
REM Window stays open after launch, prints every step, and writes a log
REM to %TEMP%\ogrs-client.log so we can diagnose anything that fails.
REM
REM CANONICAL COPY of the desktop shortcut. The actual file is deployed at
REM   C:\Users\<user>\Desktop\OGRS Client.bat
REM Re-deploy with:
REM   cp /home/sparky/ogrs/scripts/desktop-launcher.bat "/mnt/c/Users/sparky.AD/Desktop/OGRS Client.bat"

setlocal
title OGRS Client
set LOG=%TEMP%\ogrs-client.log

echo OGRS — Old Gielinor Client Launcher
echo ====================================
echo.
echo Log: %LOG%
echo Time: %date% %time%
echo. > "%LOG%"
echo OGRS launcher %date% %time% >> "%LOG%"

echo.
echo [1/4] Checking wsl.exe...
where wsl.exe 2>>"%LOG%"
if errorlevel 1 (
    echo   FAIL: wsl.exe not on PATH. Is WSL2 installed?
    echo   FAIL: wsl.exe not on PATH >> "%LOG%"
    goto :end_fail
)
echo   OK.

echo.
echo [2/4] Confirming Ubuntu-24.04 distro is available...
wsl.exe --list --quiet 2>>"%LOG%" | findstr /C:"Ubuntu-24.04" >nul
if errorlevel 1 (
    echo   FAIL: Ubuntu-24.04 distro not found.
    echo   Available distros:
    wsl.exe --list --quiet
    echo   Edit this .bat: change -d Ubuntu-24.04 to your distro name.
    goto :end_fail
)
echo   OK.

echo.
echo [3/4] Confirming launch-client.sh exists in WSL and is executable...
wsl.exe -d Ubuntu-24.04 -- test -x /home/sparky/ogrs/scripts/launch-client.sh
if errorlevel 1 (
    echo   FAIL: /home/sparky/ogrs/scripts/launch-client.sh missing or not chmod +x.
    echo   FAIL: launch-client.sh check >> "%LOG%"
    goto :end_fail
)
echo   OK.

echo.
echo [4/4] Launching client...
echo   (This window will stay open until the client closes.)
echo.
wsl.exe -d Ubuntu-24.04 -- /home/sparky/ogrs/scripts/launch-client.sh
set RC=%errorlevel%
echo.
echo Client exited with code %RC%.
echo Client exited with code %RC%. >> "%LOG%"
goto :end

:end_fail
echo.
echo ===================
echo Launcher could not start the client.
echo Full log: %LOG%
echo ===================

:end
echo.
echo Press any key to close this window.
pause >nul
endlocal
