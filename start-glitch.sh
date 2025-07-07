#!/bin/bash

# Glitch Startup Script for AI Code Plagiarism Detector
echo "🚀 Setting up AI Code Plagiarism Detector on Glitch..."

# Function to print colored output
print_status() {
    echo "✅ $1"
}

print_error() {
    echo "❌ $1"
}

print_info() {
    echo "ℹ️  $1"
}

# Check if we're on Glitch
if [ -n "$PROJECT_DOMAIN" ]; then
    print_info "Detected Glitch environment: $PROJECT_DOMAIN"
    export GLITCH_ENV=true
else
    print_info "Running in local/other environment"
fi

# Install Python dependencies
print_info "Installing Python dependencies..."
if pip install -r requirements.txt; then
    print_status "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
print_info "Installing Node.js dependencies..."
if npm install; then
    print_status "Node.js dependencies installed"
else
    print_error "Failed to install Node.js dependencies"
    exit 1
fi

# Install frontend dependencies
print_info "Installing frontend dependencies..."
cd frontend
if npm ci; then
    print_status "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    cd ..
    exit 1
fi

# Build frontend
print_info "Building frontend application..."
if npm run build && npm run export; then
    print_status "Frontend built successfully"
else
    print_error "Failed to build frontend"
    cd ..
    exit 1
fi

cd ..

# Copy built files to public directory
print_info "Setting up static files..."
mkdir -p public
if cp -r frontend/out/* public/; then
    print_status "Static files copied to public/"
else
    print_error "Failed to copy static files"
    exit 1
fi

# Verify critical files exist
print_info "Verifying setup..."

if [ -f "public/index.html" ]; then
    print_status "Frontend files ready"
else
    print_error "Frontend build incomplete - index.html missing"
    exit 1
fi

if [ -f "main.py" ]; then
    print_status "Backend file ready"
else
    print_error "Backend file missing"
    exit 1
fi

if [ -f "server.js" ]; then
    print_status "Server file ready"
else
    print_error "Server file missing"
    exit 1
fi

# Check environment variables
print_info "Checking environment variables..."
if [ -n "$COHERE_API_KEY" ] && [ -n "$TOGETHER_API_KEY" ] && [ -n "$REPLICATE_API_TOKEN" ]; then
    print_status "API keys configured"
else
    print_error "Missing API keys in .env file"
    print_info "Please add your API keys to the .env file:"
    print_info "COHERE_API_KEY=your_key_here"
    print_info "TOGETHER_API_KEY=your_key_here"
    print_info "REPLICATE_API_TOKEN=your_token_here"
fi

print_status "Setup complete! Starting application..."

# Start the application
exec node server.js
