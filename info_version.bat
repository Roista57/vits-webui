@echo off
echo Checking software and hardware versions...
echo.

:: Python 버전 확인
echo Python:
python --version

:: CMake 버전 확인
echo.
echo CMake:
cmake --version

:: Visual Studio Build Tools 버전 확인
echo.
echo Visual Studio Build Tools:
for /f "usebackq tokens=1* delims=: " %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationVersion`) do (
    echo Version: %%i
)

:: CUDA toolkit 버전 확인. nvcc는 CUDA toolkit과 함께 제공되는 컴파일러입니다.
echo.
echo CUDA Toolkit:
nvcc --version

:: CPU 정보 확인
echo.
echo CPU Information:
wmic cpu get name

:: 그래픽 카드 정보 확인
echo.
echo Graphics Card Information:
wmic path win32_VideoController get name

echo.
pause
