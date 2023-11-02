@echo off
echo This script automates the installation of Miniconda.

set DOWNLOAD_DIR=%cd%

set MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

set INSTALLER_NAME=miniconda_installer.exe

powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%MINICONDA_URL%', '%DOWNLOAD_DIR%\%INSTALLER_NAME%')"

"%DOWNLOAD_DIR%\%INSTALLER_NAME%" /S /InstallationType=JustMe /AddToPath=1 /RegisterPython=1

echo Installation is complete!

echo Creating Miniconda environment...
call conda env list | findstr "venv"
if not errorlevel 1 (
    echo Removing existing 'venv' environment...
    call conda env remove --name venv -y
    if errorlevel 1 (
        echo Error: Failed to remove existing 'venv' environment.
        pause
        exit /b
    )
)

echo Creating a new 'venv' environment in the current directory...
call conda create --prefix "%cd%\venv" python=3.8 -y


if errorlevel 1 (
    echo Error: Failed to create Miniconda environment.
    pause
    exit /b
)

echo Activating Miniconda environment...
call conda activate "%cd%\venv"

if errorlevel 1 (
    echo Error: Failed to activate Miniconda environment.
    pause
    exit /b
)

echo Installing torch...
pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cu117

if errorlevel 1 (
    echo Error: Failed to install torch and torchaudio.
    pause
    exit /b
)

echo Installing packages from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install packages.
    pause
    exit /b
)

echo Installing ffmpeg...
call conda install -c conda-forge ffmpeg -y

if errorlevel 1 (
    echo Error: Failed to install ffmpeg.
    pause
    exit /b
)

echo Installing pyopenjtalk...
pip install -U pyopenjtalk==0.2.0 --no-build-isolation

if errorlevel 1 (
    echo Error: Failed to install pyopenjtalk.
    pause
    exit /b
)

echo Installing monotonic_align...
pushd monotonic_align
for %%i in (*.*) do if not "%%~nxi"=="__init__.py" if not "%%~nxi"=="core.pyx" if not "%%~nxi"=="setup.py" del /f /q "%%i"
for /D %%i in (*) do rmdir /s /q "%%i"
mkdir monotonic_align
python setup.py build_ext --inplace
popd

if errorlevel 1 (
    echo Error: Failed to clean and Install monotonic_align.
    pause
    exit /b
)

echo Setup complete.

pause