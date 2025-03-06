@echo off
setlocal enabledelayedexpansion

:choose
echo ������ʽ��
echo [1] PyInstaller ���ļ�����
echo [2] Nuitka ���ļ�����(Windows only)
set /p choice=������ѡ�����֣�1/2����

if "%choice%"=="1" (
    echo ����ʹ�� PyInstaller ����...
    ::pyinstaller-build
    pyinstaller --onefile --optimize 2 --hide-console minimize-early -i ark.ico --upx-dir ./upx --uac-admin ark.py
) else if "%choice%"=="2" (
    echo ����ʹ�� Nuitka ����...
    ::nuitka-build
    nuitka ark.py --mingw64 --clang --onefile --standalone --include-data-dir=libs=libs --include-data-dir=src=src --windows-icon-from-ico=ark.ico --show-progress --windows-disable-console --windows-uac-admin --enable-plugin=tk-inter
) else (
    echo ��Чѡ�����������
    timeout /t 2 >nul
    cls
    goto choose
)

echo ������ɣ�
pause