@echo off
REM =============================================================================
REM Start All Services - Credit Risk Assessment AI
REM =============================================================================

echo ============================================================
echo    Starting Credit Risk Assessment AI
echo ============================================================
echo.
echo This will start both backend and frontend in separate windows.
echo.

REM Start backend in new window
start "Backend API" cmd /k "%~dp0start-backend.bat"

REM Wait for backend to start
echo [INFO] Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend in new window
start "Frontend" cmd /k "%~dp0start-frontend.bat"

echo.
echo ============================================================
echo    Services Starting
echo ============================================================
echo.
echo    Backend API:  http://localhost:8080
echo    API Docs:     http://localhost:8080/docs
echo    Frontend:     http://localhost:3000
echo.
echo    Close the terminal windows to stop the services.
echo ============================================================
echo.
pause
