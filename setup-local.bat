@echo off
echo 🏠 Setting up AI Code Plagiarism Detector for Local Development...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo ℹ️  Please install Node.js from: https://nodejs.org
    echo ℹ️  Recommended version: 18.x or higher
    pause
    exit /b 1
) else (
    echo ✅ Node.js is installed
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed!
    echo ℹ️  npm usually comes with Node.js. Please reinstall Node.js
    pause
    exit /b 1
) else (
    echo ✅ npm is installed
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo ℹ️  Please install Python 3.8+ from: https://python.org
    echo ℹ️  Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    echo ✅ Python is installed
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed!
    echo ℹ️  Please install pip with your Python installation
    pause
    exit /b 1
) else (
    echo ✅ pip is installed
)

echo ℹ️  All prerequisites satisfied! Setting up project...

REM Install Python dependencies
echo ℹ️  Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
) else (
    echo ✅ Python dependencies installed
)

REM Install Node.js dependencies
echo ℹ️  Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
) else (
    echo ✅ Node.js dependencies installed
)

REM Install frontend dependencies
echo ℹ️  Installing frontend dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Frontend dependencies installed
)

REM Build frontend
echo ℹ️  Building frontend...
npm run build
if %errorlevel% neq 0 (
    echo ❌ Failed to build frontend
    cd ..
    pause
    exit /b 1
)

npm run export
if %errorlevel% neq 0 (
    echo ❌ Failed to export frontend
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Frontend built successfully
)

cd ..

REM Create public directory and copy files
echo ℹ️  Setting up static files...
if not exist "public" mkdir public
xcopy /E /Y "frontend\out\*" "public\"
if %errorlevel% neq 0 (
    echo ❌ Failed to copy static files
    pause
    exit /b 1
) else (
    echo ✅ Static files copied to public\
)

REM Check environment variables
echo ℹ️  Checking environment variables...
if exist ".env" (
    findstr /C:"COHERE_API_KEY" .env >nul && findstr /C:"TOGETHER_API_KEY" .env >nul && findstr /C:"REPLICATE_API_TOKEN" .env >nul
    if %errorlevel% equ 0 (
        echo ✅ Environment variables found in .env file
    ) else (
        echo ⚠️  Some API keys missing in .env file
        echo ℹ️  Make sure to add your API keys to .env file
    )
) else (
    echo ⚠️  No .env file found
    echo ℹ️  Create a .env file with your API keys:
    echo ℹ️  COHERE_API_KEY=your_key_here
    echo ℹ️  TOGETHER_API_KEY=your_key_here
    echo ℹ️  REPLICATE_API_TOKEN=your_token_here
)

echo.
echo ✅ Local development setup complete!
echo ℹ️  To start the application:
echo ℹ️  1. Make sure your .env file has API keys
echo ℹ️  2. Run: python main.py
echo ℹ️  3. Open: http://localhost:5000
echo.
echo ⚠️  Note: For production deployment, use Glitch (see QUICKSTART.md)
echo.
pause
