@echo off

rem Check if local Node.js exists
if exist "nodejs\node.exe" (
    echo Using local Node.js...
    set NODE_PATH=nodejs\node.exe
) else (
    echo Local Node.js not found, using system Node.js...
    set NODE_PATH=node
)

rem Check if local TinyTeX exists
if not exist "tinytex" (
    echo Warning: Local TinyTeX not found, will use system LaTeX environment if available...
    pause
)

rem Start application
%NODE_PATH% -v
echo Starting EasyLaTeX...
%NODE_PATH% .\node_modules\.bin\electron .
pause