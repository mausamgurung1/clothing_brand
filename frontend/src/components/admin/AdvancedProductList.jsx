/**
 * Advanced Product List with search, filters, and bulk actions
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState, useEffect } from 'react';
import { productsAPI, categoriesAPI } from '../../services/api';
import { getProductImageUrl } from '../../utils/imageUtils';
import './AdvancedProductList.css';

const AdvancedProductList = ({ onEdit, onDelete }) => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [stockFilter, setStockFilter] = useState('all');
  const [sortBy, setSortBy] = useState('created_at');
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [viewMode, setViewMode] = useState('table'); // 'table' or 'grid'

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    loadProducts();
  }, [page, selectedCategory, statusFilter, stockFilter, sortBy]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const params = {
        page,
        page_size: pageSize,
        ordering: sortBy === 'created_at' ? '-created_at' : sortBy,
      };

      if (selectedCategory) {
        params.category = selectedCategory;
      }
      if (statusFilter === 'featured') {
        params.featured = 'true';
      } else if (statusFilter === 'hot') {
        params.hot = 'true';
      }
      if (stockFilter === 'low') {
        params.stock_low = 'true';
      } else if (stockFilter === 'out') {
        params.stock_out = 'true';
      }

      const response = await productsAPI.getAll(params);
      setProducts(response.data.results || []);
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data || []);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const handleBulkDelete = async () => {
    if (selectedProducts.length === 0) return;
    if (!window.confirm(`Delete ${selectedProducts.length} products?`)) return;

    try {
      await Promise.all(selectedProducts.map(id => productsAPI.delete(id)));
      setSelectedProducts([]);
      loadProducts();
    } catch (error) {
      console.error('Error deleting products:', error);
      alert('Error deleting products');
    }
  };

  const handleBulkStatusChange = async (isAvailable) => {
    if (selectedProducts.length === 0) return;

    try {
      await Promise.all(
        selectedProducts.map(id =>
          productsAPI.update(id, { is_available: isAvailable })
        )
      );
      setSelectedProducts([]);
      loadProducts();
    } catch (error) {
      console.error('Error updating products:', error);
      alert('Error updating products');
    }
  };

  const toggleProductSelection = (id) => {
    setSelectedProducts(prev =>
      prev.includes(id)
        ? prev.filter(p => p !== id)
        : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (selectedProducts.length === products.length) {
      setSelectedProducts([]);
    } else {
      setSelectedProducts(products.map(p => p.id));
    }
  };

  const handleExport = async () => {
    try {
      const response = await productsAPI.getAll({ page_size: 10000 });
      const data = response.data.results || [];
      const jsonStr = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `products_export_${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      alert('Products exported successfully!');
    } catch (error) {
      console.error('Export error:', error);
      alert('Error exporting products');
    }
  };

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="advanced-product-list">
      <div className="list-header">
        <div>
          <h1>Product Management</h1>
          <p>Manage your product catalog</p>
        </div>
        <div className="header-actions">
          <button 
            onClick={handleExport} 
            className="btn-secondary"
            title="Export products"
          >
            📥 Export
          </button>
          <button onClick={() => onEdit(null)} className="btn-primary">
            + Add Product
          </button>
        </div>
      </div>

      <div className="filters-section">
        <div className="filters-grid">
          <div className="filter-group">
            <label>Search</label>
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>

          <div className="filter-group">
            <label>Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => {
                setSelectedCategory(e.target.value);
                setPage(1);
              }}
              className="filter-select"
            >
              <option value="">All Categories</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.slug}>{cat.name}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Status</label>
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setPage(1);
              }}
              className="filter-select"
            >
              <option value="all">All</option>
              <option value="featured">Featured</option>
              <option value="hot">Hot</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Stock</label>
            <select
              value={stockFilter}
              onChange={(e) => {
                setStockFilter(e.target.value);
                setPage(1);
              }}
              className="filter-select"
            >
              <option value="all">All</option>
              <option value="in">In Stock</option>
              <option value="low">Low Stock</option>
              <option value="out">Out of Stock</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value);
                setPage(1);
              }}
              className="filter-select"
            >
              <option value="created_at">Newest</option>
              <option value="name">Name</option>
              <option value="price">Price: Low to High</option>
              <option value="-price">Price: High to Low</option>
              <option value="-rating">Rating</option>
            </select>
          </div>

          <div className="filter-group">
            <label>View Mode</label>
            <div className="view-mode-toggle">
              <button
                type="button"
                className={viewMode === 'table' ? 'active' : ''}
                onClick={() => setViewMode('table')}
              >
                📋 Table
              </button>
              <button
                type="button"
                className={viewMode === 'grid' ? 'active' : ''}
                onClick={() => setViewMode('grid')}
              >
                🎴 Grid
              </button>
            </div>
          </div>
        </div>

        {selectedProducts.length > 0 && (
          <div className="bulk-actions">
            <span>{selectedProducts.length} selected</span>
            <button onClick={() => handleBulkStatusChange(true)} className="btn-sm">
              Activate
            </button>
            <button onClick={() => handleBulkStatusChange(false)} className="btn-sm">
              Deactivate
            </button>
            <button onClick={handleBulkDelete} className="btn-sm btn-danger">
              Delete
            </button>
            <button onClick={() => setSelectedProducts([])} className="btn-sm btn-secondary">
              Clear
            </button>
          </div>
        )}
      </div>

      {loading ? (
        <div className="loading">Loading products...</div>
      ) : (
        <>
          {viewMode === 'table' ? (
            <div className="products-table-wrapper">
              <table className="products-table">
              <thead>
                <tr>
                  <th>
                    <input
                      type="checkbox"
                      checked={selectedProducts.length === products.length && products.length > 0}
                      onChange={toggleSelectAll}
                    />
                  </th>
                  <th>Image</th>
                  <th>Name</th>
                  <th>Category</th>
                  <th>Price</th>
                  <th>Stock</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredProducts.map(product => (
                  <tr key={product.id}>
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedProducts.includes(product.id)}
                        onChange={() => toggleProductSelection(product.id)}
                      />
                    </td>
                    <td>
                      <div className="product-thumb">
                        {getProductImageUrl(product) ? (
                          <img src={getProductImageUrl(product)} alt={product.name} />
                        ) : (
                          <span>No Image</span>
                        )}
                      </div>
                    </td>
                    <td>
                      <div className="product-name-cell">
                        <strong>{product.name}</strong>
                        {product.is_featured && <span className="badge featured">Featured</span>}
                        {product.is_hot && <span className="badge hot">Hot</span>}
                      </div>
                    </td>
                    <td>{product.category?.name || 'N/A'}</td>
                    <td>
                      <div className="price-cell">
                        <span className="price">${product.price}</span>
                        {product.compare_at_price && (
                          <span className="compare-price">${product.compare_at_price}</span>
                        )}
                      </div>
                    </td>
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
                    <td>
                      <div className="action-buttons">
                        <button onClick={() => onEdit(product)} className="btn-edit">
                          Edit
                        </button>
                        <button onClick={() => onDelete(product.id)} className="btn-delete">
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          ) : (
            <div className="products-grid-view">
              {filteredProducts.map(product => (
                <div key={product.id} className="product-grid-card">
                  <div className="product-grid-image">
                    {getProductImageUrl(product) ? (
                      <img src={getProductImageUrl(product)} alt={product.name} />
                    ) : (
                      <div className="no-image">No Image</div>
                    )}
                    <div className="product-grid-badges">
                      {product.is_featured && <span className="badge featured">Featured</span>}
                      {product.is_hot && <span className="badge hot">Hot</span>}
                    </div>
                  </div>
                  <div className="product-grid-info">
                    <h3>{product.name}</h3>
                    <p className="product-grid-category">{product.category?.name || 'N/A'}</p>
                    <div className="product-grid-price">
                      <span className="price">${product.price}</span>
                      {product.compare_at_price && (
                        <span className="compare-price">${product.compare_at_price}</span>
                      )}
                    </div>
                    <div className="product-grid-meta">
                      <span className={`stock-badge ${product.stock_quantity === 0 ? 'out' : product.stock_quantity < 10 ? 'low' : 'ok'}`}>
                        Stock: {product.stock_quantity}
                      </span>
                      <span className={`status-badge ${product.is_available ? 'active' : 'inactive'}`}>
                        {product.is_available ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <div className="product-grid-actions">
                      <input
                        type="checkbox"
                        checked={selectedProducts.includes(product.id)}
                        onChange={() => toggleProductSelection(product.id)}
                      />
                      <button onClick={() => onEdit(product)} className="btn-edit">
                        Edit
                      </button>
                      <button onClick={() => onDelete(product.id)} className="btn-delete">
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {filteredProducts.length === 0 && (
            <div className="no-data">
              {searchTerm ? 'No products found matching your search.' : 'No products yet. Create your first product!'}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AdvancedProductList;

