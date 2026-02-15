@echo off
REM Stock Bulb Monitor - Windows Startup Script

echo =========================================
echo  Stock Bulb Monitor
echo =========================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the monitor
echo Starting monitor...
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo =========================================
    echo  Error occurred! Press any key to exit
    echo =========================================
    pause > nul
)
