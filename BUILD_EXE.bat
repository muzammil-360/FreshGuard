@echo off
title Food Expiry Calculator - EXE Builder
color 0A

echo ============================================
echo   FOOD EXPIRY CALCULATOR - EXE BUILDER
echo ============================================
echo.

:: Step 1: Check Python
echo [1/4] Python check kar raha hai...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python nahi mila! Python install karo pehle.
    echo Download: https://www.python.org/downloads/
    pause
    exit
)
echo       Python mil gaya!
echo.

:: Step 2: Install PyInstaller
echo [2/4] PyInstaller install ho raha hai...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: PyInstaller install nahi hua. Internet check karo.
    pause
    exit
)
echo       PyInstaller ready!
echo.

:: Step 3: Go to project folder
echo [3/4] Project folder mein ja raha hai...
cd /d "%~dp0"
echo       Folder: %cd%
echo.

:: Step 4: Build EXE
echo [4/4] EXE ban raha hai... (1-2 minute lagega)
echo.
pyinstaller --onefile --windowed --name "FoodExpiryCalculator" login_page.py

echo.
echo ============================================
if exist "dist\FoodExpiryCalculator.exe" (
    echo   SUCCESS! EXE BAN GAYA!
    echo   Location: dist\FoodExpiryCalculator.exe
    echo   Ab us .exe ko double-click karo!
    echo ============================================
    explorer dist
) else (
    echo   Kuch error aaya. Upar ka output dekho.
    echo ============================================
)

pause
