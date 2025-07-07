#!/bin/bash

echo "🚀 Starting AI Code Plagiarism Detector on Replit..."
echo "=================================================="

# Set environment variables for Replit
export PORT=5000
export HOST=0.0.0.0
export FLASK_ENV=production

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if frontend directory exists and install Node.js dependencies
if [ -d "frontend" ]; then
    echo "📦 Installing Node.js dependencies..."
    cd frontend
    npm install
    
    echo "🔨 Building frontend..."
    npm run build
    
    echo "📁 Copying built files to static directory..."
    cd ..
    
    # Create static directory if it doesn't exist
    mkdir -p static
    
    # Copy built files to static directory for Flask to serve
    if [ -d "frontend/out" ]; then
        cp -r frontend/out/* static/
        echo "✅ Frontend build copied to static directory"
    elif [ -d "frontend/.next" ]; then
        cp -r frontend/.next/static static/
        echo "✅ Frontend build copied to static directory"
    else
        echo "⚠️  Frontend build not found, serving from source"
    fi
else
    echo "⚠️  Frontend directory not found, serving backend only"
fi

echo "🌐 Starting Flask server on port $PORT..."
echo "🔗 Your app will be available at: https://$REPL_SLUG.$REPL_OWNER.repl.co"

# Start the Flask application
python main.py
