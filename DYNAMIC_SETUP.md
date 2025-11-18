# Dynamic Configuration Setup - Baabuu Clothing

## ✅ All URLs Are Now Dynamic!

The project has been completely refactored to use **environment variables** instead of hardcoded URLs. This makes it work seamlessly across different environments (development, staging, production).

## 🔧 Configuration Files

### 1. Frontend Configuration (`frontend/.env`)

Create `frontend/.env` file:

```env
# Development
VITE_API_BASE_URL=http://localhost:8000
VITE_MEDIA_BASE_URL=http://localhost:8000

# Production (example)
# VITE_API_BASE_URL=https://api.yourdomain.com
# VITE_MEDIA_BASE_URL=https://api.yourdomain.com
```

### 2. Django Configuration (`.env` in root)

Create `.env` file in project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
USE_POSTGRESQL=False
DB_NAME=clothing_store_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CORS (comma-separated)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📁 Key Files

### `frontend/src/config.js`
- **Central configuration file**
- Reads environment variables
- Provides utility functions: `getApiUrl()`, `getMediaUrl()`
- Automatically uses current origin if env vars not set

### `frontend/src/services/api.js`
- Uses dynamic API base URL from config
- Automatically handles proxy in development
- Works with any backend URL

### `frontend/src/utils/imageUtils.js`
- Uses dynamic media base URL
- Handles all image URL formats
- No hardcoded URLs

### `store/serializers.py`
- Backend returns absolute URLs using `request.build_absolute_uri()`
- Automatically adapts to current domain
- Works in any environment

## 🚀 How It Works

### Development Mode
1. Frontend reads `VITE_API_BASE_URL` from `.env`
2. If not set, uses current `window.location.origin`
3. Vite proxy forwards `/api` requests to backend
4. All image URLs use dynamic base URL

### Production Mode
1. Set `VITE_API_BASE_URL` to your production API URL
2. Build React app: `npm run build`
3. All URLs automatically use production domain
4. No code changes needed!

## ✨ Benefits

1. **No Hardcoded URLs**: Everything uses environment variables
2. **Environment Agnostic**: Same code works in dev/staging/prod
3. **Easy Deployment**: Just change env vars
4. **Automatic Fallbacks**: Uses current origin if env not set
5. **Type Safe**: Centralized configuration

## 🔍 What Changed

### Before (Hardcoded):
```javascript
const API_URL = 'http://localhost:8000/api';
const imageUrl = `http://localhost:8000${product.image}`;
```

### After (Dynamic):
```javascript
import { getMediaUrl } from '../config';
const imageUrl = getMediaUrl(product.image); // Automatically uses env var or current origin
```

## 📝 Usage Examples

### In Components:
```javascript
import { getProductImageUrl } from '../utils/imageUtils';
import { getApiUrl } from '../config';

// Get product image (automatically uses correct base URL)
const imageUrl = getProductImageUrl(product);

// Build API URL
const apiUrl = getApiUrl('/products/');
```

### Environment Variables:
- **Development**: `VITE_API_BASE_URL=http://localhost:8000`
- **Staging**: `VITE_API_BASE_URL=https://staging-api.example.com`
- **Production**: `VITE_API_BASE_URL=https://api.example.com`

## 🎯 All Components Updated

✅ `HomePage.jsx` - Uses dynamic image URLs
✅ `ProductPage.jsx` - Uses dynamic image URLs
✅ `ProductList.jsx` - Uses dynamic image URLs
✅ `ProductForm.jsx` - Uses dynamic image URLs
✅ `ProductDetail.jsx` - Uses dynamic image URLs
✅ `api.js` - Uses dynamic API base URL
✅ `imageUtils.js` - Uses dynamic media base URL

## 🔄 Migration Guide

If you have existing code with hardcoded URLs:

1. **Replace hardcoded URLs**:
   ```javascript
   // ❌ Old
   const url = 'http://localhost:8000/api/products';
   
   // ✅ New
   import { getApiUrl } from '../config';
   const url = getApiUrl('/products/');
   ```

2. **Replace image URLs**:
   ```javascript
   // ❌ Old
   const img = `http://localhost:8000${product.image}`;
   
   // ✅ New
   import { getProductImageUrl } from '../utils/imageUtils';
   const img = getProductImageUrl(product);
   ```

## 🎉 Result

**Zero hardcoded URLs in the entire project!** Everything is now dynamic and environment-aware.

