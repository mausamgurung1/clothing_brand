import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { productsAPI } from '../services/api';
import { getProductImageUrl } from '../utils/imageUtils';
import './ProductDetail.css';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    loadProduct();
  }, [id]);

  const loadProduct = async () => {
    try {
      const response = await productsAPI.getById(id);
      setProduct(response.data);
      setSelectedImage(getProductImageUrl(response.data));
      
      // Load related products
      if (response.data.category) {
        const relatedRes = await productsAPI.getAll({
          category: response.data.category.slug,
          page_size: 4
        });
        setRelatedProducts(
          relatedRes.data.results?.filter(p => p.id !== response.data.id) || []
        );
      }
    } catch (error) {
      console.error('Error loading product:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading product...</div>;
  }

  if (!product) {
    return <div className="error">Product not found</div>;
  }

  const mainImageUrl = getProductImageUrl(product);
  const images = product.images || [];
  const allImages = mainImageUrl ? [mainImageUrl, ...images.map(img => getProductImageUrl(img))] : images.map(img => getProductImageUrl(img));

  return (
    <div className="product-detail-page">
      <div className="container">
        <div className="breadcrumb">
          <Link to="/">Home</Link> / <Link to="/product/">Shop</Link> / {product.name}
        </div>

        <div className="product-detail-grid">
          <div className="product-images">
            <div className="main-image">
              {selectedImage || mainImageUrl ? (
                <img 
                  src={selectedImage || mainImageUrl} 
                  alt={product.name}
                  className="product-main-image"
                />
              ) : (
                <div className="image-placeholder">No Image</div>
              )}
            </div>
            {allImages.length > 1 && (
              <div className="thumbnail-images">
                {allImages.map((img, idx) => (
                  <img
                    key={idx}
                    src={img}
                    alt={`${product.name} ${idx + 1}`}
                    className={selectedImage === img ? 'active' : ''}
                    onClick={() => setSelectedImage(img)}
                  />
                ))}
              </div>
            )}
          </div>

          <div className="product-info">
            <h1 className="product-title">{product.name}</h1>
            
            <div className="product-price-section">
              <span className="price">${product.price}</span>
              {product.compare_at_price && (
                <>
                  <span className="compare-price">${product.compare_at_price}</span>
                  {product.discount_percentage > 0 && (
                    <span className="discount-badge">-{product.discount_percentage}% OFF</span>
                  )}
                </>
              )}
            </div>

            {product.short_description && (
              <p className="product-short-desc">{product.short_description}</p>
            )}

            {product.description && (
              <div className="product-description">
                <h3>Description</h3>
                <p>{product.description}</p>
              </div>
            )}

            {product.sizes && (
              <div className="product-attributes">
                <strong>Sizes:</strong> {product.sizes}
              </div>
            )}

            {product.colors && (
              <div className="product-attributes">
                <strong>Colors:</strong> {product.colors}
              </div>
            )}

            {product.stock_quantity !== undefined && (
              <div className="product-stock">
                <strong>Stock:</strong> {product.stock_quantity > 0 ? `${product.stock_quantity} available` : 'Out of stock'}
              </div>
            )}

            {product.rating > 0 && (
              <div className="product-rating">
                <strong>Rating:</strong> ⭐ {product.rating}/5 ({product.review_count} reviews)
              </div>
            )}

            <div className="product-actions">
              <button className="btn-add-cart">Add to Cart</button>
              <button className="btn-wishlist">Add to Wishlist</button>
            </div>
          </div>
        </div>

        {relatedProducts.length > 0 && (
          <section className="related-products">
            <h2>Related Products</h2>
            <div className="products-grid">
              {relatedProducts.map(relatedProduct => (
                <div key={relatedProduct.id} className="product-card">
                  <div className="product-image-wrapper">
                    {getProductImageUrl(relatedProduct) ? (
                      <img 
                        src={getProductImageUrl(relatedProduct)} 
                        alt={relatedProduct.name}
                        className="product-image"
                      />
                    ) : (
                      <div className="product-image-placeholder">No Image</div>
                    )}
                  </div>
                  <div className="product-info">
                    <h3>{relatedProduct.name}</h3>
                    <div className="product-price">
                      <span className="price">${relatedProduct.price}</span>
                      {relatedProduct.compare_at_price && (
                        <span className="compare-price">${relatedProduct.compare_at_price}</span>
                      )}
                    </div>
                    <Link to={`/product/${relatedProduct.id}/`} className="btn-view">
                      View Details
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
};

export default ProductDetail;

