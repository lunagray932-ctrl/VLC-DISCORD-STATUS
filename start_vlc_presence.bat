@echo off
REM VLC Discord Rich Presence - Startup Script
REM This script starts the VLC Discord Rich Presence application

cd /d "d:\GULP"

REM Start the Python script in a minimized window
start /min "VLC Discord Presence" python vlc_discord_presence.py

REM Alternative: Start with visible console for debugging
REM Uncomment the line below and comment the line above if you want to see the console
REM start "VLC Discord Presence" python vlc_discord_presence.py

exit
