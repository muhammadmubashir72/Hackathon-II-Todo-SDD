/** @type {import('next').NextConfig} */
const nextConfig = {
  // Server Actions are enabled by default in Next.js 14.2+
  // No need to explicitly enable them in experimental

  // Add environment variable for the backend API
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://mubashirsaeedi-todo-api.hf.space/',
  },
};

export default nextConfig;
