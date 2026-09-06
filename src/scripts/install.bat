@echo off
setlocal enabledelayedexpansion

rem ============================================================
rem  EasyLaTeX 一键安装脚本 (Windows)
rem  注意：TinyTeX 必须装到【项目根目录】下的 tinytex\，
rem        因为后端 tex_compiler.py 是按项目根来探测的，
rem        而不是按运行脚本时所在的目录。
rem ============================================================

rem 项目根 = 本脚本所在目录(src\scripts\)的上两级
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
pushd "%PROJECT_ROOT%"
set "PROJECT_ROOT=%CD%"

echo 项目根目录: %PROJECT_ROOT%
echo.

echo [1/4] 正在配置 npm 镜像...
echo registry=https://registry.npmmirror.com> "%PROJECT_ROOT%\.npmrc"
echo strict-ssl=false>> "%PROJECT_ROOT%\.npmrc"

echo.
echo [2/4] 正在安装 Node.js 依赖...
call npm install
if errorlevel 1 (
    echo [警告] npm install 失败，请检查网络或手动执行 npm install
)

echo.
echo [3/4] 正在安装 Python 依赖...
python -m pip install -r "%PROJECT_ROOT%\src\backend\requirements.txt"
if errorlevel 1 (
    echo [警告] Python 依赖安装失败，请检查 Python 是否在 PATH 中
)

echo.
echo [4/4] 正在下载并安装 TinyTeX...
set "TINYTEX_DIR=%PROJECT_ROOT%\tinytex"

if exist "%TINYTEX_DIR%\bin\windows\xelatex.exe" (
    echo TinyTeX 已存在，跳过下载。
    goto :after_tinytex
)

if not exist "%TINYTEX_DIR%" mkdir "%TINYTEX_DIR%"

echo 下载 TinyTeX (约 100MB，请耐心等待)...
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; try { Invoke-WebRequest -Uri 'https://yihui.org/tinytex/TinyTeX-1.zip' -OutFile '%TINYTEX_DIR%\TinyTeX.zip' -UseBasicParsing } catch { Write-Host ('下载失败: ' + $_.Exception.Message); exit 1 }"
if errorlevel 1 (
    echo [警告] TinyTeX 下载失败。你可以：
    echo   1. 手动从 https://yihui.org/tinytex/ 下载并解压到 %TINYTEX_DIR%
    echo   2. 或安装 TeX Live / MiKTeX 并加入 PATH
    goto :after_tinytex
)

echo 解压中...
powershell -NoProfile -Command "Expand-Archive -Path '%TINYTEX_DIR%\TinyTeX.zip' -DestinationPath '%TINYTEX_DIR%' -Force"
del "%TINYTEX_DIR%\TinyTeX.zip" 2>nul

rem 官方压缩包里多一层 .TinyTeX 目录，摊平到 tinytex\ 下
if exist "%TINYTEX_DIR%\.TinyTeX" (
    echo 整理目录结构...
    xcopy "%TINYTEX_DIR%\.TinyTeX\*" "%TINYTEX_DIR%\" /E /Y /Q >nul
    rmdir /S /Q "%TINYTEX_DIR%\.TinyTeX"
)

:after_tinytex

echo.
echo 安装完成！
echo   TinyTeX 路径: %TINYTEX_DIR%
echo.
echo 运行 run.bat 启动应用。
popd
pause
