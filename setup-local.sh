#!/bin/bash

# Local Development Setup Script for AI Code Plagiarism Detector
echo "🏠 Setting up AI Code Plagiarism Detector for Local Development..."

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

print_warning() {
    echo "⚠️  $1"
}

# Check if Node.js is installed
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js is installed: $NODE_VERSION"
else
    print_error "Node.js is not installed!"
    print_info "Please install Node.js from: https://nodejs.org"
    print_info "Recommended version: 18.x or higher"
    exit 1
fi

# Check if npm is installed
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_status "npm is installed: $NPM_VERSION"
else
    print_error "npm is not installed!"
    print_info "npm usually comes with Node.js. Please reinstall Node.js"
    exit 1
fi

# Check if Python is installed
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    print_status "Python is installed: $PYTHON_VERSION"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "Python3 is installed: $PYTHON_VERSION"
    alias python=python3
else
    print_error "Python is not installed!"
    print_info "Please install Python 3.8+ from: https://python.org"
    exit 1
fi

# Check if pip is installed
if command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version)
    print_status "pip is installed: $PIP_VERSION"
elif command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    print_status "pip3 is installed: $PIP_VERSION"
    alias pip=pip3
else
    print_error "pip is not installed!"
    print_info "Please install pip with your Python installation"
    exit 1
fi

print_info "All prerequisites satisfied! Setting up project..."

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
if npm install; then
    print_status "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    cd ..
    exit 1
fi

# Build frontend
print_info "Building frontend..."
if npm run build && npm run export; then
    print_status "Frontend built successfully"
else
    print_error "Failed to build frontend"
    cd ..
    exit 1
fi

cd ..

# Create public directory and copy files
print_info "Setting up static files..."
mkdir -p public
if cp -r frontend/out/* public/; then
    print_status "Static files copied to public/"
else
    print_error "Failed to copy static files"
    exit 1
fi

# Check environment variables
print_info "Checking environment variables..."
if [ -f ".env" ]; then
    if grep -q "COHERE_API_KEY" .env && grep -q "TOGETHER_API_KEY" .env && grep -q "REPLICATE_API_TOKEN" .env; then
        print_status "Environment variables found in .env file"
    else
        print_warning "Some API keys missing in .env file"
        print_info "Make sure to add your API keys to .env file"
    fi
else
    print_warning "No .env file found"
    print_info "Create a .env file with your API keys:"
    print_info "COHERE_API_KEY=your_key_here"
    print_info "TOGETHER_API_KEY=your_key_here"
    print_info "REPLICATE_API_TOKEN=your_token_here"
fi

print_status "Local development setup complete!"
print_info "To start the application:"
print_info "1. Make sure your .env file has API keys"
print_info "2. Run: python main.py"
print_info "3. Open: http://localhost:5000"

print_warning "Note: For production deployment, use Glitch (see QUICKSTART.md)"
