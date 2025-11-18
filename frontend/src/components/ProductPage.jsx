import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, Link } from 'react-router-dom';
import { productsAPI, categoriesAPI } from '../services/api';
import { getProductImageUrl } from '../utils/imageUtils';
import './ProductPage.css';

const ProductPage = () => {
  const [searchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || '');

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    loadProducts();
  }, [page, selectedCategory]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const params = { page, page_size: 12 };
      if (selectedCategory) {
        params.category = selectedCategory;
      }
      const response = await productsAPI.getAll(params);
      setProducts(response.data.results || []);
      setTotalPages(Math.ceil((response.data.count || 0) / 12));
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


  if (loading) {
    return <div className="loading">Loading products...</div>;
  }

  return (
    <div className="product-page">
      <div className="container">
        <div className="product-page-header">
          <h1>Shop</h1>
          <div className="filters">
            <select 
              value={selectedCategory} 
              onChange={(e) => {
                setSelectedCategory(e.target.value);
                setPage(1);
              }}
              className="category-filter"
            >
              <option value="">All Categories</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.slug}>{cat.name}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="products-grid">
          {products.map(product => (
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
                <div className="product-meta">
                  <span>Stock: {product.stock_quantity}</span>
                  {product.rating > 0 && <span>⭐ {product.rating}</span>}
                </div>
                <Link to={`/product/${product.id}/`} className="btn-view">View Details</Link>
              </div>
            </div>
          ))}
        </div>

        {products.length === 0 && (
          <div className="empty-state">
            <p>No products found.</p>
          </div>
        )}

        {totalPages > 1 && (
          <div className="pagination">
            <button 
              onClick={() => setPage(p => Math.max(1, p - 1))} 
              disabled={page === 1}
            >
              Previous
            </button>
            <span>Page {page} of {totalPages}</span>
            <button 
              onClick={() => setPage(p => Math.min(totalPages, p + 1))} 
              disabled={page === totalPages}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductPage;

