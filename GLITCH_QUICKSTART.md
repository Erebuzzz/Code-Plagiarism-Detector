# 🚀 Glitch Quickstart Guide - AI Code Plagiarism Detector

## Deploy in 5 Minutes! (100% FREE)

### Step 1: Prepare Your Environment Variables
Before starting, gather these API keys:
- **Cohere API Key**: Get free at [cohere.ai](https://cohere.ai)
- **Together.ai API Key**: Get free at [together.ai](https://together.ai)
- **Replicate Token**: Get free at [replicate.com](https://replicate.com)

### Step 2: Deploy to Glitch

#### Option A: Import from GitHub (Recommended)
1. Go to [glitch.com](https://glitch.com) and sign up (free)
2. Click "New Project" → "Import from GitHub"
3. Enter: `https://github.com/yourusername/Code-Plagiarism-Detector`
4. Name your project: `ai-code-plagiarism-detector`

#### Option B: Manual Setup
1. Go to [glitch.com](https://glitch.com) and create account
2. Click "New Project" → "hello-express"
3. Replace all files with your project files

### Step 3: Configure Environment Variables
1. In Glitch, click the `.env` file in the sidebar
2. Add these variables:
```
COHERE_API_KEY=your_cohere_key_here
TOGETHER_API_KEY=your_together_ai_key_here
REPLICATE_API_TOKEN=your_replicate_token_here
GLITCH_ENV=true
NODE_ENV=production
```

### Step 4: Install Dependencies
Glitch will automatically install dependencies. If not, in the terminal run:
```bash
npm install
pip install -r requirements.txt
```

### Step 5: Build Frontend
In the Glitch terminal, run:
```bash
npm run build
```

### Step 6: Start the App
Click the "Show" button in Glitch or run:
```bash
npm start
```

## 🎉 Your App is Live!

Your app will be available at: `https://your-project-name.glitch.me`

## 🔧 Project Structure on Glitch
```
/
├── server.js              # Express server (proxy + frontend)
├── main.py                # Flask backend (AI analysis)
├── package.json           # Node.js dependencies
├── requirements.txt       # Python dependencies
├── glitch.json           # Glitch configuration
├── .env                  # Environment variables
├── frontend/             # Next.js source code
└── public/               # Built frontend files
```

## 🌐 How It Works
1. **Express Server**: Serves frontend and proxies API calls
2. **Flask Backend**: Handles AI analysis at port 5000
3. **Unified Access**: Everything accessible from one URL

## 📍 API Endpoints
- `GET /` → React Frontend
- `POST /api/check` → Code plagiarism check
- `POST /api/analyze` → Code structure analysis
- `POST /api/detailed-check` → Detailed comparison
- `GET /api/health` → Backend health check

## 🛠️ Troubleshooting

### App Won't Start?
1. Check `.env` file has all required API keys
2. Run `npm run build` in the terminal
3. Make sure `public/` folder has frontend files

### Backend Errors?
1. Check `requirements.txt` dependencies installed
2. Verify API keys are correct
3. Check logs in Glitch terminal

### Frontend Not Loading?
1. Ensure `npm run build` completed successfully
2. Check `public/index.html` exists
3. Restart the project

## 💡 Pro Tips
- **Free Tier**: App sleeps after 5 minutes of inactivity
- **Waking Up**: First request after sleep takes ~10-15 seconds
- **Resources**: 512MB RAM, 1GB storage, 4000 requests/hour
- **Always Free**: No credit card required!

## 🎯 Quick Commands
```bash
# Restart the app
refresh

# Check logs
logs

# Install packages
npm install
pip install -r requirements.txt

# Build frontend
npm run build

# Start manually
npm start
```

## 🌟 Features Working Out of the Box
✅ Code plagiarism detection  
✅ AI-generated code detection  
✅ Similarity analysis  
✅ Code structure analysis  
✅ Beautiful responsive UI  
✅ Real-time analysis  
✅ Multiple AI models  

## 📞 Need Help?
- Glitch Support: [help.glitch.com](https://help.glitch.com)
- Project Issues: Check your GitHub repository
- API Issues: Verify your API keys

---
**🎉 Congratulations! Your AI Code Plagiarism Detector is now live and free forever!**
