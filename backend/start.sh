#!/bin/bash

# Mock Interview Backend - Start Script

cd "$(dirname "$0")"

echo "🚀 Starting Mock Interview Backend..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3.12 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "   ✅ Created .env file"
    echo "   ⚠️  Please update it with your Supabase and OpenAI credentials!"
    echo ""
fi

# Check if DATABASE_URL is configured
if grep -q "YOUR-PASSWORD" .env || grep -q "PROJECT-REF" .env; then
    echo "⚠️  Database not configured!"
    echo ""
    echo "Please update your .env file with:"
    echo "1. Supabase DATABASE_URL"
    echo "2. OpenAI API KEY"
    echo ""
    echo "See SETUP_COMPLETE.md for instructions."
    exit 1
fi

echo "✅ Environment configured"
echo "🌐 Starting server on http://localhost:8000"
echo "📚 API docs will be at http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop"
echo ""

# Start uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
