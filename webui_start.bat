@echo off

echo Running vits-webui...
venv\Scripts\python webui-vits.py

if errorlevel 1 (
    echo Error: Failed to run vits-webui.
    pause
    exit /b
)

pause