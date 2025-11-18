/**
 * Dynamic configuration for API and media URLs
 * Uses environment variables with fallbacks
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

// Get API base URL from environment or use current origin (dynamic)
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL 
  || (typeof window !== 'undefined' ? window.location.origin : '');

// Get media base URL from environment or use API base URL
export const MEDIA_BASE_URL = import.meta.env.VITE_MEDIA_BASE_URL 
  || API_BASE_URL;

// API endpoints
export const API_ENDPOINTS = {
  PRODUCTS: '/api/products/',
  CATEGORIES: '/api/categories/',
  BLOG: '/api/blog/',
};

// Build full API URL
export const getApiUrl = (endpoint) => {
  if (endpoint.startsWith('http')) {
    return endpoint;
  }
  if (endpoint.startsWith('/api')) {
    return `${API_BASE_URL}${endpoint}`;
  }
  return `${API_BASE_URL}/api${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
};

// Build full media URL (dynamic)
export const getMediaUrl = (path) => {
  if (!path) return null;
  
  // If already absolute URL, return as is
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  
  // If path starts with /media/ or /static/, use MEDIA_BASE_URL
  if (path.startsWith('/media/') || path.startsWith('/static/')) {
    // If MEDIA_BASE_URL is empty, use current origin
    const base = MEDIA_BASE_URL || (typeof window !== 'undefined' ? window.location.origin : '');
    return base ? `${base}${path}` : path;
  }
  
  // If path starts with /, use MEDIA_BASE_URL
  if (path.startsWith('/')) {
    const base = MEDIA_BASE_URL || (typeof window !== 'undefined' ? window.location.origin : '');
    return base ? `${base}${path}` : path;
  }
  
  // Otherwise, assume it's a media file
  const base = MEDIA_BASE_URL || (typeof window !== 'undefined' ? window.location.origin : '');
  return base ? `${base}/media/${path}` : `/media/${path}`;
};

