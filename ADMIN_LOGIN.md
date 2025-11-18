# Admin Panel Login Guide

## 🔐 How to Login to Admin Panel

### Step 1: Create a Superuser

First, you need to create an admin user in Django:

```bash
cd /home/mausamgr/clothing_brand
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email (optional)
- Password (twice for confirmation)

### Step 2: Access Login Page

Navigate to: **http://localhost:5173/admin/login**

### Step 3: Enter Credentials

Use the username and password you created in Step 1.

### Step 4: Access Admin Panel

After successful login, you'll be redirected to the admin dashboard at:
**http://localhost:5173/admin/**

## 🔑 Features

- **Token-based Authentication**: Uses Django REST Framework tokens
- **Secure**: Only staff/superuser accounts can access
- **Auto-redirect**: Automatically redirects to login if not authenticated
- **Session Persistence**: Token saved in localStorage
- **Logout**: Click "Logout" button in admin header

## 📝 API Endpoints

- `POST /api/auth/login/` - Login endpoint
- `POST /api/auth/logout/` - Logout endpoint  
- `GET /api/auth/check/` - Check authentication status

## ⚠️ Important Notes

1. **Only staff users** can access the admin panel
2. Token is stored in browser localStorage
3. Token is automatically included in API requests
4. If token expires, you'll be redirected to login

## 🛠️ Troubleshooting

### Can't login?
- Make sure you created a superuser: `python manage.py createsuperuser`
- Check that the user has `is_staff=True` or `is_superuser=True`
- Verify Django server is running on port 8000
- Check browser console for errors

### Token expired?
- Simply login again
- Token will be refreshed automatically

### Forgot password?
- Use Django admin: `python manage.py changepassword <username>`
- Or create a new superuser

