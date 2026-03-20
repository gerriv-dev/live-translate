@echo off

rmdir /s /q .\build

nuitka main.py --mode=onefile --output-filename=LiveTranslate.exe --output-dir=build --remove-output
