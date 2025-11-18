/**
 * Category Manager - Advanced category management
 * 
 * Copyright (c) 2024 Baabuu Clothing
 * Licensed under MIT License
 */

import React, { useState, useEffect } from 'react';
import { categoriesAPI } from '../../services/api';
import { getImageUrl } from '../../utils/imageUtils';
import './CategoryManager.css';

const CategoryManager = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    description: '',
    image: null,
    is_active: true,
  });

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data || []);
    } catch (error) {
      console.error('Error loading categories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = new FormData();
      data.append('name', formData.name);
      data.append('description', formData.description);
      data.append('is_active', formData.is_active);
      if (formData.image) {
        data.append('image', formData.image);
      }

      if (editingCategory) {
        await categoriesAPI.update(editingCategory.slug, data);
      } else {
        await categoriesAPI.create(data);
      }

      resetForm();
      loadCategories();
    } catch (error) {
      console.error('Error saving category:', error);
      alert('Error saving category');
    }
  };

  const handleEdit = (category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      slug: category.slug || '',
      description: category.description || '',
      image: null,
      is_active: category.is_active !== false,
    });
    setShowForm(true);
  };

  const handleDelete = async (slug) => {
    if (!window.confirm('Are you sure you want to delete this category?')) {
      return;
    }
    try {
      await categoriesAPI.delete(slug);
      loadCategories();
    } catch (error) {
      console.error('Error deleting category:', error);
      alert('Error deleting category');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      slug: '',
      description: '',
      image: null,
      is_active: true,
    });
    setEditingCategory(null);
    setShowForm(false);
  };

  const filteredCategories = categories.filter(cat =>
    cat.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="loading">Loading categories...</div>;
  }

  return (
    <div className="category-manager">
      <div className="manager-header">
        <div>
          <h1>Category Management</h1>
          <p>Manage product categories</p>
        </div>
        <div className="header-actions">
          <input
            type="text"
            placeholder="Search categories..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <button onClick={() => setShowForm(true)} className="btn-primary">
            + Add Category
          </button>
        </div>
      </div>

      {showForm && (
        <div className="form-modal">
          <div className="form-modal-content">
            <div className="form-header">
              <h2>{editingCategory ? 'Edit Category' : 'Add New Category'}</h2>
              <button onClick={resetForm} className="close-btn">×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Category Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="4"
                />
              </div>
              <div className="form-group">
                <label>Category Image</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setFormData({ ...formData, image: e.target.files[0] })}
                />
              </div>
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  />
                  Active
                </label>
              </div>
              <div className="form-actions">
                <button type="button" onClick={resetForm} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  {editingCategory ? 'Update' : 'Create'} Category
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="categories-grid">
        {filteredCategories.map(category => (
          <div key={category.id} className="category-card">
            <div className="category-image">
              {category.image ? (
                <img src={getImageUrl(category.image)} alt={category.name} />
              ) : (
                <div className="no-image">No Image</div>
              )}
            </div>
            <div className="category-info">
              <h3>{category.name}</h3>
              {category.description && (
                <p className="category-description">{category.description}</p>
              )}
              <div className="category-meta">
                <span className={`status-badge ${category.is_active ? 'active' : 'inactive'}`}>
                  {category.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
            <div className="category-actions">
              <button onClick={() => handleEdit(category)} className="btn-edit">
                Edit
              </button>
              <button onClick={() => handleDelete(category.slug)} className="btn-delete">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredCategories.length === 0 && (
        <div className="no-data">
          {searchTerm ? 'No categories found matching your search.' : 'No categories yet. Create your first category!'}
        </div>
      )}
    </div>
  );
};

export default CategoryManager;

