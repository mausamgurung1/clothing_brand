from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Inline admin for SubProduct (shown within Product)
class SubProductInline(admin.TabularInline):
    model = SubProduct
    extra = 1
    fields = ['description', 'image', 'image_preview']
    readonly_fields = ['image_preview']
    verbose_name = "Product Variation"
    verbose_name_plural = "Product Variations"
    
    def image_preview(self, obj):
        if obj.image:
            # Handle both string URLs and ImageField
            if isinstance(obj.image, str):
                # Image is stored as a URL string
                if obj.image.startswith('http'):
                    image_url = obj.image
                elif obj.image.startswith('images/'):
                    image_url = f'https://images.prathmeshsoni.works/{obj.image}'
                else:
                    image_url = f'/media/{obj.image}'
            else:
                # Image is an ImageField object
                image_url = obj.image.url
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', image_url)
        return "No image"
    image_preview.short_description = "Preview"

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_per_page = 20

# Size Admin
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_per_page = 20

# Color Admin
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_per_page = 20

# Product Admin with inline SubProducts
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'image_preview', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'category__name']
    inlines = [SubProductInline]
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'price')
        }),
        ('Product Image', {
            'fields': ('image_id', 'image_preview'),
        }),
    )
    
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image_id:
            # Handle both string URLs and ImageField
            if isinstance(obj.image_id, str):
                # Image is stored as a URL string
                if obj.image_id.startswith('http'):
                    image_url = obj.image_id
                elif obj.image_id.startswith('images/'):
                    image_url = f'https://images.prathmeshsoni.works/{obj.image_id}'
                else:
                    image_url = f'/media/{obj.image_id}'
            else:
                # Image is an ImageField object
                image_url = obj.image_id.url
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', image_url)
        return "No image"
    image_preview.short_description = "Image Preview"

# ProductSizeNColor Admin
@admin.register(ProductSizeNColor)
class ProductSizeNColorAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'stock_quantity', 'created_at']
    list_filter = ['size', 'color', 'product', 'created_at']
    search_fields = ['product__name', 'size__name', 'color__name']
    list_editable = ['stock_quantity']
    autocomplete_fields = ['product', 'size', 'color']
    list_per_page = 50
    
    fieldsets = (
        ('Product Details', {
            'fields': ('product',)
        }),
        ('Variation Details', {
            'fields': ('size', 'color', 'stock_quantity')
        }),
    )

# SubProduct Admin with inline ProductSizeNColor
@admin.register(SubProduct)
class SubProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'description_preview', 'image_preview', 'get_stock_quantity', 'created_at']
    list_filter = ['product', 'created_at']
    search_fields = ['product__name', 'description']
    filter_horizontal = ['product_size_color']
    list_per_page = 20
    
    fieldsets = (
        ('Product Reference', {
            'fields': ('product',)
        }),
        ('Variation Details', {
            'fields': ('description', 'product_size_color')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
    )
    
    readonly_fields = ['image_preview', 'get_stock_quantity']
    
    def description_preview(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_preview.short_description = "Description"
    
    def image_preview(self, obj):
        if obj.image:
            # Handle both string URLs and ImageField
            if isinstance(obj.image, str):
                # Image is stored as a URL string
                if obj.image.startswith('http'):
                    image_url = obj.image
                elif obj.image.startswith('images/'):
                    image_url = f'https://images.prathmeshsoni.works/{obj.image}'
                else:
                    image_url = f'/media/{obj.image}'
            else:
                # Image is an ImageField object
                image_url = obj.image.url
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', image_url)
        return "No image"
    image_preview.short_description = "Image Preview"
    
    def get_stock_quantity(self, obj):
        return obj.get_stock_quantity()
    get_stock_quantity.short_description = "Total Stock"


