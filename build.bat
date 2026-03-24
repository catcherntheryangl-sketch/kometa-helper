@echo off
REM ============================================================
REM  build.bat - Build Kometa Helper into a standalone .exe
REM  Run this from the root of the project on Windows
REM ============================================================

echo.
echo  ===== Kometa Helper Build Script =====
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)

REM Create/activate venv
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Installing/upgrading dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
pip install pyinstaller --quiet

echo [INFO] Running PyInstaller...
pyinstaller kometa-helper.spec --noconfirm

if errorlevel 1 (
    echo [ERROR] PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo  ===== Build Complete =====
echo  Output: dist\KometaHelper.exe
echo.

REM Optional: open dist folder
explorer dist

pause
