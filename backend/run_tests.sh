#!/bin/bash

# Test runner script for Mock Interview API
# This script runs all tests with coverage reporting

set -e  # Exit on error

echo "========================================"
echo "Running Mock Interview API Tests"
echo "========================================"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo "✓ Activating virtual environment..."
    source venv/bin/activate
else
    echo "✗ Virtual environment not found!"
    echo "  Run: python3.12 -m venv venv"
    exit 1
fi

# Check if pytest is installed
if ! python -c "import pytest" 2>/dev/null; then
    echo "✗ pytest not installed!"
    echo "  Installing test dependencies..."
    pip install pytest pytest-cov pytest-asyncio httpx
fi

echo ""
echo "Running tests..."
echo "----------------------------------------"

# Run tests with coverage
pytest \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    -v

echo ""
echo "========================================"
echo "Test Results"
echo "========================================"
echo ""
echo "✓ Tests completed!"
echo ""
echo "Coverage report saved to: htmlcov/index.html"
echo "Open it with: open htmlcov/index.html"
echo ""
