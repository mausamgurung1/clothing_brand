# Baabuu Clothing - Django + React E-commerce Platform

A modern, full-stack e-commerce application built with Django REST Framework backend and React frontend.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Baabuu Clothing

## 🚀 Features

### Backend (Django)
- ✅ PostgreSQL database
- ✅ RESTful API with Django REST Framework
- ✅ Image upload handling
- ✅ Product management with price & offer price
- ✅ Category management
- ✅ Blog system
- ✅ Review system
- ✅ Contact forms
- ✅ Newsletter subscription

### Frontend (React)
- ✅ Modern React UI with Vite
- ✅ Product listing with images from backend
- ✅ Product creation/editing with image upload
- ✅ Price and offer price management
- ✅ Automatic discount calculation
- ✅ Category filtering
- ✅ Responsive design
- ✅ All data fetched from backend API

## 📋 Quick Start

### 1. Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create sample data (optional)
python manage.py create_sample_data --products 20 --blog-posts 5

# Start Django server
python manage.py runserver
```

Backend runs on: **http://localhost:8000**

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start React dev server
npm run dev
```

Frontend runs on: **http://localhost:5173**

## 🌐 Access Points

- **React App**: http://localhost:5173/
  - Home page with featured products
  - Shop page with all products
  - Admin panel for product management

- **Django Admin**: http://localhost:8000/admin/
  - Full admin interface
  - Manage all models

- **API Browser**: http://localhost:8000/api/
  - REST API endpoints
  - Test API calls

- **Main Website**: http://localhost:8000/
  - Public-facing website (Django templates)

## 📡 API Endpoints

All endpoints return JSON and support image uploads:

- `GET /api/products/` - List products (with pagination, filtering)
- `POST /api/products/` - Create product (with image upload)
- `GET /api/products/{id}/` - Get product details
- `PATCH /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `POST /api/products/{id}/upload_image/` - Upload additional images
- `GET /api/categories/` - List categories
- `GET /api/blog/` - List blog posts

## 🖼️ Image Handling

- Images are uploaded to `media/products/` directory
- Backend returns absolute URLs for images
- React components automatically handle image URLs
- Fallback to static images if uploaded image not available
- Image preview before upload

## 💰 Price Management

- **Price**: Regular selling price (required)
- **Compare at Price**: Original/higher price for showing discounts
- **Discount**: Automatically calculated percentage
- Validation: Offer price must be greater than regular price

## 🎨 React Components

- **HomePage**: Displays featured and hot products from backend
- **ProductPage**: Product listing with category filtering
- **ProductList**: Admin product management
- **ProductForm**: Create/edit products with image upload

## 🔧 Technology Stack

**Backend:**
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Pillow (image processing)

**Frontend:**
- React 18
- Vite (build tool)
- React Router
- Axios (API calls)
- React Hook Form

## 📁 Project Structure

```
clothing_brand/
├── clothing_store/       # Django project
├── store/                # Django app
│   ├── models.py        # Database models
│   ├── api_views.py     # API viewsets
│   ├── serializers.py   # DRF serializers
│   └── api_urls.py      # API routes
├── frontend/            # React app
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── utils/       # Utility functions
│   └── package.json
├── templates/           # Django templates
├── static/             # Static files
└── media/              # Uploaded files
```

## 🎯 Key Features

1. **All Data from Backend**: React fetches all data from Django API
2. **Image Upload**: Full image upload support with preview
3. **Price Management**: Price and offer price with discount calculation
4. **Real-time Updates**: Changes reflect immediately
5. **Error Handling**: Proper error handling and fallbacks
6. **Image Fallbacks**: Handles missing images gracefully

## 🚀 Production Deployment

1. Build React app: `cd frontend && npm run build`
2. Collect static files: `python manage.py collectstatic`
3. Configure production database
4. Set environment variables
5. Use a production server (Gunicorn + Nginx)

## 📝 Notes

- All images are served from backend
- API uses absolute URLs for images
- React components handle image errors gracefully
- CORS is configured for development
- Media files are stored in `media/` directory

Enjoy your modern e-commerce platform! 🎉
