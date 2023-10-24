@echo off

echo Activating Miniconda environment...
call conda activate "%cd%\venv"

echo Running vits-webui...
python webui-vits.py

if errorlevel 1 (
    echo Error: Failed to run vits-webui.
    pause
    exit /b
)

pause