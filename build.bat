@echo off
:: ============================================================================
::  build.bat  –  Build url2html_gui.exe using PyInstaller
::
::  Usage:
::      build.bat           (uses Python on PATH)
::      build.bat C:\Python311\python.exe   (explicit interpreter)
::
::  Requirements installed automatically if missing:
::      pip install pillow pyinstaller
::
::  Output:  dist\url2html_gui.exe
:: ============================================================================

setlocal EnableDelayedExpansion

:: ── Resolve Python interpreter ────────────────────────────────────────────────
if "%~1"=="" (
    set PYTHON=python
) else (
    set PYTHON=%~1
)

echo.
echo ============================================================
echo   url2html GUI  --  Build Script
echo ============================================================
echo   Python  : %PYTHON%
echo   Script  : url2html_gui.py
echo   Icon    : url2html_gui.ico
echo ============================================================
echo.

:: ── Verify Python is available ────────────────────────────────────────────────
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.  Install Python 3.8+ or pass the full
    echo         path to python.exe as the first argument.
    echo.
    echo         Example:  build.bat C:\Python311\python.exe
    goto :fail
)

:: ── Verify source file exists ─────────────────────────────────────────────────
if not exist "url2html_gui.py" (
    echo [ERROR] url2html_gui.py not found in the current directory.
    echo         Run this script from the folder that contains the source files.
    goto :fail
)

:: ── Step 1: Install / upgrade dependencies ────────────────────────────────────
echo [1/4]  Installing required packages ...
echo.
%PYTHON% -m pip install --upgrade pip --quiet
%PYTHON% -m pip install --upgrade pillow pyinstaller --quiet
if errorlevel 1 (
    echo [ERROR] pip install failed.  Check your internet connection and pip configuration.
    goto :fail
)
echo        Done.
echo.

:: ── Step 2: Generate icon ─────────────────────────────────────────────────────
echo [2/4]  Generating icon ...
echo.
if exist "make_icon.py" (
    %PYTHON% make_icon.py
    if errorlevel 1 (
        echo [WARN]  make_icon.py failed.  Trying to continue with existing icon ...
    ) else (
        echo        Icon generated: url2html_gui.ico
    )
) else (
    echo        make_icon.py not found – using existing url2html_gui.ico
)

if not exist "url2html_gui.ico" (
    echo [ERROR] url2html_gui.ico not found.  Cannot embed icon.
    goto :fail
)
echo.

:: ── Step 3: Clean previous build artefacts ────────────────────────────────────
echo [3/4]  Cleaning previous build ...
echo.
if exist "build"              rmdir /s /q "build"
if exist "dist"               rmdir /s /q "dist"
if exist "url2html_gui.spec"  del /q "url2html_gui.spec"
echo        Done.
echo.

:: ── Step 4: Run PyInstaller ───────────────────────────────────────────────────
echo [4/4]  Running PyInstaller ...
echo.

%PYTHON% -m PyInstaller ^
    --onefile ^
    --windowed ^
    --icon="url2html_gui.ico" ^
    --name="url2html_gui" ^
    --add-data="url2html_gui.ico;." ^
    --noconfirm ^
    --clean ^
    "url2html_gui.py"

if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller failed.  See output above for details.
    goto :fail
)

:: ── Done ──────────────────────────────────────────────────────────────────────
echo.
echo ============================================================
echo   BUILD SUCCESSFUL
echo ============================================================
if exist "dist\url2html_gui.exe" (
    for %%F in ("dist\url2html_gui.exe") do (
        echo   Output : dist\url2html_gui.exe
        echo   Size   : %%~zF bytes
    )
)
echo.
echo   Copy dist\url2html_gui.exe to any Windows PC and run it.
echo   No Python installation is required on the target machine.
echo ============================================================
echo.
goto :end

:fail
echo.
echo ============================================================
echo   BUILD FAILED  -- see errors above
echo ============================================================
echo.
exit /b 1

:end
endlocal
