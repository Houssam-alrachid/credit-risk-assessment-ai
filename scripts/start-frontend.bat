@echo off
REM =============================================================================
REM Start Frontend - Credit Risk Assessment AI
REM =============================================================================

echo ============================================================
echo    Starting Frontend
echo ============================================================
echo.

cd /d "%~dp0..\frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    npm install
)

echo.
echo ============================================================
echo    Frontend starting on http://localhost:3000
echo    Press Ctrl+C to stop
echo ============================================================
echo.

npm run dev
