/**
 * Utility functions for handling image URLs from backend
 * Uses dynamic configuration
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import { getMediaUrl } from '../config';

export const getImageUrl = (imageUrl) => {
  return getMediaUrl(imageUrl);
};

export const getProductImageUrl = (product) => {
  // Try main_image_url first
  if (product?.main_image_url) {
    return getMediaUrl(product.main_image_url);
  }
  
  // Fallback to image_url
  if (product?.image_url) {
    return getMediaUrl(product.image_url);
  }
  
  // Try main_image if it's a file object
  if (product?.main_image) {
    return getMediaUrl(product.main_image);
  }
  
  return null;
};

