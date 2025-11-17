# 🚀 Running the Clothing Store Project

## ✅ Project Status

Both servers are now running!

### Backend (Django)
- **Status**: ✅ Running
- **URL**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

### Frontend (React)
- **Status**: ✅ Running  
- **URL**: http://localhost:5173
- **Admin Panel**: http://localhost:5173/

## 📋 Quick Start Commands

### Start Backend (Django)
```bash
cd /home/mausamgr/clothing_brand
python manage.py runserver
```

### Start Frontend (React)
```bash
cd /home/mausamgr/clothing_brand/frontend
npm run dev
```

## 🌐 Access Points

1. **React Admin Panel**: http://localhost:5173/
   - Create, edit, delete products
   - Upload images
   - Manage prices and offer prices

2. **Django Admin**: http://localhost:8000/admin/
   - Full admin interface
   - Manage all models

3. **API Browser**: http://localhost:8000/api/
   - REST API endpoints
   - Test API calls

4. **Main Website**: http://localhost:8000/
   - Public-facing website

## 🔧 API Endpoints

- **Products**: http://localhost:8000/api/products/
- **Categories**: http://localhost:8000/api/categories/
- **Blog Posts**: http://localhost:8000/api/blog/

## 📝 Features Available

✅ Product Management with React UI
✅ Image Upload with Preview
✅ Price & Offer Price Management
✅ Automatic Discount Calculation
✅ Form Validation
✅ PostgreSQL Database
✅ REST API

## 🛠️ Troubleshooting

### If servers are not running:

**Backend:**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process if needed
pkill -f "manage.py runserver"

# Start again
python manage.py runserver
```

**Frontend:**
```bash
# Check if port 5173 is in use
lsof -i :5173

# Kill existing process if needed
pkill -f vite

# Start again
cd frontend
npm run dev
```

### Database Issues:
```bash
# Run migrations
python manage.py migrate

# Create sample data
python manage.py create_sample_data --products 10
```

## 📊 Current Status

- ✅ Django server: Running on port 8000
- ✅ React server: Running on port 5173
- ✅ PostgreSQL: Connected
- ✅ API: Available at /api/
- ✅ CORS: Configured for React

## 🎯 Next Steps

1. Open http://localhost:5173/ in your browser
2. Click "Create New Product"
3. Fill in the form with:
   - Product name
   - Price
   - Offer price (optional)
   - Upload an image
   - Add other details
4. Click "Create Product"
5. View your products in the grid!

Enjoy your clothing store management system! 🎉

