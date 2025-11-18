/**
 * Analytics Dashboard - Advanced statistics and charts
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState, useEffect } from 'react';
import { productsAPI, categoriesAPI } from '../../services/api';
import './Analytics.css';

const Analytics = () => {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalCategories: 0,
    featuredProducts: 0,
    hotProducts: 0,
    lowStock: 0,
    outOfStock: 0,
    totalValue: 0,
    averagePrice: 0,
    totalStock: 0,
  });
  const [categoryStats, setCategoryStats] = useState([]);
  const [priceRangeStats, setPriceRangeStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
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
      
      const totalValue = products.reduce((sum, p) => sum + (p.price * p.stock_quantity), 0);
      const totalStock = products.reduce((sum, p) => sum + p.stock_quantity, 0);
      const averagePrice = products.length > 0 
        ? products.reduce((sum, p) => sum + p.price, 0) / products.length 
        : 0;

      // Category statistics
      const catStats = categories.map(cat => {
        const catProducts = products.filter(p => p.category?.id === cat.id);
        return {
          name: cat.name,
          count: catProducts.length,
          totalValue: catProducts.reduce((sum, p) => sum + (p.price * p.stock_quantity), 0),
        };
      }).sort((a, b) => b.count - a.count);

      // Price range statistics
      const priceRanges = [
        { label: '$0 - $50', min: 0, max: 50 },
        { label: '$50 - $100', min: 50, max: 100 },
        { label: '$100 - $200', min: 100, max: 200 },
        { label: '$200+', min: 200, max: Infinity },
      ];

      const priceStats = priceRanges.map(range => ({
        label: range.label,
        count: products.filter(p => p.price >= range.min && p.price < range.max).length,
      }));

      setStats({
        totalProducts: products.length,
        totalCategories: categories.length,
        featuredProducts,
        hotProducts,
        lowStock,
        outOfStock,
        totalValue,
        averagePrice,
        totalStock,
      });

      setCategoryStats(catStats);
      setPriceRangeStats(priceStats);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics-loading">Loading analytics...</div>;
  }

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1>Analytics Dashboard</h1>
        <p>Comprehensive insights into your store</p>
      </div>

      <div className="analytics-grid">
        <div className="stat-card primary">
          <div className="stat-icon">📦</div>
          <div className="stat-content">
            <h3>{stats.totalProducts}</h3>
            <p>Total Products</p>
          </div>
        </div>

        <div className="stat-card success">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>${stats.totalValue.toLocaleString()}</h3>
            <p>Total Inventory Value</p>
          </div>
        </div>

        <div className="stat-card info">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>${stats.averagePrice.toFixed(2)}</h3>
            <p>Average Price</p>
          </div>
        </div>

        <div className="stat-card warning">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>{stats.lowStock}</h3>
            <p>Low Stock Items</p>
          </div>
        </div>

        <div className="stat-card danger">
          <div className="stat-icon">❌</div>
          <div className="stat-content">
            <h3>{stats.outOfStock}</h3>
            <p>Out of Stock</p>
          </div>
        </div>

        <div className="stat-card secondary">
          <div className="stat-icon">📦</div>
          <div className="stat-content">
            <h3>{stats.totalStock}</h3>
            <p>Total Stock Units</p>
          </div>
        </div>
      </div>

      <div className="analytics-charts">
        <div className="chart-card">
          <h2>Products by Category</h2>
          <div className="chart-content">
            {categoryStats.length > 0 ? (
              <div className="bar-chart">
                {categoryStats.map((cat, index) => {
                  const maxCount = Math.max(...categoryStats.map(c => c.count), 1);
                  const percentage = (cat.count / maxCount) * 100;
                  return (
                    <div key={index} className="bar-item">
                      <div className="bar-label">{cat.name}</div>
                      <div className="bar-container">
                        <div 
                          className="bar-fill" 
                          style={{ width: `${percentage}%` }}
                        >
                          <span className="bar-value">{cat.count}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="no-data">No category data available</p>
            )}
          </div>
        </div>

        <div className="chart-card">
          <h2>Products by Price Range</h2>
          <div className="chart-content">
            {priceRangeStats.length > 0 ? (
              <div className="pie-chart">
                {priceRangeStats.map((range, index) => {
                  const total = priceRangeStats.reduce((sum, r) => sum + r.count, 0);
                  const percentage = total > 0 ? (range.count / total) * 100 : 0;
                  return (
                    <div key={index} className="pie-item">
                      <div className="pie-label">
                        <span className="pie-color" style={{ 
                          backgroundColor: ['#4299e1', '#48bb78', '#ed8936', '#f56565'][index] 
                        }}></span>
                        {range.label}
                      </div>
                      <div className="pie-value">
                        {range.count} ({percentage.toFixed(1)}%)
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="no-data">No price data available</p>
            )}
          </div>
        </div>
      </div>

      <div className="analytics-table-section">
        <h2>Category Performance</h2>
        <table className="analytics-table">
          <thead>
            <tr>
              <th>Category</th>
              <th>Products</th>
              <th>Total Value</th>
              <th>Average Price</th>
            </tr>
          </thead>
          <tbody>
            {categoryStats.map((cat, index) => {
              const avgPrice = cat.count > 0 
                ? (cat.totalValue / cat.count).toFixed(2) 
                : '0.00';
              return (
                <tr key={index}>
                  <td><strong>{cat.name}</strong></td>
                  <td>{cat.count}</td>
                  <td>${cat.totalValue.toLocaleString()}</td>
                  <td>${avgPrice}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Analytics;

