@echo off

pyinstaller --onefile --optimize 2 --upx-dir ./upx/win/ --hide-console minimize-early -i ark.ico --uac-admin --disable-windowed-traceback ark.py

pause