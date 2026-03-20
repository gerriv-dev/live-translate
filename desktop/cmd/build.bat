@echo off

echo Building Live-Translate Desktop...
echo.

nuitka main.py --mode=onefile --output-filename=LiveTranslate.exe --remove-output

echo Build finished.
echo.
