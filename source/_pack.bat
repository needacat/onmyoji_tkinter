@REM pyinstaller -i "resource/icon.ico" -F -w %1
pyinstaller -i "resource/icon.ico" -F -w main.py
@REM nuitka  --standalone --output-dir=dist --enable-plugin=tk-inter --windows-icon-from-ico=resource/icon.ico %1
echo dp0 = %~dp0
move /Y .\dist\main.exe OSS.exe
@echo off
del main.spec
pause