/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // For Replit deployment - API calls go to same origin
  async rewrites() {
    return [
      {
        source: '/api/check',
        destination: '/check',
      },
      {
        source: '/api/analyze', 
        destination: '/analyze',
      },
      {
        source: '/api/detailed-check',
        destination: '/detailed-check',
      },
    ]
  },
  
  // Static export for Replit deployment
  output: 'export',
  trailingSlash: true,
  
  images: {
    unoptimized: true
  },
  
  // Disable server-side features for static export
  eslint: {
    ignoreDuringBuilds: true,
  },
}

module.exports = nextConfig
