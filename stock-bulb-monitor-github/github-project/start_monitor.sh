#!/bin/bash
# Stock Bulb Monitor - Mac/Linux Startup Script

echo "========================================="
echo " Stock Bulb Monitor"
echo "========================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the monitor
echo "Starting monitor..."
echo ""
python3 main.py

# If error occurred, wait
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================="
    echo " Error occurred! Press ENTER to exit"
    echo "========================================="
    read
fi
