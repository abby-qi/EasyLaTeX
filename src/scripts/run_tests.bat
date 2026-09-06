@echo off
echo Running all tests...
echo.

cd /d "d:\Code_File\EasyLaTeX"

echo ========================================
echo Running all tests in tests/ directory
echo ========================================
python -m pytest tests/ -v --tb=short

echo.
echo ========================================
echo Test complete!
echo ========================================
