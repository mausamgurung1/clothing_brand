from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, CategoryViewSet, BlogPostViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'blog', BlogPostViewSet, basename='blogpost')

urlpatterns = [
    path('api/', include(router.urls)),
]

