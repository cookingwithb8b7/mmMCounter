@echo off
REM Build script for mmMCounter Windows executable
REM Run this from the build directory

echo ========================================
echo mmMCounter Build Script
echo ========================================
echo.

REM Navigate to build directory
cd /d "%~dp0"

REM Check if PyInstaller is installed
echo Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing PyInstaller 6.3.0...
    pip install pyinstaller==6.3.0
    if errorlevel 1 (
        echo Failed to install PyInstaller!
        pause
        exit /b 1
    )
) else (
    echo PyInstaller found.
)

echo.
echo Cleaning previous builds...

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist mmMCounter rmdir /s /q mmMCounter

echo.
echo Building executable with PyInstaller...
echo This may take a few minutes...
echo.

REM Build executable
pyinstaller mmMCounter.spec

REM Check if build succeeded
if exist dist\mmMCounter.exe (
    echo.
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo Executable location: dist\mmMCounter.exe
    echo.
    echo File size:
    dir dist\mmMCounter.exe | find "mmMCounter.exe"
    echo.
    echo ========================================
    echo.
    echo You can now run dist\mmMCounter.exe
    echo.
) else (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    echo.
    echo Check the error messages above.
    echo.
    exit /b 1
)

pause
