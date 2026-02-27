@echo off
REM =============================================================================
REM Setup UV Environment - Credit Risk Assessment AI
REM =============================================================================

echo ============================================================
echo    Setting up UV environment
echo ============================================================
echo.

REM Check if uv is installed
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] uv is not installed!
    echo.
    echo Install uv with:
    echo   PowerShell: irm https://astral.sh/uv/install.ps1 ^| iex
    echo   Or: pip install uv
    echo.
    pause
    exit /b 1
)

echo [INFO] uv found: 
uv --version
echo.

REM Sync dependencies
echo [INFO] Syncing dependencies with uv...
uv sync

echo.
echo ============================================================
echo    Setup complete!
echo ============================================================
echo.
echo To activate the environment:
echo   .venv\Scripts\activate
echo.
echo To run the app:
echo   uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
echo.
pause
