@echo off
chcp 65001 >nul
echo ========================================
echo   HumanLapse - 打包为 EXE
echo ========================================
echo.

REM 检查是否安装了 PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 PyInstaller
    echo.
    echo 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo [错误] 安装失败，请手动执行：
        echo   pip install pyinstaller
        pause
        exit /b 1
    )
)

echo [信息] 开始打包...
echo.

REM 打包为单个 EXE 文件
pyinstaller --onefile ^
    --name "HumanLapse" ^
    --console ^
    --add-data "speed_controller.py;." ^
    --noconfirm ^
    speed_controller_drag.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   打包失败！
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 输出位置：dist\HumanLapse.exe
echo.
echo 使用方法：
echo   1. 拖动视频文件到 HumanLapse.exe
echo   2. 拖动文件夹到 HumanLapse.exe
echo.
echo 注意：用户仍需安装 FFmpeg 并添加到 PATH
echo.
pause

