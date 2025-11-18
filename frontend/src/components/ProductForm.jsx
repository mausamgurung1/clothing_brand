import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { productsAPI, categoriesAPI } from '../services/api';
import { getProductImageUrl } from '../utils/imageUtils';

const ProductForm = ({ product, onSuccess, onCancel }) => {
  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm({
    defaultValues: product || {
      name: '',
      description: '',
      short_description: '',
      price: '',
      compare_at_price: '',
      category_id: '',
      tags: '',
      stock_quantity: 0,
      is_available: true,
      sizes: '',
      colors: '',
      weight: '',
      dimensions: '',
      materials: '',
      is_featured: false,
      is_hot: false,
    }
  });

  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    loadCategories();
    if (product) {
      // Set image preview from product using dynamic URL
      if (product.main_image_url) {
        setImagePreview(getProductImageUrl(product));
      } else if (product.image_url) {
        setImagePreview(getProductImageUrl(product));
      }
    }
  }, [product]);

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const formData = {
        ...data,
        price: parseFloat(data.price),
        compare_at_price: data.compare_at_price ? parseFloat(data.compare_at_price) : null,
        stock_quantity: parseInt(data.stock_quantity),
        weight: data.weight ? parseFloat(data.weight) : null,
        is_available: data.is_available === true || data.is_available === 'true',
        is_featured: data.is_featured === true || data.is_featured === 'true',
        is_hot: data.is_hot === true || data.is_hot === 'true',
      };

      if (selectedImage) {
        formData.main_image = selectedImage;
      }

      if (product) {
        await productsAPI.update(product.id, formData);
      } else {
        await productsAPI.create(formData);
      }

      onSuccess();
    } catch (error) {
      console.error('Error saving product:', error);
      alert('Error saving product: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="product-form">
      <div className="form-section">
        <h2>{product ? 'Edit Product' : 'Create New Product'}</h2>
        
        <div className="form-group">
          <label>Product Name *</label>
          <input
            {...register('name', { required: 'Product name is required' })}
            className={errors.name ? 'error' : ''}
          />
          {errors.name && <span className="error-text">{errors.name.message}</span>}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Price *</label>
            <input
              type="number"
              step="0.01"
              {...register('price', { 
                required: 'Price is required',
                min: { value: 0, message: 'Price must be positive' }
              })}
              className={errors.price ? 'error' : ''}
            />
            {errors.price && <span className="error-text">{errors.price.message}</span>}
          </div>

          <div className="form-group">
            <label>Compare at Price (Offer Price)</label>
            <input
              type="number"
              step="0.01"
              {...register('compare_at_price', {
                validate: (value) => {
                  const price = parseFloat(watch('price'));
                  if (value && parseFloat(value) <= price) {
                    return 'Offer price must be greater than regular price';
                  }
                  return true;
                }
              })}
              className={errors.compare_at_price ? 'error' : ''}
            />
            {errors.compare_at_price && (
              <span className="error-text">{errors.compare_at_price.message}</span>
            )}
            {watch('compare_at_price') && watch('price') && (
              <div className="discount-info">
                Discount: {Math.round(((parseFloat(watch('compare_at_price')) - parseFloat(watch('price'))) / parseFloat(watch('compare_at_price'))) * 100)}%
              </div>
            )}
          </div>
        </div>

        <div className="form-group">
          <label>Category</label>
          <select {...register('category_id')}>
            <option value="">Select Category</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Short Description</label>
          <textarea
            {...register('short_description')}
            rows="2"
          />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea
            {...register('description')}
            rows="5"
          />
        </div>

        <div className="form-group">
          <label>Product Image</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />
          {imagePreview && (
            <div className="image-preview">
              <img 
                src={imagePreview} 
                alt="Preview"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
          )}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Stock Quantity</label>
            <input
              type="number"
              {...register('stock_quantity', { min: 0 })}
            />
          </div>

          <div className="form-group">
            <label>Sizes (comma-separated)</label>
            <input {...register('sizes')} placeholder="S,M,L,XL" />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Colors (comma-separated)</label>
            <input {...register('colors')} placeholder="Black,Blue,White" />
          </div>

          <div className="form-group">
            <label>Weight (kg)</label>
            <input
              type="number"
              step="0.01"
              {...register('weight')}
            />
          </div>
        </div>

        <div className="form-group">
          <label>Dimensions</label>
          <input {...register('dimensions')} placeholder="110 x 33 x 100 cm" />
        </div>

        <div className="form-group">
          <label>Materials</label>
          <input {...register('materials')} placeholder="60% cotton, 40% polyester" />
        </div>

        <div className="form-group">
          <label>Tags (comma-separated)</label>
          <input {...register('tags')} placeholder="Fashion,Lifestyle,Denim" />
        </div>

        <div className="form-checkboxes">
          <label>
            <input type="checkbox" {...register('is_available')} />
            Available
          </label>
          <label>
            <input type="checkbox" {...register('is_featured')} />
            Featured
          </label>
          <label>
            <input type="checkbox" {...register('is_hot')} />
            Hot
          </label>
        </div>

        <div className="form-actions">
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Saving...' : (product ? 'Update Product' : 'Create Product')}
          </button>
          {onCancel && (
            <button type="button" onClick={onCancel} className="btn-secondary">
              Cancel
            </button>
          )}
        </div>
      </div>
    </form>
  );
};

export default ProductForm;

