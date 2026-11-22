@echo off
rem Puts a Sky Gahshomar icon on the Desktop and in the Start menu that opens the app.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo.
    echo  Please double-click "Start app.bat" first; it installs the app and makes the icon.
    echo.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" tools\launch.py --make-shortcut
echo.
echo  The Sky Gahshomar icon is now on your Desktop and in the Start menu.
echo.
pause
