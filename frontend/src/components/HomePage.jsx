/**
 * HomePage component - Main landing page with featured products
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productsAPI, categoriesAPI } from '../services/api';
import { getProductImageUrl, getImageUrl } from '../utils/imageUtils';
import './HomePage.css';

const HomePage = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [hotProducts, setHotProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [featuredRes, hotRes, categoriesRes] = await Promise.all([
        productsAPI.getAll({ featured: 'true', page_size: 8 }),
        productsAPI.getAll({ hot: 'true', page_size: 4 }),
        categoriesAPI.getAll(),
      ]);
      
      setFeaturedProducts(featuredRes.data.results || []);
      setHotProducts(hotRes.data.results || []);
      setCategories(categoriesRes.data || []);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };


  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="home-page">
      {/* Hero Slider */}
      <section className="hero-slider">
        <div className="hero-slide">
          <div className="hero-content">
            <span className="hero-subtitle">Women Collection 2024</span>
            <h2 className="hero-title">NEW SEASON</h2>
            <Link to="/product/" className="btn-shop">Shop Now</Link>
          </div>
        </div>
      </section>

      {/* Categories Banner */}
      {categories.length > 0 && (
        <section className="categories-banner">
          <div className="container">
            <div className="banner-grid">
              {categories.slice(0, 3).map(category => (
                <div key={category.id} className="banner-item">
                  <div className="banner-image">
                    {category.image ? (
                      <img 
                        src={getImageUrl(category.image)} 
                        alt={category.name}
                        onError={(e) => {
                          e.target.style.display = 'none';
                          if (!e.target.nextSibling) {
                            const placeholder = document.createElement('div');
                            placeholder.className = 'banner-placeholder';
                            placeholder.textContent = category.name;
                            e.target.parentElement.appendChild(placeholder);
                          }
                        }}
                      />
                    ) : (
                      <div className="banner-placeholder">{category.name}</div>
                    )}
                  </div>
                  <div className="banner-overlay">
                    <h3>{category.name}</h3>
                    <Link to={`/product/?category=${category.slug}`}>Shop Now</Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Hot Products */}
      {hotProducts.length > 0 && (
        <section className="hot-products">
          <div className="container">
            <h2 className="section-title">Hot Products</h2>
            <div className="products-grid">
              {hotProducts.map(product => (
                <div key={product.id} className="product-card">
                  <div className="product-image-wrapper">
                    {getProductImageUrl(product) ? (
                      <img 
                        src={getProductImageUrl(product)} 
                        alt={product.name}
                        className="product-image"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          const placeholder = e.target.nextSibling;
                          if (placeholder) {
                            placeholder.style.display = 'flex';
                          }
                        }}
                      />
                    ) : null}
                    <div 
                      className="product-image-placeholder"
                      style={{display: getProductImageUrl(product) ? 'none' : 'flex'}}
                    >
                      No Image
                    </div>
                    {product.is_hot && <span className="badge hot">HOT</span>}
                    {product.discount_percentage > 0 && (
                      <span className="badge discount">-{product.discount_percentage}%</span>
                    )}
                  </div>
                  <div className="product-info">
                    <h3 className="product-name">{product.name}</h3>
                    <div className="product-price">
                      <span className="price">${product.price}</span>
                      {product.compare_at_price && (
                        <span className="compare-price">${product.compare_at_price}</span>
                      )}
                    </div>
                    <Link to={`/product/${product.id}/`} className="btn-view">View Details</Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Featured Products */}
      {featuredProducts.length > 0 && (
        <section className="featured-products">
          <div className="container">
            <h2 className="section-title">Featured Products</h2>
            <div className="products-grid">
              {featuredProducts.map(product => (
                <div key={product.id} className="product-card">
                  <div className="product-image-wrapper">
                    {getProductImageUrl(product) ? (
                      <img 
                        src={getProductImageUrl(product)} 
                        alt={product.name}
                        className="product-image"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          const placeholder = e.target.nextSibling;
                          if (placeholder) {
                            placeholder.style.display = 'flex';
                          }
                        }}
                      />
                    ) : null}
                    <div 
                      className="product-image-placeholder"
                      style={{display: getProductImageUrl(product) ? 'none' : 'flex'}}
                    >
                      No Image
                    </div>
                    {product.is_featured && <span className="badge featured">Featured</span>}
                    {product.discount_percentage > 0 && (
                      <span className="badge discount">-{product.discount_percentage}%</span>
                    )}
                  </div>
                  <div className="product-info">
                    <h3 className="product-name">{product.name}</h3>
                    <div className="product-price">
                      <span className="price">${product.price}</span>
                      {product.compare_at_price && (
                        <span className="compare-price">${product.compare_at_price}</span>
                      )}
                    </div>
                    <Link to={`/product/${product.id}/`} className="btn-view">View Details</Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default HomePage;

