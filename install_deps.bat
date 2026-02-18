@echo off

rem Check if local Node.js exists
if exist "nodejs\node.exe" (
    echo Using local Node.js...
    set NODE_PATH=nodejs\node.exe
    set NPM_PATH=nodejs\npm.cmd
) else (
    echo Local Node.js not found, using system Node.js...
    set NODE_PATH=node
    set NPM_PATH=npm
)

rem Configure npm mirror
echo Configuring npm mirror...
echo registry=https://registry.npmmirror.com > .npmrc
echo strict-ssl=false >> .npmrc
echo.

rem Install dependencies
echo Installing project dependencies...
%NPM_PATH% install
echo.

rem Check if TinyTeX exists
if not exist "tinytex" (
    echo Warning: TinyTeX directory not found. Please download and place TinyTeX according to PORTABLE_SETUP.md...
    echo.
)

echo Dependencies installed successfully!
pause