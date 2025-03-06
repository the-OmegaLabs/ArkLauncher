@echo off
setlocal enabledelayedexpansion

:choose
echo 构建方式：
echo [1] PyInstaller 单文件构建
echo [2] Nuitka 单文件构建(Windows only)
set /p choice=请输入选项数字（1/2）：

if "%choice%"=="1" (
    echo 正在使用 PyInstaller 构建...
    ::pyinstaller-build
    pyinstaller --onefile --optimize 2 --hide-console minimize-early -i ark.ico --upx-dir ./upx --uac-admin ark.py
) else if "%choice%"=="2" (
    echo 正在使用 Nuitka 构建...
    ::nuitka-build
    nuitka ark.py --onefile --standalone --include -data-dir=libs=libs --include-data-dir=src=src --windows-icon-from-ico=ark.ico --show-progress --windows-disable-console --windows-uac-admin
) else (
    echo 无效选项，请重新输入
    timeout /t 2 >nul
    cls
    goto choose
)

echo 构建完成！
pause
>>>>>>> Stashed changes
