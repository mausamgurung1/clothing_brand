/**
 * API service for communicating with Django backend
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import axios from 'axios';
import { API_BASE_URL, getApiUrl } from '../config';

// Use proxy in development, full URL in production
const apiBaseUrl = import.meta.env.DEV ? '/api' : `${API_BASE_URL}/api`;

const api = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Products API
export const productsAPI = {
  getAll: (params = {}) => api.get('/products/', { params }),
  getById: (id) => api.get(`/products/${id}/`),
  create: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (key === 'main_image' && data[key] instanceof File) {
        formData.append(key, data[key]);
      } else if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.post('/products/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  update: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (key === 'main_image' && data[key] instanceof File) {
        formData.append(key, data[key]);
      } else if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.patch(`/products/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  delete: (id) => api.delete(`/products/${id}/`),
  uploadImage: (id, imageFile, altText = '', order = 0, isPrimary = false) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('alt_text', altText);
    formData.append('order', order);
    formData.append('is_primary', isPrimary);
    return api.post(`/products/${id}/upload_image/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  deleteImage: (id, imageId) => api.delete(`/products/${id}/delete_image/`, {
    data: { image_id: imageId },
  }),
};

// Categories API
export const categoriesAPI = {
  getAll: () => api.get('/categories/'),
  getBySlug: (slug) => api.get(`/categories/${slug}/`),
  create: (data) => api.post('/categories/', data),
  update: (slug, data) => api.patch(`/categories/${slug}/`, data),
  delete: (slug) => api.delete(`/categories/${slug}/`),
};

// Auth API
export const authAPI = {
  login: (username, password) => api.post('/auth/login/', { username, password }),
  logout: () => api.post('/auth/logout/'),
  checkAuth: () => api.get('/auth/check/'),
};

// Set auth token for authenticated requests
export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Token ${token}`;
    localStorage.setItem('auth_token', token);
  } else {
    delete api.defaults.headers.common['Authorization'];
    localStorage.removeItem('auth_token');
  }
};

// Load token from localStorage on init
const savedToken = localStorage.getItem('auth_token');
if (savedToken) {
  setAuthToken(savedToken);
}

export default api;

