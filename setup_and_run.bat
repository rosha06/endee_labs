@echo off
REM Complete Setup: Start Endee + Setup Project + Run API
REM This is the ONE-COMMAND SOLUTION!

echo ======================================================================
echo  Support Ticket Classifier - COMPLETE SETUP
echo ======================================================================
echo.
echo This will:
echo   1. Start Endee vector database (Docker)
echo   2. Install Python dependencies
echo   3. Create vector index
echo   4. Load sample tickets
echo   5. Start the API server
echo.
pause

REM ==================== STEP 1: Start Endee ====================
echo.
echo ======================================================================
echo [STEP 1/5] Starting Endee server...
echo ======================================================================

docker compose -f docker-compose-endee.yml up -d
if errorlevel 1 (
    echo [ERROR] Failed to start Endee. Is Docker installed and running?
    pause
    exit /b 1
)

echo Waiting for Endee to be ready...
timeout /t 8 /nobreak >nul

REM ==================== STEP 2: Install Dependencies ====================
echo.
echo ======================================================================
echo [STEP 2/5] Installing dependencies...
echo ======================================================================
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM ==================== STEP 3: Create Index ====================
echo.
echo ======================================================================
echo [STEP 3/5] Creating vector index in Endee...
echo ======================================================================
python scripts/setup_endee.py
if errorlevel 1 (
    echo [ERROR] Failed to create index
    pause
    exit /b 1
)

REM ==================== STEP 4: Index Tickets ====================
echo.
echo ======================================================================
echo [STEP 4/5] Indexing sample tickets...
echo ======================================================================
python scripts/index_tickets.py
if errorlevel 1 (
    echo [ERROR] Failed to index tickets
    pause
    exit /b 1
)

REM ==================== STEP 5: Start API ====================
echo.
echo ======================================================================
echo [STEP 5/5] Starting API server...
echo ======================================================================
echo.
echo  SETUP COMPLETE! 
echo.
echo  API available at:
echo    - Documentation: http://localhost:8000/docs
echo    - Health Check: http://localhost:8000/health
echo.
echo  Endee Dashboard: http://localhost:8080
echo.
echo  Press Ctrl+C to stop
echo.
echo ======================================================================
echo.

python main.py

pause
