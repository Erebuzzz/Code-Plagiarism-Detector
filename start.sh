#!/bin/bash

# Zeabur deployment startup script
echo "🚀 Starting AI Code Plagiarism Detector on Zeabur..."

# Install dependencies
pip install -r requirements.txt

# Set environment variables for production
export FLASK_ENV=production

# Start the Flask application
python main.py
