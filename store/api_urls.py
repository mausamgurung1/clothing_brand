from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    ProductViewSet, CategoryViewSet, BlogPostViewSet,
    login_view, logout_view, check_auth_view
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'blog', BlogPostViewSet, basename='blogpost')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/login/', login_view, name='api_login'),
    path('api/auth/logout/', logout_view, name='api_logout'),
    path('api/auth/check/', check_auth_view, name='api_check_auth'),
]

