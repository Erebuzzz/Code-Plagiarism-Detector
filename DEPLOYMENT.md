# 🚀 Glitch Deployment Guide - AI Code Plagiarism Detector

## Deploy to Glitch (Backend + Frontend Combined) - FREE!

Glitch offers free hosting that's perfect for your AI Code Plagiarism Detector. No credit card required!

### 📋 Prerequisites
- Glitch account (free at [glitch.com](https://glitch.com))
- Your API keys (Cohere, Together.ai, Replicate)
- GitHub repository (optional but recommended)

### 🎯 Why Glitch?
- ✅ **Completely FREE** - No credit card needed
- ✅ Automatic HTTPS
- ✅ Built-in code editor
- ✅ Easy environment management
- ✅ Auto-deployment on file changes
- ✅ Great community and support
- ✅ Perfect for demos and portfolios

### 🔧 Deployment Steps

#### 1. Create New Glitch Project
1. Go to [glitch.com](https://glitch.com)
2. Click "New Project"
3. Choose "Import from GitHub" (recommended) or "hello-express"
4. Name it: `ai-code-plagiarism-detector`

#### 2. Import Your Code
**Option A: From GitHub (Recommended)**
1. Click "Tools" → "Import and Export" → "Import from GitHub"
2. Enter your repository URL: `https://github.com/yourusername/Code-Plagiarism-Detector`
3. Glitch will import everything automatically

**Option B: Manual Upload**
1. Delete default files
2. Upload/copy all your project files
3. Maintain the same directory structure

#### 3. Configure Environment Variables
1. In Glitch, click ".env" file in the sidebar
2. Add these environment variables:
   ```
   COHERE_API_KEY=your_cohere_key_here
   TOGETHER_API_KEY=your_together_ai_key_here
   REPLICATE_API_TOKEN=your_replicate_token_here
   GLITCH_ENV=true
   NODE_ENV=production
   ```

#### 4. Automatic Setup
Glitch will automatically:
- Install Node.js dependencies from `package.json`
- Install Python dependencies from `requirements.txt`
- Build the frontend automatically
- Start the application via `server.js`

#### 5. Manual Setup (if needed)
If automatic setup fails, use the terminal:
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Build frontend
npm run build

# Start app
npm start
```

#### 4. Project Structure for Glitch
```
/
├── server.js              # Main server file (we'll create this)
├── main.py                # Flask backend
├── package.json           # Node.js dependencies and scripts
├── requirements.txt       # Python dependencies
├── frontend/              # Next.js frontend
├── public/                # Static files served by Express
├── start.sh              # Startup script
└── glitch.json           # Glitch configuration
```

### 💡 How It Works on Glitch
1. **Express.js Proxy**: Node.js Express serves frontend and proxies API calls to Flask
2. **Dual Process**: Flask backend + Express frontend server
3. **Build Process**: Frontend builds during startup
4. **Single URL**: Everything accessible from one Glitch URL

### 🚀 Architecture
```
https://your-app.glitch.me/
├── / (React Frontend via Express)
├── /analysis (Code Analysis Page)
├── /comparison (Detailed Comparison)
├── /api/check (Proxied to Flask backend)
├── /api/analyze (Proxied to Flask backend)
└── /api/detailed-check (Proxied to Flask backend)
```

### 🌐 Your Live App
Once deployed, your app will be available at:
`https://ai-code-plagiarism-detector.glitch.me`

### 💰 Cost
- **100% FREE** - No hidden costs
- **Always-on**: App sleeps after 5 minutes of inactivity
- **Resource limits**: 1GB storage, 4000 requests/hour
- **Perfect for**: Demos, portfolios, learning projects

### ⚡ Performance on Free Tier
- **Boot time**: ~10-15 seconds from sleep
- **Memory**: 512MB RAM (sufficient for your app)
- **Storage**: 1GB (more than enough)
- **Bandwidth**: Unlimited for reasonable use

### 🎉 Benefits of Glitch
- **No credit card required**
- **Instant deployment**
- **Built-in terminal**
- **Live code editing**
- **Community showcase**
- **Educational friendly**
- **Great for MVPs and demos**

### 📝 Next Steps
See the detailed setup files and configuration coming next!

Need help? Glitch has excellent documentation and community support!
