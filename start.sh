#!/bin/bash

echo "Starting Ron's Blog..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo

# Install/update requirements
echo "Installing requirements..."
pip install -r requirements.txt
echo

# Copy environment file if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo
fi

# Start the Flask development server
echo "Starting Flask development server..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo
python app.py
