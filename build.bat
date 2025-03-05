@echo off

pyinstaller --onefile --optimize 2 --upx-dir ./upx --hide-console minimize-early -i ark.ico --uac-admin ark.py