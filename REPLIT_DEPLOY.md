# 🚀 Replit Deployment Guide - AI Code Plagiarism Detector

## Deploy to Replit (Backend + Frontend Combined)

This guide will help you deploy your full-stack AI Code Plagiarism Detector on Replit in a single container.

### 📋 Prerequisites
- Replit account (free tier works)
- Your API keys (Cohere, Together.ai, Replicate)
- GitHub repository (optional but recommended)

### 🔧 Deployment Steps

#### 1. Create New Repl
1. Go to [replit.com](https://replit.com)
2. Click "Create Repl"
3. Choose "Python" template
4. Name it: `ai-code-plagiarism-detector`

#### 2. Import Your Code
**Option A: From GitHub (Recommended)**
1. Click "Import from GitHub"
2. Enter your repository URL
3. Replit will automatically import everything

**Option B: Manual Upload**
1. Upload all files from your project
2. Maintain the same directory structure

#### 3. Configure Environment Variables
1. In Replit, go to "Secrets" tab (lock icon)
2. Add these environment variables:
   ```
   COHERE_API_KEY=your_cohere_key_here
   TOGETHER_API_KEY=your_together_ai_key_here
   REPLICATE_API_TOKEN=your_replicate_token_here
   REPLIT_ENV=true
   ```

#### 4. Install Dependencies
Replit will automatically detect `requirements.txt` and install Python packages.
For frontend dependencies, we'll install them via the startup script.

#### 5. Project Structure for Replit
```
/
├── main.py                 # Flask backend (already exists)
├── requirements.txt        # Python dependencies
├── .replit                 # Replit configuration
├── replit.nix             # Nix configuration for Node.js
├── pyproject.toml         # Python project config
├── frontend/              # Next.js frontend
├── static/                # Static files served by Flask
└── start.sh               # Startup script
```

### 🎯 Replit Advantages
- ✅ Free hosting (with limitations)
- ✅ Automatic HTTPS
- ✅ Built-in code editor
- ✅ Easy environment management
- ✅ Auto-deployment on file changes
- ✅ Shared development environment

### 💡 How It Works on Replit
1. **Unified Server**: Flask serves both API and frontend
2. **Build Process**: Frontend builds during startup
3. **Single Port**: Everything runs on one port (5000)
4. **Auto-scaling**: Replit handles scaling automatically

### 🚀 Go Live!
Once configured, your app will be available at:
`https://ai-code-plagiarism-detector.username.repl.co`

### 💰 Cost
- **Free Tier**: 500MB RAM, always-on for limited hours
- **Hacker Plan**: $7/month for more resources and always-on
- **Pro Plan**: $20/month for maximum performance

### ⚠️ Limitations on Free Tier
- App sleeps after inactivity
- Limited CPU/RAM
- Shared resources
- May be slower for AI API calls

Need help with the setup? The configuration files are ready to use!
