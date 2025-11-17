from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from .models import Product, Category, ProductImage, BlogPost
from .serializers import (
    ProductSerializer, ProductCreateUpdateSerializer,
    CategorySerializer, ProductImageSerializer, BlogPostSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Filter by hot
        hot = self.request.query_params.get('hot', None)
        if hot == 'true':
            queryset = queryset.filter(is_hot=True)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                description__icontains=search
            ) | queryset.filter(
                tags__icontains=search
            )
        
        # Sort
        sort_by = self.request.query_params.get('sort', '-created_at')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'rating':
            queryset = queryset.order_by('-rating', '-review_count')
        else:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Add image URLs to each product
        for product_data in response.data['results']:
            if 'main_image_url' not in product_data:
                product_data['main_image_url'] = product_data.get('image_url', '')
        return response
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        """Upload additional images for a product"""
        product = self.get_object()
        image = request.FILES.get('image')
        alt_text = request.data.get('alt_text', '')
        order = request.data.get('order', 0)
        is_primary = request.data.get('is_primary', False)
        
        if not image:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_image = ProductImage.objects.create(
            product=product,
            image=image,
            alt_text=alt_text,
            order=order,
            is_primary=is_primary
        )
        
        serializer = ProductImageSerializer(
            product_image,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'])
    def delete_image(self, request, pk=None):
        """Delete an image from a product"""
        image_id = request.data.get('image_id')
        if not image_id:
            return Response(
                {'error': 'image_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = self.get_object()
        try:
            image = ProductImage.objects.get(id=image_id, product=product)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                content__icontains=search
            )
        
        return queryset.order_by('-published_at')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

