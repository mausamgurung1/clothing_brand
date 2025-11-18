# Django Admin Panel Guide - Baabuu Clothing

## Overview

This project has **two admin panels**:

1. **Django Admin** (Backend) - `http://localhost:8000/admin/`
   - Traditional Django admin interface
   - Full CRUD operations for all models
   - User management
   - Best for backend data management

2. **React Admin** (Frontend) - `http://localhost:5173/admin/`
   - Modern React-based admin interface
   - Advanced product management
   - Analytics dashboard
   - Best for frontend user experience

---

## Django Admin Access

### URL
- **Django Admin**: `http://localhost:8000/admin/`
- **User Management**: `http://localhost:8000/admin/auth/user/` ✅ (correct)
- **Note**: `/admin/user/` will automatically redirect to `/admin/auth/user/`

### Login Credentials
Use your Django superuser credentials:
```bash
python manage.py createsuperuser
```

### Features

#### 1. **Custom User Admin**
- Enhanced user list with additional fields
- Shows: username, email, first name, last name, staff status, superuser status, date joined, last login
- Filterable by: staff status, superuser status, active status, date joined
- Searchable by: username, email, first name, last name

#### 2. **Product Management**
- Full product CRUD operations
- Image uploads (main image + multiple product images)
- Price and offer price management
- Stock quantity tracking
- Featured and hot product flags
- SEO fields (meta title, meta description)

#### 3. **Category Management**
- Category CRUD operations
- Product count display
- Active/inactive status

#### 4. **Blog Management**
- Blog post creation and editing
- Featured image uploads
- Publishing controls
- View count tracking

#### 5. **Contact Messages**
- View all contact form submissions
- Status management (new, read, replied, archived)
- Bulk actions: mark as read, mark as replied, archive

#### 6. **Newsletter Subscribers**
- View all newsletter subscriptions
- Active/inactive status
- Subscription date tracking

#### 7. **Product Reviews**
- Review approval/disapproval
- Bulk actions for review management
- Rating and comment display

---

## Custom Admin Branding

The Django admin has been customized with:
- **Site Header**: "Baabuu Clothing Admin"
- **Site Title**: "Baabuu Clothing Admin Portal"
- **Index Title**: "Welcome to Baabuu Clothing Administration"

---

## Dark Mode / Light Mode

Django Admin (Django 3.2+) includes **built-in dark mode support**:

### How to Toggle:
1. **Look for the moon icon** (🌙) in the top-right corner of the Django admin
2. **Click the moon icon** to cycle through themes:
   - **Auto** → Follows your system preference
   - **Light** → Always light mode
   - **Dark** → Always dark mode
3. **Your preference is saved** in browser localStorage

### Note:
- This is **separate** from the React admin panel dark mode
- Django admin dark mode is a built-in Django feature
- React admin dark mode is our custom implementation

---

## Common URLs

| Model | URL |
|-------|-----|
| Users | `/admin/auth/user/` |
| Products | `/admin/store/product/` |
| Categories | `/admin/store/category/` |
| Blog Posts | `/admin/store/blogpost/` |
| Contact Messages | `/admin/store/contactmessage/` |
| Newsletter | `/admin/store/newslettersubscriber/` |
| Reviews | `/admin/store/review/` |

---

## Favicon Fix

The favicon 404 error has been fixed by:
- Adding a redirect from `/favicon.ico` to `/static/images/icons/favicon.png`
- This eliminates the 404 errors in the logs

---

## Quick Start

1. **Create a superuser** (if you haven't already):
   ```bash
   python manage.py createsuperuser
   ```

2. **Access Django Admin**:
   - Go to: `http://localhost:8000/admin/`
   - Login with your superuser credentials

3. **Access User Management**:
   - Go to: `http://localhost:8000/admin/auth/user/`
   - Or click "Users" in the admin sidebar

---

## Notes

- The Django admin is automatically available at `/admin/`
- User model is at `/admin/auth/user/` (not `/admin/user/`)
- All models from the `store` app are registered and accessible
- The admin interface is fully customizable and can be extended as needed

---

**Copyright (c) 2024 Baabuu Clothing**  
**Licensed under MIT License**

