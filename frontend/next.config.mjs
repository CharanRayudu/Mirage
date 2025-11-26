/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // In a Docker environment, the frontend talks to the backend via its service name.
        destination: 'http://127.0.0.1:8000/:path*',
      },
    ]
  },
};

export default nextConfig;
