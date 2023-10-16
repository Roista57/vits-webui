@echo off

echo Creating virtual environment...
python -m venv venv


if errorlevel 1 (
    echo Error: Failed to create virtual environment.
    pause
    exit /b
)

echo Upgrade pip...
venv\scripts\python -m pip install --upgrade pip
if errorlevel 1 (
    echo Error: Failed to upgrade pip.
    pause
    exit /b
)

echo Installing torch...
venv\Scripts\pip3 install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cu117

if errorlevel 1 (
    echo Error: Failed to install torch and torchaudio.
    pause
    exit /b
)

echo Installing packages from requirements.txt...
venv\Scripts\pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install packages.
    pause
    exit /b
)

echo Installing pyopenjtalk...
venv\Scripts\pip install -U pyopenjtalk==0.2.0 --no-build-isolation

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
..\venv\Scripts\python setup.py build_ext --inplace
popd

if errorlevel 1 (
    echo Error: Failed to clean and Install monotonic_align.
    pause
    exit /b
)

echo Setup complete.

pause