@echo off

pyinstaller --onefile --optimize 2 --upx-dir ./upx/win/ --hide-console minimize-early -i ark.ico --disable-windowed-traceback ark.py
