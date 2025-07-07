@echo off
echo Setting up AI Code Plagiarism Detector...

echo.
echo Step 1: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Setting up frontend...
cd frontend
call npm install

echo.
echo Step 3: Building frontend...
call npm run build
call npm run export

echo.
echo Step 4: Going back to root directory...
cd ..

echo.
echo ========================================
echo Setup completed successfully! 
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Add your API keys to the .env file:
echo    - COHERE_API_KEY=your_key_here
echo    - TOGETHER_API_KEY=your_key_here  
echo    - REPLICATE_API_TOKEN=your_token_here
echo 3. Run: python main.py
echo 4. Open: http://localhost:5000
echo.
echo Get your free API keys from:
echo - Cohere: https://dashboard.cohere.ai/
echo - Together.ai: https://www.together.ai/
echo - Replicate: https://replicate.com/
echo.
pause
