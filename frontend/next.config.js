/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables for API backend
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
  
  // For Vercel deployment with Zeabur backend
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
    
    // Ensure the URL has proper protocol
    let formattedApiUrl = apiUrl;
    if (!apiUrl.startsWith('http://') && !apiUrl.startsWith('https://')) {
      formattedApiUrl = `https://${apiUrl}`;
    }
    
    console.log('API URL for rewrites:', formattedApiUrl);
    
    return [
      {
        source: '/api/:path*',
        destination: `${formattedApiUrl}/:path*`,
      },
    ]
  },
  
  // Vercel deployment configuration
  images: {
    unoptimized: true
  },
  
  eslint: {
    ignoreDuringBuilds: true,
  },
  
  // Optimize for production
  swcMinify: true,
  poweredByHeader: false,
}

module.exports = nextConfig
