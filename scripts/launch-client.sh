#!/usr/bin/env bash
# OGRS — launch the desktop client.
#
# The server is expected to be running already (sparky's "server uptime is
# critical" rule means it shouldn't be restarted from a launcher anyway).
# This script just boots the Swing client jar with the Java 8 the project
# needs.
#
# Invoked from the desktop shortcut(s) — the Windows .bat on the desktop
# calls this via `wsl.exe bash <path>`.

set -e
cd "$(dirname "$0")/../client"
exec env JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 java -jar Open_RSC_Client.jar
