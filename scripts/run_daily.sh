#!/bin/bash

# Daily News Collection Script

# Set script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Set environment variables
export PYTHONPATH="$PROJECT_DIR"

# Log file with timestamp
LOG_FILE="logs/daily_run_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

# Run the application with logging
echo "Starting daily news collection at $(date)" | tee -a "$LOG_FILE"
python main.py 2>&1 | tee -a "$LOG_FILE"

# Check exit code
if [ $? -eq 0 ]; then
    echo "Daily news collection completed successfully at $(date)" | tee -a "$LOG_FILE"

    # Optional: Send success notification
    # curl -X POST "your-webhook-url" -d "Smart Journalist: Daily report generated successfully"
else
    echo "Daily news collection failed at $(date)" | tee -a "$LOG_FILE"

    # Optional: Send failure notification
    # curl -X POST "your-error-webhook-url" -d "Smart Journalist: Daily report generation failed"
fi
