#!/bin/bash

# Create and activate virtual environment
if [ ! -d "backend/venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv backend/venv
fi
source backend/venv/bin/activate

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install pytest pytest-asyncio pytest-mock httpx google-generativeai firebase-admin sqlalchemy fastapi uvicorn python-multipart pypdf Pillow pydantic-settings

# Run tests
echo "🚀 Running tests..."
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest backend/tests -v
