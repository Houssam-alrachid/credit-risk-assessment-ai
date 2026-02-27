@echo off
REM =============================================================================
REM Remove Package with UV - Credit Risk Assessment AI
REM =============================================================================

if "%1"=="" (
    echo Usage: remove-package.bat PACKAGE_NAME
    echo Example: remove-package.bat requests
    pause
    exit /b 1
)

echo Removing package: %1
uv remove %*
echo.
echo Package removed successfully!
pause
