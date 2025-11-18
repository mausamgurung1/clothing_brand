"""
Django REST Framework serializers for Baabuu Clothing

Copyright (c) 2024 Baabuu Clothing
Licensed under MIT License
"""

from rest_framework import serializers
from .models import Product, Category, ProductImage, BlogPost


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'order', 'is_primary']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    images = ProductImageSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'compare_at_price', 'discount_percentage',
            'category', 'category_id', 'tags',
            'main_image', 'main_image_url', 'image_url', 'images',
            'sku', 'stock_quantity', 'is_available',
            'sizes', 'colors', 'weight', 'dimensions', 'materials',
            'is_featured', 'is_hot', 'rating', 'review_count',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'sku', 'rating', 'review_count', 'created_at', 'updated_at']
    
    def get_main_image_url(self, obj):
        request = self.context.get('request')
        
        if obj.main_image:
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        
        # Return image_url if it exists, ensuring it's a full URL
        if obj.image_url:
            if request:
                # If image_url is a static path, make it absolute
                if obj.image_url.startswith('/static/'):
                    return request.build_absolute_uri(obj.image_url)
                # If already absolute, return as is
                if obj.image_url.startswith('http'):
                    return obj.image_url
                # Otherwise assume it's a media path
                if obj.image_url.startswith('/media/'):
                    return request.build_absolute_uri(obj.image_url)
                return request.build_absolute_uri(f'/media/{obj.image_url}')
            # Fallback: return as is if no request context
            return obj.image_url
        
        return ''
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products with image upload"""
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'short_description',
            'price', 'compare_at_price',
            'category_id', 'tags',
            'main_image', 'image_url',
            'stock_quantity', 'is_available',
            'sizes', 'colors', 'weight', 'dimensions', 'materials',
            'is_featured', 'is_hot', 'published_at'
        ]
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
    
    def validate_compare_at_price(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Compare at price cannot be negative.")
        return value
    
    def validate(self, data):
        price = data.get('price')
        compare_at_price = data.get('compare_at_price')
        
        if compare_at_price and price and compare_at_price <= price:
            raise serializers.ValidationError({
                'compare_at_price': 'Compare at price must be greater than regular price.'
            })
        
        return data


class BlogPostSerializer(serializers.ModelSerializer):
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'content', 'excerpt',
            'featured_image', 'featured_image_url', 'image_url',
            'is_published', 'published_at', 'view_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at']
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return obj.image_url or ''

