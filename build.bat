@echo off

pyinstaller --onefile --optimize 2 --hide-console minimize-early -i ark.ico --uac-admin ark.py