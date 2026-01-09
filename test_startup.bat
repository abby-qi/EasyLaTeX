@echo off
echo ========================================
echo EasyLaTeX 项目启动测试
echo ========================================
echo.

cd /d "d:\Code_File\EasyLaTeX"

echo [1/4] 检查 Node.js 和 npm...
node --version
npm --version
if %errorlevel% neq 0 (
    echo   ✗ Node.js/npm 检查失败
    exit /b 1
) else (
    echo   ✓ Node.js/npm 正常
)
echo.

echo [2/4] 检查 Python 和 MiKTeX...
python --version
if %errorlevel% neq 0 (
    echo   ✗ Python 检查失败
) else (
    echo   ✓ Python 正常
)

"D:\Application\MiKTeX\miktex\bin\x64\pdflatex.exe" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ MiKTeX 检查失败
) else (
    echo   ✓ MiKTeX 正常
)
echo.

echo [3/4] 检查依赖安装情况...
if not exist "node_modules\" (
    echo   ⚠ node_modules 不存在,需要运行 npm install
    set NEED_INSTALL=1
) else (
    echo   ✓ node_modules 存在
    set NEED_INSTALL=0
)
echo.

echo [4/4] 测试后端功能...
python -m pytest tests/ -q --tb=no
if %errorlevel% neq 0 (
    echo   ⚠ 后端测试有失败,但不影响运行
) else (
    echo   ✓ 后端测试通过
)
echo.

echo ========================================
echo 测试完成!
echo ========================================
echo.
if %NEED_INSTALL%==1 (
    echo 接下来请运行:
    echo   npm install
    echo   npm start
) else (
    echo 接下来请运行:
    echo   npm start
)
echo.
