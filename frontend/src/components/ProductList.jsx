import React, { useState, useEffect } from 'react';
import { productsAPI } from '../services/api';
import { getProductImageUrl } from '../utils/imageUtils';

const ProductList = ({ onEdit, onDelete }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    loadProducts();
  }, [page]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const response = await productsAPI.getAll({ page });
      setProducts(response.data.results);
      setTotalPages(Math.ceil(response.data.count / 12));
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await productsAPI.delete(id);
        loadProducts();
      } catch (error) {
        console.error('Error deleting product:', error);
        alert('Error deleting product');
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading products...</div>;
  }

  return (
    <div className="product-list">
      <h2>Products</h2>
      <div className="products-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <div className="product-image">
              {getProductImageUrl(product) ? (
                <img 
                  src={getProductImageUrl(product)} 
                  alt={product.name}
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
                className="no-image" 
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
              <h3>{product.name}</h3>
              <div className="product-price">
                <span className="price">${product.price}</span>
                {product.compare_at_price && (
                  <span className="compare-price">${product.compare_at_price}</span>
                )}
              </div>
              <div className="product-meta">
                <span>Stock: {product.stock_quantity}</span>
                <span>Rating: {product.rating || 0}/5</span>
              </div>
              <div className="product-actions">
                <button onClick={() => onEdit(product)} className="btn-edit">
                  Edit
                </button>
                <button onClick={() => handleDelete(product.id)} className="btn-delete">
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      {products.length === 0 && (
        <div className="empty-state">No products found. Create your first product!</div>
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
  );
};

export default ProductList;

