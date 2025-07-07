# 🚀 Quick Start Guide

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- Git (optional, for cloning)

## Installation

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Setup frontend:**
```bash
cd frontend
npm install
npm run build
npm run export
cd ..
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Get API Keys (Free)

### 1. Cohere API Key
- Visit: https://dashboard.cohere.ai/
- Sign up for free account
- Go to API Keys section
- Copy your key

### 2. Together.ai API Key
- Visit: https://www.together.ai/
- Create free account
- Navigate to API section
- Generate and copy key

### 3. Replicate API Token
- Visit: https://replicate.com/
- Sign up for free
- Go to Account → API tokens
- Create and copy token

## Configuration

Edit your `.env` file:
```env
COHERE_API_KEY=your_cohere_key_here
TOGETHER_API_KEY=your_together_key_here
REPLICATE_API_TOKEN=your_replicate_token_here
```

## Running the Application

1. **Start the server:**
```bash
python main.py
```

2. **Open in browser:**
```
http://localhost:5000
```

## Testing

Run the API test script:
```bash
python test_api.py
```

## Usage

1. **Enter Code**: Paste two code snippets in the editors
2. **Compare**: Click "Compare Code" button
3. **View Results**: See similarity scores and analysis
4. **Interpret**: 
   - 80%+ = High similarity (potential plagiarism)
   - 60-80% = Moderate similarity (review needed)
   - 40-60% = Low similarity (some patterns)
   - <40% = Very low similarity (likely original)

## Features

- ✅ Multiple AI model analysis
- ✅ Monaco code editor with syntax highlighting
- ✅ Dark/light theme support
- ✅ Responsive design
- ✅ Real-time similarity scores
- ✅ Radar chart visualization
- ✅ REST API endpoint

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Frontend not loading
```bash
cd frontend
npm run build
npm run export
cd ..
```

### API errors
- Check your `.env` file has correct API keys
- Verify internet connection
- Check API key quotas

### Port already in use
- Change port in `main.py`: `app.run(port=5001)`
- Or kill existing process

## Support

- Check the README.md for detailed documentation
- Test with `python test_api.py`
- Verify API keys are valid and have quota
- Ensure all dependencies are installed

## Deployment

### Replit (Recommended)
1. Upload files to Replit
2. Set environment variables in Replit Secrets
3. Run the project

### Other Platforms
- Works on any platform supporting Python + Node.js
- No Docker required
- Static frontend served by Flask
