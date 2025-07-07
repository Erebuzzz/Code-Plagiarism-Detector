const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Start Flask backend
let flaskProcess;
const startFlaskBackend = () => {
  console.log('🐍 Starting Flask backend...');
  flaskProcess = spawn('python', ['main.py'], {
    env: { ...process.env, PORT: '5000' },
    stdio: 'inherit'
  });

  flaskProcess.on('error', (err) => {
    console.error('❌ Flask backend error:', err);
  });

  flaskProcess.on('exit', (code) => {
    console.log(`🐍 Flask backend exited with code ${code}`);
    if (code !== 0) {
      console.log('🔄 Restarting Flask backend...');
      setTimeout(startFlaskBackend, 5000);
    }
  });
};

// Wait for Flask to be ready
const waitForFlask = async () => {
  const http = require('http');
  return new Promise((resolve) => {
    const checkFlask = () => {
      const req = http.get('http://localhost:5000/health', (res) => {
        if (res.statusCode === 200) {
          console.log('✅ Flask backend is ready!');
          resolve();
        } else {
          setTimeout(checkFlask, 1000);
        }
      });
      req.on('error', () => {
        setTimeout(checkFlask, 1000);
      });
      req.setTimeout(1000, () => {
        req.destroy();
        setTimeout(checkFlask, 1000);
      });
    };
    checkFlask();
  });
};

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Proxy API calls to Flask backend
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:5000',
  changeOrigin: true,
  pathRewrite: {
    '^/api': '', // Remove /api prefix when forwarding to Flask
  },
  onError: (err, req, res) => {
    console.error('❌ Proxy error:', err.message);
    res.status(500).json({ 
      error: 'Backend service unavailable',
      message: 'The AI analysis service is starting up. Please try again in a moment.'
    });
  }
}));

// Serve React frontend
app.get('*', (req, res) => {
  const indexPath = path.join(__dirname, 'public', 'index.html');
  
  if (fs.existsSync(indexPath)) {
    res.sendFile(indexPath);
  } else {
    // Fallback response if frontend not built yet
    res.send(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>AI Code Plagiarism Detector</title>
          <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 600px; margin: 0 auto; }
            .loading { color: #666; }
          </style>
        </head>
        <body>
          <div class="container">
            <h1>🚀 AI Code Plagiarism Detector</h1>
            <p class="loading">Setting up your application...</p>
            <p>Please wait a moment while we prepare everything for you.</p>
            <p><a href="/api/health">Check Backend Status</a></p>
          </div>
        </body>
      </html>
    `);
  }
});

// Initialize the application
const init = async () => {
  console.log('🚀 Starting AI Code Plagiarism Detector on Glitch...');
  console.log('================================================');
  
  // Check if frontend is built
  const frontendBuilt = fs.existsSync(path.join(__dirname, 'public', 'index.html'));
  
  if (!frontendBuilt) {
    console.log('🔧 Frontend not built yet, building now...');
    await buildFrontend();
  }
  
  // Start Flask backend
  startFlaskBackend();
  
  // Wait for Flask to be ready
  await waitForFlask();
  
  // Start Express server
  app.listen(PORT, () => {
    console.log(`🌐 Express server running on port ${PORT}`);
    console.log(`📡 Flask backend running on port 5000`);
    if (process.env.PROJECT_DOMAIN) {
      console.log(`✅ App ready at: https://${process.env.PROJECT_DOMAIN}.glitch.me`);
    } else {
      console.log(`✅ App ready at: http://localhost:${PORT}`);
    }
    console.log('🎉 AI Code Plagiarism Detector is live!');
  });
};

// Build frontend if needed
const buildFrontend = () => {
  return new Promise((resolve, reject) => {
    console.log('📦 Building frontend...');
    
    const buildProcess = exec('cd frontend && npm ci && npm run build && npm run export && cd .. && mkdir -p public && cp -r frontend/out/* public/', 
      (error, stdout, stderr) => {
        if (error) {
          console.error('❌ Frontend build failed:', error);
          reject(error);
        } else {
          console.log('✅ Frontend built successfully');
          resolve();
        }
      }
    );
    
    buildProcess.stdout?.on('data', (data) => {
      console.log('📦 Build:', data.toString().trim());
    });
    
    buildProcess.stderr?.on('data', (data) => {
      console.error('📦 Build error:', data.toString().trim());
    });
  });
};

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('👋 Shutting down gracefully...');
  if (flaskProcess) {
    flaskProcess.kill();
  }
  process.exit(0);
});

// Start the application
init().catch(console.error);
