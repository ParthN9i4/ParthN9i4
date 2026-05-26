#!/usr/bin/env bash
# PPML/FHE Research Dashboard — Quick Start Script

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================================"
echo "  PPML/FHE Research Dashboard"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env to set your password and API keys."
    echo "  Default password: changeme"
    echo ""
fi

echo ""
echo "Starting dashboard at http://127.0.0.1:5000"
echo "Default password: changeme (change in .env or Settings page)"
echo "Press Ctrl+C to stop."
echo ""

python3 app.py
