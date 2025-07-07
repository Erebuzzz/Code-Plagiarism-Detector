# 🚀 Quick Deploy to Replit - 5 Minutes!

## Your AI Code Plagiarism Detector is Ready for Replit! ✅

### 📁 Files Ready for Deployment:
- ✅ `.replit` - Replit configuration
- ✅ `replit.nix` - System dependencies  
- ✅ `pyproject.toml` - Python project config
- ✅ `start.sh` - Startup script
- ✅ `main.py` - Modified for Replit hosting
- ✅ Frontend updated for same-origin API calls

### 🎯 Deploy in 3 Steps:

#### Step 1: Push to GitHub (Optional but Recommended)
```bash
git add .
git commit -m "Ready for Replit deployment"
git push origin main
```

#### Step 2: Import to Replit
1. Go to [replit.com](https://replit.com) 
2. Click "Create Repl" → "Import from GitHub"
3. Paste your repo URL
4. Name it: `ai-code-plagiarism-detector`

#### Step 3: Add API Keys & Run
1. In Replit, click "Secrets" (🔒)
2. Add your API keys:
   - `COHERE_API_KEY`
   - `TOGETHER_API_KEY`
   - `REPLICATE_API_TOKEN`
3. Click "Run" button

### 🌐 Result:
Your app will be live at:
`https://ai-code-plagiarism-detector.yourusername.repl.co`

### 💡 What Happens When You Click "Run":
1. Installs Python dependencies
2. Installs Node.js dependencies  
3. Builds React frontend
4. Starts Flask server on port 5000
5. Serves both frontend and API from single URL

### 🔧 Architecture on Replit:
```
https://your-app.username.repl.co/
├── / (React Frontend)
├── /analysis (Code Analysis Page)
├── /comparison (Detailed Comparison)
├── /api/check (API: Basic similarity)
├── /api/analyze (API: Single code analysis)
└── /api/detailed-check (API: Detailed comparison)
```

### 💰 Cost:
- **Free**: Perfect for testing and demos
- **Hacker ($7/mo)**: Always-on, faster performance
- **Pro ($20/mo)**: Maximum speed and reliability

### ⚡ Performance Notes:
- First load may take 30-60 seconds (cold start)
- AI API calls work perfectly
- Frontend is served as static files (fast)
- App sleeps after 1 hour on free tier

### 🎉 That's It!
Your full-stack AI Code Plagiarism Detector is now deployed on Replit with:
- ✅ Beautiful React frontend
- ✅ Powerful Flask backend  
- ✅ Multiple AI model integration
- ✅ Advanced code analysis
- ✅ Professional deployment

**Ready to go live!** 🚀
