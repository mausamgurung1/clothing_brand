/**
 * Main App component with routing
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import ProductForm from './components/ProductForm';
import HomePage from './components/HomePage';
import ProductPage from './components/ProductPage';
import ProductDetail from './components/ProductDetail';
import Dashboard from './components/admin/Dashboard';
import CategoryManager from './components/admin/CategoryManager';
import AdvancedProductList from './components/admin/AdvancedProductList';
import AdminLayout from './components/admin/AdminLayout';
import Login from './components/admin/Login';
import ProtectedRoute from './components/admin/ProtectedRoute';
import Analytics from './components/admin/Analytics';
import Settings from './components/admin/Settings';
import UserManagement from './components/admin/UserManagement';
import './App.css';

// Admin Routes Component
const AdminRoutes = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  const handleCreate = () => {
    setEditingProduct(null);
    setShowForm(true);
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setShowForm(true);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingProduct(null);
    window.location.reload();
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingProduct(null);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    try {
      const { productsAPI } = await import('./services/api');
      await productsAPI.delete(id);
      window.location.reload();
    } catch (error) {
      console.error('Error deleting product:', error);
      alert('Error deleting product');
    }
  };

  return (
    <ProtectedRoute>
      {showForm && (
        <div style={{ padding: '2rem' }}>
          <ProductForm
            product={editingProduct}
            onSuccess={handleFormSuccess}
            onCancel={handleCancel}
          />
        </div>
      )}
      {!showForm && (
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route 
            path="/products" 
            element={
              <AdvancedProductList
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            } 
          />
          <Route path="/categories" element={<CategoryManager />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/users" element={<UserManagement />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      )}
    </ProtectedRoute>
  );
};

// Public Layout Component
const PublicLayout = ({ children }) => {
  return (
    <div className="app">
      <header className="app-header">
        <Link to="/" className="logo">
          <h1>Baabuu Clothing</h1>
        </Link>
        <nav className="main-nav">
          <Link to="/">Home</Link>
          <Link to="/product/">Shop</Link>
          <Link to="/admin">Admin</Link>
        </nav>
      </header>
      {children}
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/admin/login" element={<Login />} />
        <Route path="/admin/*" element={
          <AdminLayout>
            <AdminRoutes />
          </AdminLayout>
        } />
        <Route path="/*" element={
          <PublicLayout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/product/" element={<ProductPage />} />
              <Route path="/product/:id/" element={<ProductDetail />} />
            </Routes>
          </PublicLayout>
        } />
      </Routes>
    </Router>
  );
}

export default App;
