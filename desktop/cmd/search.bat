@echo off

echo Suche nach Mikrofonen...
echo.

for /f "tokens=1,* delims=]" %%a in ('ffmpeg -hide_banner -list_devices true -f dshow -i dummy 2^>^&1 ^| findstr "(audio)"') do (
    echo %%b
)

echo.
echo Suche abgeschlossen.

pause
