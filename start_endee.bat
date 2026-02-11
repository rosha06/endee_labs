@echo off
REM Start Endee Server using Docker Compose

echo ======================================================================
echo  Starting Endee Vector Database
echo ======================================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker not found! Please install Docker Desktop
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/2] Starting Endee server via Docker...
echo.

docker compose -f docker-compose-endee.yml up -d

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start Endee server
    pause
    exit /b 1
)

echo.
echo [2/2] Endee server is starting...
echo.
echo Waiting for Endee to be ready (5 seconds)...
timeout /t 5 /nobreak >nul

echo.
echo ======================================================================
echo  Endee Server Status
echo ======================================================================
echo  Status: Running
echo  URL: http://localhost:8080
echo  Container: endee-server
echo.
echo To stop Endee:
echo   docker compose -f docker-compose-endee.yml down
echo.
echo To view logs:
echo   docker logs endee-server
echo ======================================================================
echo.

pause
