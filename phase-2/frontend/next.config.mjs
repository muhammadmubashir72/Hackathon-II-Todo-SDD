/** @type {import('next').NextConfig} */
const nextConfig = {
  // Add environment variable for the backend API
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://mubashirsaeedi-todo-api.hf.space/',
  },
};

export default nextConfig;
