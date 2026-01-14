#!/bin/bash

# Start script for Mock Interview Frontend
# This script starts the Vite development server

set -e

echo "========================================"
echo "Mock Interview App - Frontend"
echo "========================================"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "✗ node_modules not found!"
    echo "  Installing dependencies..."
    npm install
    echo ""
fi

echo "✓ Starting development server..."
echo "  Frontend will be available at: http://localhost:5173"
echo "  Make sure backend is running at: http://localhost:8000"
echo ""

# Start dev server
npm run dev
