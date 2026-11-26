
@echo off
setlocal

set "VENV_DIR=cli\.venv"
set "PYTHON=python"

REM Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\python.exe" (

    REM 1. Check Python installation
    where python >nul 2>&1
    if errorlevel 1 (
        echo Error: Python is not installed or not in PATH.
        exit /b 1
    )

    REM 2. Check Python version (3.13+)
    python -c "import sys; sys.exit(0 if sys.version_info >= (3, 13) else 1)"
    if errorlevel 1 (
        echo Error: Python 3.13 or above is required.
        python --version
        exit /b 1
    )

    REM 3. Check pip
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo Error: pip is not installed.
        exit /b 1
    )

    REM 4. Create virtual environment
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 exit /b 1

    REM 5. Install dependencies
    echo Installing CLI dependencies...
    "%VENV_DIR%\Scripts\python.exe" -m pip install -r cli\requirements.txt
    if errorlevel 1 exit /b 1
)

REM 6. Execute CLI and forward all arguments
"%VENV_DIR%\Scripts\python.exe" cli %*
exit /b %ERRORLEVEL%
