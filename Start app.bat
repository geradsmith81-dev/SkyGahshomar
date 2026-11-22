@echo off
setlocal
title Sky Gahshomar
cd /d "%~dp0"
set "MODE=%~1"

rem ---- is the app's private Python environment present and up to date? ----
set "NEEDSETUP="
if not exist ".venv\Scripts\pythonw.exe" set "NEEDSETUP=1"
if not defined NEEDSETUP ( fc /b "requirements.txt" ".venv\installed-requirements.txt" >nul 2>nul || set "NEEDSETUP=1" )

if defined NEEDSETUP (
    if /i "%MODE%"=="--setup" goto :setup
    if /i "%MODE%"=="--share" goto :setup
    rem The Desktop icon starts this window minimised, so run the setup in a window that can be seen.
    echo  Sky Gahshomar is installing or updating its components in a separate window...
    start "Sky Gahshomar setup" /wait cmd /c ""%~f0" --setup"
    fc /b "requirements.txt" ".venv\installed-requirements.txt" >nul 2>nul || exit /b 1
)
goto :launch

:setup
rem ---- find Python 3.12 or newer (only needed to create the private environment) ----
set "PY="
if exist ".venv\Scripts\python.exe" goto :havepy
for %%V in (3.15 3.14 3.13 3.12) do if not defined PY ( py -%%V -c "import sys" >nul 2>nul && set "PY=py -%%V" )
if not defined PY ( py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>nul && set "PY=py -3" )
rem the Windows "python" placeholder only opens the Microsoft Store, so check that Python really runs
if not defined PY ( python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>nul && set "PY=python" )
if not defined PY (
    py -3 -c "import sys" >nul 2>nul && goto :oldpython
    python -c "import sys" >nul 2>nul && goto :oldpython
    goto :nopython
)
:havepy

echo.
echo  Installing Sky Gahshomar's components (tested versions, each checked against its published
echo  checksum). This needs an internet connection and takes about 2 to 5 minutes. Please wait...
echo.
if not exist ".venv\Scripts\python.exe" ( %PY% -m venv .venv || goto :fail )
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check --no-input --require-hashes --only-binary ":all:" -r requirements.txt || goto :fail
copy /y "requirements.txt" ".venv\installed-requirements.txt" >nul
echo.
echo  Setup finished.
rem ---- put a Sky Gahshomar icon on the Desktop and in the Start menu ----
".venv\Scripts\python.exe" tools\launch.py --make-shortcut >nul 2>nul && echo  A Sky Gahshomar icon has been put on your Desktop and in the Start menu.
if /i "%MODE%"=="--setup" exit /b 0

:launch
if /i "%MODE%"=="--setup" exit /b 0
if /i "%MODE%"=="--share" (
    ".venv\Scripts\python.exe" tools\launch.py --share
    exit /b 0
)
rem ---- start the app without a console window; it opens in its own window ----
start "" ".venv\Scripts\pythonw.exe" tools\launch.py
exit /b 0

:nopython
echo.
echo  Python was not found on this computer.
echo  Please install it from https://www.python.org/downloads/
echo  and tick "Add python.exe to PATH" on the first installer screen.
echo.
pause
exit /b 1

:oldpython
echo.
echo  This computer's Python is older than 3.12. Sky Gahshomar needs Python 3.12 or newer
echo  (it is tested with 3.15). Please install a current Python from https://www.python.org/downloads/
echo.
pause
exit /b 1

:fail
echo.
echo  Setup did not complete. Check your internet connection, then double-click
echo  "Start app.bat" again.
echo  If the message above says "no matching distribution" or "could not find a version",
echo  this computer's Python is newer than the versions Sky Gahshomar was tested with: install
echo  Python 3.15 from https://www.python.org/downloads/ and try again.
echo  If it says "hashes do not match", a download was damaged or altered; try again later.
echo.
if exist ".venv" rmdir /s /q ".venv"
pause
exit /b 1
