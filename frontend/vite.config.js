/**
 * Vite configuration for Baabuu Clothing
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Get API base URL from environment (fully dynamic)
const getApiBaseUrl = () => {
  // Priority 1: Use environment variable (required in production)
  if (process.env.VITE_API_BASE_URL) {
    return process.env.VITE_API_BASE_URL
  }
  
  // Priority 2: In production, env var is required
  if (process.env.NODE_ENV === 'production') {
    throw new Error(
      'VITE_API_BASE_URL must be set in production. ' +
      'Please set it in your environment variables or .env file.'
    )
  }
  
  // Priority 3: Development fallback (only if not in production)
  // This is a convenience for local development only
  const devPort = process.env.DJANGO_PORT || '8000'
  return `http://localhost:${devPort}`
}

const apiBaseUrl = getApiBaseUrl()

export default defineConfig({
  plugins: [react()],
  server: {
    port: parseInt(process.env.VITE_PORT || '5173', 10),
    proxy: {
      '/api': {
        target: apiBaseUrl,
        changeOrigin: true,
        secure: false,
      },
      '/media': {
        target: apiBaseUrl,
        changeOrigin: true,
        secure: false,
      },
      '/static': {
        target: apiBaseUrl,
        changeOrigin: true,
        secure: false,
      },
    },
  },
  // Build configuration
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})

