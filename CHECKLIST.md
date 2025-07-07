# ✅ Glitch Deployment Checklist

## Pre-Deployment Checklist

### 📋 Required Files
- [ ] `server.js` - Express server with Flask proxy
- [ ] `main.py` - Flask backend with health endpoint
- [ ] `package.json` - Node.js dependencies and scripts
- [ ] `requirements.txt` - Python dependencies
- [ ] `glitch.json` - Glitch configuration
- [ ] `frontend/` - Next.js application folder
- [ ] `.env.example` - Environment variables template

### 🔑 Environment Variables
- [ ] `COHERE_API_KEY` - Your Cohere API key
- [ ] `TOGETHER_API_KEY` - Your Together.ai API key
- [ ] `REPLICATE_API_TOKEN` - Your Replicate token
- [ ] `GLITCH_ENV=true` - Glitch environment flag
- [ ] `NODE_ENV=production` - Production mode

### 🛠️ Dependencies Check
- [ ] Express.js in `package.json`
- [ ] http-proxy-middleware in `package.json`
- [ ] All Python packages in `requirements.txt`
- [ ] Frontend dependencies in `frontend/package.json`

## Deployment Steps

### 1. Glitch Project Setup
- [ ] Created Glitch account
- [ ] Imported project from GitHub OR uploaded files manually
- [ ] Project name set (e.g., `ai-code-plagiarism-detector`)

### 2. Environment Configuration
- [ ] Opened `.env` file in Glitch
- [ ] Added all required API keys
- [ ] Set `GLITCH_ENV=true`
- [ ] Set `NODE_ENV=production`

### 3. Dependencies Installation
- [ ] Node.js dependencies installed automatically
- [ ] Python dependencies installed via `pip install -r requirements.txt`
- [ ] Frontend dependencies installed in `frontend/` folder

### 4. Frontend Build
- [ ] Ran `npm run build` in Glitch terminal
- [ ] `public/` folder created with built files
- [ ] `public/index.html` exists and is accessible

### 5. Backend Configuration
- [ ] Flask app configured for port 5000
- [ ] Health endpoint `/health` working
- [ ] CORS enabled for frontend integration
- [ ] All API endpoints functional

## Post-Deployment Testing

### 🌐 Frontend Testing
- [ ] App loads at `https://your-project.glitch.me`
- [ ] Home page displays correctly
- [ ] Navigation between pages works
- [ ] UI components render properly
- [ ] Responsive design works on mobile

### 🔌 Backend Testing
- [ ] Health check: `https://your-project.glitch.me/api/health`
- [ ] Can submit code for analysis
- [ ] Plagiarism detection working
- [ ] AI detection working
- [ ] Error handling working

### 🚀 End-to-End Testing
- [ ] Upload code samples
- [ ] Plagiarism analysis completes
- [ ] Results display correctly
- [ ] Comparison feature works
- [ ] All features functional

## Troubleshooting Checklist

### 🔧 Common Issues
- [ ] App not starting → Check `.env` variables
- [ ] 500 errors → Check Python dependencies
- [ ] Frontend not loading → Run `npm run build`
- [ ] API errors → Verify API keys
- [ ] Slow startup → Normal for Glitch free tier

### 📊 Performance Check
- [ ] Initial load time acceptable (~10-15s from sleep)
- [ ] API responses under 30 seconds
- [ ] Memory usage within limits
- [ ] No continuous errors in logs

### 🔍 Monitoring
- [ ] Check Glitch logs for errors
- [ ] Monitor API key usage
- [ ] Verify all endpoints responding
- [ ] Test from different devices/browsers

## Success Criteria

### ✅ Deployment Successful When:
- [ ] App accessible at public URL
- [ ] All features working as expected
- [ ] Frontend and backend communicating
- [ ] API integrations functioning
- [ ] No critical errors in logs
- [ ] Responsive across devices

### 🎯 Performance Targets
- [ ] App wakes from sleep in <20 seconds
- [ ] API responses in <30 seconds
- [ ] Frontend loads in <10 seconds (after wake)
- [ ] No memory limit exceeded warnings

## Final Steps

### 📝 Documentation
- [ ] Update README with live demo URL
- [ ] Document any Glitch-specific configurations
- [ ] Update deployment guides if needed

### 🚀 Go Live
- [ ] Share live demo URL
- [ ] Test with real users
- [ ] Monitor for any issues
- [ ] Celebrate successful deployment! 🎉

---

## Quick Commands Reference

```bash
# In Glitch Terminal
npm install              # Install Node.js dependencies
pip install -r requirements.txt  # Install Python dependencies
npm run build           # Build frontend
npm start               # Start the application
refresh                 # Restart the Glitch project
logs                    # View application logs
```

## Environment Variables Template
```
COHERE_API_KEY=your_key_here
TOGETHER_API_KEY=your_key_here
REPLICATE_API_TOKEN=your_token_here
GLITCH_ENV=true
NODE_ENV=production
```

**Happy Deploying! 🚀**
