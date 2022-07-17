del /f /s /q dist
del /f /s /q build
pyinstaller -F init.py -i icon.ico --add-data "assets;assets"