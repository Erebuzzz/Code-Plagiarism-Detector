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
    
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/:path*`,
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
