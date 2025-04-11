@echo off

python -c "import os, sys; sys.exit(bool(not sys.version_info >= (3,10)))"
setlocal
IF %errorlevel% equ 1 (
    echo You are not using Python 3.10 or later
    pause
    exit /b 1
) ELSE (
    IF %errorlevel% equ 9009 (
        echo Python is not installed
        pause
        exit /b 1
    )
)
IF NOT EXIST ".venv" (
    echo Creating venv
    python -m venv .venv
 ) ELSE (
    echo Venv already exists
 )


call .venv\Scripts\activate.bat

python -m pip install -r requirements.txt
IF %errorlevel% equ 0 (
    python builder\main.py
)
endlocal
pause