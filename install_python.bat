@echo off

python --version
if %errorlevel% equ 0 (
    echo Python is already installed
    pause
    exit /b 0
)

set "PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
set "PYTHON_EXE=python-installer.exe"

curl -L -o %PYTHON_EXE% %PYTHON_URL%

start /wait %PYTHON_EXE% /quiet /passive InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0

del %PYTHON_EXE%
