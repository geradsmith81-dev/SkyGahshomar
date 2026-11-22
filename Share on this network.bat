@echo off
rem Shares Sky Gahshomar with phones, tablets and other computers on the same (private) network.
rem A new password is shown each time. Close the window to stop sharing.
title Sky Gahshomar - shared on this network
cd /d "%~dp0"
call "%~dp0Start app.bat" --share
pause
