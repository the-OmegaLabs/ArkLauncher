@echo off

pyinstaller --onefile --optimize 2 --noupx -i ark.ico --disable-windowed-traceback ark.py
