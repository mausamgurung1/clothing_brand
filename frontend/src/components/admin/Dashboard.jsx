/**
 * Admin Dashboard - Overview and statistics
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productsAPI, categoriesAPI } from '../../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalCategories: 0,
    featuredProducts: 0,
    hotProducts: 0,
    lowStock: 0,
    outOfStock: 0,
  });
  const [loading, setLoading] = useState(true);
  const [recentProducts, setRecentProducts] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [productsRes, categoriesRes] = await Promise.all([
        productsAPI.getAll({ page_size: 1000 }),
        categoriesAPI.getAll(),
      ]);

      const products = productsRes.data.results || [];
      const categories = categoriesRes.data || [];

      // Calculate statistics
      const featuredProducts = products.filter(p => p.is_featured).length;
      const hotProducts = products.filter(p => p.is_hot).length;
      const lowStock = products.filter(p => p.stock_quantity < 10 && p.stock_quantity > 0).length;
      const outOfStock = products.filter(p => p.stock_quantity === 0).length;

      setStats({
        totalProducts: products.length,
        totalCategories: categories.length,
        featuredProducts,
        hotProducts,
        lowStock,
        outOfStock,
      });

      // Get recent products (last 5)
      setRecentProducts(products.slice(0, 5));
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p className="dashboard-subtitle">Welcome to Baabuu Clothing Admin Panel</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon products">📦</div>
          <div className="stat-content">
            <h3>{stats.totalProducts}</h3>
            <p>Total Products</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon categories">📁</div>
          <div className="stat-content">
            <h3>{stats.totalCategories}</h3>
            <p>Categories</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon featured">⭐</div>
          <div className="stat-content">
            <h3>{stats.featuredProducts}</h3>
            <p>Featured Products</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon hot">🔥</div>
          <div className="stat-content">
            <h3>{stats.hotProducts}</h3>
            <p>Hot Products</p>
          </div>
        </div>

        <div className="stat-card warning">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>{stats.lowStock}</h3>
            <p>Low Stock</p>
          </div>
        </div>

        <div className="stat-card danger">
          <div className="stat-icon">❌</div>
          <div className="stat-content">
            <h3>{stats.outOfStock}</h3>
            <p>Out of Stock</p>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <Link to="/admin/products" className="quick-action-card">
          <div className="quick-action-icon">📦</div>
          <div className="quick-action-content">
            <h3>Manage Products</h3>
            <p>Add, edit, or delete products</p>
          </div>
        </Link>
        <Link to="/admin/categories" className="quick-action-card">
          <div className="quick-action-icon">📁</div>
          <div className="quick-action-content">
            <h3>Manage Categories</h3>
            <p>Organize your product categories</p>
          </div>
        </Link>
        <Link to="/admin/analytics" className="quick-action-card">
          <div className="quick-action-icon">📊</div>
          <div className="quick-action-content">
            <h3>View Analytics</h3>
            <p>See detailed statistics</p>
          </div>
        </Link>
        <Link to="/admin/settings" className="quick-action-card">
          <div className="quick-action-icon">⚙️</div>
          <div className="quick-action-content">
            <h3>Settings</h3>
            <p>Configure your store</p>
          </div>
        </Link>
      </div>

      <div className="dashboard-sections">
        <div className="dashboard-section">
          <h2>Recent Products</h2>
          <div className="recent-products">
            {recentProducts.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Image</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Stock</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {recentProducts.map(product => (
                    <tr key={product.id}>
                      <td>
                        <div className="product-thumb">
                          {product.main_image_url ? (
                            <img src={product.main_image_url} alt={product.name} />
                          ) : (
                            <span>No Image</span>
                          )}
                        </div>
                      </td>
                      <td>{product.name}</td>
                      <td>${product.price}</td>
                      <td>
                        <span className={`stock-badge ${product.stock_quantity === 0 ? 'out' : product.stock_quantity < 10 ? 'low' : 'ok'}`}>
                          {product.stock_quantity}
                        </span>
                      </td>
                      <td>
                        <span className={`status-badge ${product.is_available ? 'active' : 'inactive'}`}>
                          {product.is_available ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="no-data">No products yet. Create your first product!</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

