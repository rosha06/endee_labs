#!/bin/bash
# Support Ticket Classifier - Quick Start Script
# Run this to start the API server

echo "======================================================================"
echo " Support Ticket Classifier API"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found! Please install Python 3.11+"
    exit 1
fi

echo "[1/3] Starting application..."
echo ""

# Start the API server
echo "[2/3] Launching FastAPI server..."
echo ""
echo "API will be available at:"
echo "  - Documentation: http://localhost:8000/docs"
echo "  - Health Check:  http://localhost:8000/health"
echo ""
echo "[3/3] Press Ctrl+C to stop the server"
echo ""

python3 main.py
