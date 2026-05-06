@echo off
chcp 65001 >nul
echo ========================================
echo   HumanLapse - Build EXE
echo ========================================
echo.

REM Check PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller not found
    echo.
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo [ERROR] Install failed. Please run:
        echo   pip install pyinstaller
        pause
        exit /b 1
    )
)

echo [INFO] Start building...
echo.

call :build_exe HumanLapse_30s
if errorlevel 1 goto :build_failed

call :build_exe HumanLapse_60s
if errorlevel 1 goto :build_failed

call :copy_ffmpeg_binaries
if errorlevel 1 goto :build_failed

echo.
echo ========================================
echo   Build complete!
echo ========================================
echo(
echo(Output files:
echo(  dist\HumanLapse_30s.exe
echo(  dist\HumanLapse_60s.exe
echo(  dist\ffmpeg.exe
echo(  dist\ffprobe.exe
echo(
echo(Usage:
echo(  1. Keep EXE, ffmpeg.exe and ffprobe.exe together
echo(  2. Drag a video file onto the target EXE
echo(  3. Drag a folder onto the target EXE
echo(
echo(Notes:
echo(  - HumanLapse_30s.exe outputs 30-second videos
echo(  - HumanLapse_60s.exe outputs 60-second videos
echo(  - FFmpeg is included in this release package
echo(
pause
exit /b 0

:build_exe
echo [INFO] Building %~1.exe ...
pyinstaller --onefile ^
    --name "%~1" ^
    --console ^
    --add-data "speed_controller.py;." ^
    --noconfirm ^
    speed_controller_drag.py
if errorlevel 1 exit /b 1
echo [INFO] %~1.exe built successfully
echo.
exit /b 0

:copy_ffmpeg_binaries
echo [INFO] Copying FFmpeg binaries...
if not exist "ffmpeg.exe" (
    echo [ERROR] Missing ffmpeg.exe in project root
    exit /b 1
)
if not exist "ffprobe.exe" (
    echo [ERROR] Missing ffprobe.exe in project root
    exit /b 1
)
copy /Y "ffmpeg.exe" "dist\ffmpeg.exe" >nul
if errorlevel 1 exit /b 1
copy /Y "ffprobe.exe" "dist\ffprobe.exe" >nul
if errorlevel 1 exit /b 1
echo [INFO] FFmpeg binaries copied
echo.
exit /b 0

:build_failed
echo.
echo ========================================
echo   Build failed!
echo ========================================
pause
exit /b 1
