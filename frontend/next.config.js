/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/check',
        destination: 'http://localhost:8000/check',
      },
      {
        source: '/analyze',
        destination: 'http://localhost:8000/analyze',
      },
      {
        source: '/detailed-check',
        destination: 'http://localhost:8000/detailed-check',
      },
    ]
  },
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
