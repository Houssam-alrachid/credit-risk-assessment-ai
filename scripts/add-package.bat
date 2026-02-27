@echo off
REM =============================================================================
REM Add Package with UV - Credit Risk Assessment AI
REM =============================================================================

if "%1"=="" (
    echo Usage: add-package.bat PACKAGE_NAME
    echo Example: add-package.bat requests
    pause
    exit /b 1
)

echo Adding package: %1
uv add %*
echo.
echo Package added successfully!
pause
