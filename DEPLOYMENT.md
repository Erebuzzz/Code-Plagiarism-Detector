# 🚀 Zeabur + Vercel Deployment Guide

## Architecture Overview

This project uses a **split deployment strategy** for optimal performance:

- **Backend (Python Flask)**: Deployed on **Zeabur** 
- **Frontend (Next.js React)**: Deployed on **Vercel**

## Why This Architecture?

✅ **Zeabur** excels at Python backend deployment  
✅ **Vercel** is perfect for Next.js frontends  
✅ Better performance than monolithic deployments  
✅ Easier scaling and maintenance  
✅ Both offer generous free tiers  

---

## 🏗️ Backend Deployment (Zeabur)

### 1. Prepare Backend Repository
Your backend files are ready:
- `main.py` - Flask application
- `requirements.txt` - Python dependencies  
- `Dockerfile` - Container configuration
- `zbpack.json` - Zeabur configuration
- `.env.example` - Environment variables template

### 2. Deploy to Zeabur

1. **Create Zeabur Account**
   - Go to [zeabur.com](https://zeabur.com)
   - Sign up with GitHub

2. **Create New Service**
   - Click "Create Service"
   - Select "Git Repository"
   - Connect your GitHub repository
   - Select this project

3. **Configure Environment Variables**
   Add these in Zeabur dashboard:
   ```
   COHERE_API_KEY=your_cohere_key
   TOGETHER_API_KEY=your_together_key  
   REPLICATE_API_TOKEN=your_replicate_token
   FLASK_ENV=production
   ZEABUR=true
   ```

4. **Deploy**
   - Zeabur will automatically detect Python and deploy
   - Your backend will be available at: `https://your-service.zeabur.app`

### 3. Test Backend
Visit `https://your-backend.zeabur.app/health` to verify deployment.

---

## 🌐 Frontend Deployment (Vercel)

### 1. Prepare Frontend
Navigate to your `frontend/` directory. The files are ready:
- `package.json` - Dependencies and scripts
- `next.config.js` - Vercel configuration  
- `.env.example` - Environment template

### 2. Deploy to Vercel

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project"
   - Import from GitHub
   - Select your repository
   - **Set Root Directory**: `frontend`

3. **Configure Environment Variables**
   Add in Vercel dashboard:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.zeabur.app
   ```

4. **Deploy**
   - Vercel will automatically build and deploy
   - Your frontend will be available at: `https://your-app.vercel.app`

---

## 🔗 Connect Frontend & Backend

### 1. Update CORS in Backend
In your backend `.env` file on Zeabur:
```
CORS_ORIGINS=https://your-frontend.vercel.app
```

### 2. Test Integration
1. Open your Vercel frontend URL
2. Try the code analysis features
3. Verify API calls work correctly

---

## 📋 Quick Deployment Checklist

### Backend (Zeabur)
- [ ] Repository connected to Zeabur
- [ ] Environment variables configured
- [ ] Health endpoint responding
- [ ] CORS configured for frontend domain

### Frontend (Vercel) 
- [ ] Repository connected to Vercel
- [ ] Root directory set to `frontend`
- [ ] `NEXT_PUBLIC_API_URL` environment variable set
- [ ] Build successful
- [ ] API calls working

---

## 🛠️ Environment Variables Reference

### Backend (Zeabur Dashboard)
```
COHERE_API_KEY=your_cohere_api_key
TOGETHER_API_KEY=your_together_ai_key  
REPLICATE_API_TOKEN=your_replicate_token
FLASK_ENV=production
ZEABUR=true
CORS_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (Vercel Dashboard)
```
NEXT_PUBLIC_API_URL=https://your-backend.zeabur.app
```

---

## 🎯 Benefits of This Setup

### Performance
- **CDN**: Vercel provides global CDN for frontend
- **Edge Functions**: Optimized API calls  
- **Python Optimization**: Zeabur optimized for Python apps

### Scalability  
- **Independent Scaling**: Scale frontend and backend separately
- **Resource Optimization**: Each service uses optimal resources
- **Cost Effective**: Pay only for what you use

### Development
- **Separate Deployments**: Update frontend/backend independently  
- **Better Organization**: Clear separation of concerns
- **Team Collaboration**: Frontend and backend teams can work independently

---

## 🔍 Troubleshooting

### Backend Issues
- **500 Errors**: Check Zeabur logs for Python errors
- **API Not Responding**: Verify environment variables set
- **CORS Errors**: Ensure frontend URL added to CORS_ORIGINS

### Frontend Issues  
- **Build Failures**: Check package.json and dependencies
- **API Errors**: Verify NEXT_PUBLIC_API_URL is correct
- **404 on Routes**: Ensure Vercel routing configured

### Integration Issues
- **CORS Blocked**: Update backend CORS configuration
- **API Not Found**: Verify backend URL in frontend env vars
- **Environment Variables**: Check both dashboards for correct values

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ **Fast Backend**: Python Flask on Zeabur
- ✅ **Lightning Frontend**: Next.js on Vercel  
- ✅ **Global CDN**: Optimized worldwide delivery
- ✅ **Auto-scaling**: Handle traffic spikes automatically
- ✅ **Professional URLs**: Custom domains supported

**Your AI Code Plagiarism Detector is now live with enterprise-grade infrastructure!**
