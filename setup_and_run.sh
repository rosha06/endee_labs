#!/bin/bash
# Support Ticket Classifier - Complete Setup Script
# Run this for first-time setup (installs dependencies, creates index, loads data)

echo "======================================================================"
echo " Support Ticket Classifier - FIRST TIME SETUP"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found! Please install Python 3.11+"
    exit 1
fi

echo "This script will:"
echo "  1. Install Python dependencies"
echo "  2. Create Endee vector index"
echo "  3. Index sample tickets"
echo "  4. Start the API server"
echo ""
echo "Make sure Endee server is running on localhost:6333"
echo ""
read -p "Press Enter to continue..."

# Step 1: Install dependencies
echo ""
echo "======================================================================"
echo "[STEP 1/4] Installing dependencies..."
echo "======================================================================"
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

# Step 2: Create Endee index
echo ""
echo "======================================================================"
echo "[STEP 2/4] Creating Endee vector index..."
echo "======================================================================"
python3 scripts/setup_endee.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create index. Is Endee running?"
    exit 1
fi

# Step 3: Index sample tickets
echo ""
echo "======================================================================"
echo "[STEP 3/4] Indexing sample tickets..."
echo "======================================================================"
python3 scripts/index_tickets.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to index tickets"
    exit 1
fi

# Step 4: Start server
echo ""
echo "======================================================================"
echo "[STEP 4/4] Starting API server..."
echo "======================================================================"
echo ""
echo "API will be available at:"
echo "  - Documentation: http://localhost:8000/docs"
echo "  - Health Check:  http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
