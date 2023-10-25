@echo off
echo Checking software and hardware versions...
echo.

echo Python:
python --version

echo.
echo CMake:
cmake --version

echo.
echo Visual Studio Build Tools:
for /f "usebackq tokens=1* delims=: " %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationVersion`) do (
    echo Version: %%i
)

echo.
echo CUDA Toolkit:
nvcc --version

echo.
echo CPU Information:
wmic cpu get name

echo.
echo Graphics Card Information:
wmic path win32_VideoController get name

echo.
pause
