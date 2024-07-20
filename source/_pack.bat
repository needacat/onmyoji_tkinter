pyinstaller -i "../resource/icon.png" -F -w %1
@REM nuitka  --standalone --output-dir=dist --enable-plugin=tk-inter --windows-icon-from-ico=resource/icon.png %1
echo dp0 = %~dp0
move /Y .\dist\main.exe OSS.exe
del main.spec
pause