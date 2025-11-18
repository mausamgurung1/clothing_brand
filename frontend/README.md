# React Frontend - Dynamic Configuration

## Environment Variables

Create a `.env` file in the `frontend/` directory (copy from `.env.example`):

```env
# Development
VITE_API_BASE_URL=http://localhost:8000
VITE_MEDIA_BASE_URL=http://localhost:8000
VITE_PORT=5173
```

### For Production:

```env
# Production - MUST set these
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_MEDIA_BASE_URL=https://api.yourdomain.com
VITE_PORT=5173
```

**Important**: In production, `VITE_API_BASE_URL` should be set to your actual API domain. The proxy in `vite.config.js` will use this value dynamically.

## Dynamic URL Configuration

The project uses environment variables for all URLs:

- **Development**: Uses `.env` file or defaults to `http://localhost:8000`
- **Production**: Set `VITE_API_BASE_URL` to your production API URL

## How It Works

1. **Config File** (`src/config.js`):
   - Reads environment variables
   - Provides utility functions for URLs
   - Falls back to current origin if not set

2. **API Service** (`src/services/api.js`):
   - Uses dynamic base URL from config
   - Automatically handles proxy in development

3. **Image Utils** (`src/utils/imageUtils.js`):
   - Uses dynamic media base URL
   - Handles all image URL formats

## No Hardcoded URLs

All components use:
- `getApiUrl()` for API endpoints
- `getMediaUrl()` for images
- `getProductImageUrl()` for product images

These functions automatically use the correct base URL based on environment.

