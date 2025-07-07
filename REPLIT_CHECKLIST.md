# ✅ Replit Deployment Checklist

## Pre-Deployment Setup

### 1. Prepare Your Code
- [ ] Code is working locally
- [ ] All API keys are ready
- [ ] Frontend builds successfully (`cd frontend && npm run build`)
- [ ] Backend starts without errors (`python main.py`)

### 2. Create Replit Account
- [ ] Sign up at [replit.com](https://replit.com)
- [ ] Verify email address

### 3. Setup Repository (Recommended)
- [ ] Push code to GitHub
- [ ] Make repository public (or have Replit Pro for private repos)

## Deployment Steps

### Step 1: Create New Repl
1. Go to [replit.com](https://replit.com)
2. Click "Create Repl"
3. Choose "Import from GitHub" 
4. Enter your repository URL: `https://github.com/yourusername/Code-Plagiarism-Detector`
5. Name your repl: `ai-code-plagiarism-detector`

### Step 2: Configure Environment Variables
1. In Replit, click the "Secrets" tab (🔒 icon)
2. Add these secrets:
   ```
   COHERE_API_KEY = your_cohere_api_key_here
   TOGETHER_API_KEY = your_together_ai_key_here  
   REPLICATE_API_TOKEN = your_replicate_token_here
   REPLIT_ENV = true
   ```

### Step 3: Setup Replit Configuration
Run this command in the Replit shell:
```bash
chmod +x replit_setup.sh && ./replit_setup.sh setup
```

### Step 4: Start Your App
1. Click the "Run" button in Replit
2. Wait for setup to complete (may take 2-3 minutes first time)
3. Your app will be available at the URL shown

## Expected Output
```
🚀 Starting AI Code Plagiarism Detector on Replit...
📦 Installing Python dependencies...
📦 Installing Node.js dependencies...
🔨 Building frontend...
✅ Frontend build copied to static directory
🌐 Starting Flask server on port 5000...
🔗 Your app will be available at: https://your-repl.your-username.repl.co
```

## Post-Deployment

### Test Your App
- [ ] Main page loads correctly
- [ ] Code similarity check works
- [ ] Single code analysis works  
- [ ] Detailed comparison works
- [ ] All AI APIs respond properly

### Share Your App
Your app will be live at: `https://ai-code-plagiarism-detector.yourusername.repl.co`

## Troubleshooting

### Common Issues:
1. **App sleeps after inactivity**: Normal on free tier
2. **Slow initial load**: First API calls may be slower
3. **Build errors**: Check that all dependencies are in requirements.txt and package.json
4. **API errors**: Verify your API keys in Secrets

### Getting Help:
- Check Replit console for error messages
- Verify environment variables are set correctly
- Test API keys separately if needed

## Upgrade Options

### Free Tier Limitations:
- App sleeps after 1 hour of inactivity
- Limited CPU/RAM
- Shared resources

### Paid Plans:
- **Hacker ($7/month)**: Always-on, more resources
- **Pro ($20/month)**: Maximum performance, private repos

Your AI Code Plagiarism Detector is now live! 🎉
