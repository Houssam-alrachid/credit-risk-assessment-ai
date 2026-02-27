@echo off
REM =============================================================================
REM Start Backend - Credit Risk Assessment AI
REM =============================================================================

echo ============================================================
echo    Starting Backend API
echo ============================================================
echo.

cd /d "%~dp0..\backend"

REM Check if .env exists in root
if not exist "..\\.env" (
    echo [WARNING] .env file not found!
    echo Please create .env in the project root with your API keys.
    pause
    exit /b 1
)

REM Copy .env to backend
copy /Y "..\\.env" ".env" >nul

REM Check if uv is installed
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] uv is not installed!
    pause
    exit /b 1
)

REM Sync dependencies
if not exist ".venv" (
    echo [INFO] Setting up virtual environment...
    uv sync
)

echo.
echo ============================================================
echo    Backend starting on http://localhost:8080
echo    API Docs: http://localhost:8080/docs
echo    Press Ctrl+C to stop
echo ============================================================
echo.

uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

echo.
echo [INFO] Cleaning up...
taskkill /F /IM python.exe /T >nul 2>&1
