@echo off
echo Checking Node.js installation...
echo.

echo 1. Checking C:\Program Files\nodejs...
if exist "C:\Program Files\nodejs\node.exe" (
    echo   Found! Testing...
    "C:\Program Files\nodejs\node.exe" --version
    "C:\Program Files\nodejs\npm.cmd" --version
) else (
    echo   Not found
)

echo.
echo 2. Checking C:\Program Files (x86)\nodejs...
if exist "C:\Program Files (x86)\nodejs\node.exe" (
    echo   Found! Testing...
    "C:\Program Files (x86)\nodejs\node.exe" --version
    "C:\Program Files (x86)\nodejs\npm.cmd" --version
) else (
    echo   Not found
)

echo.
echo 3. Current PATH:
echo %PATH%
