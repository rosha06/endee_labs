@echo off
REM Support Ticket Classifier - Quick Start Script
REM Run this to start the API server

echo ======================================================================
echo  Support Ticket Classifier API
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

echo [1/3] Starting application...
echo.

REM Start the API server
echo [2/3] Launching FastAPI server...
echo.
echo API will be available at:
echo   - Documentation: http://localhost:8000/docs
echo   - Health Check:  http://localhost:8000/health
echo.
echo [3/3] Press Ctrl+C to stop the server
echo.

python main.py

pause
