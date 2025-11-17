from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Category, Product, ProductImage, BlogPost, 
    ContactMessage, NewsletterSubscriber, Review
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'image_url', 'alt_text', 'order', 'is_primary']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'stock_quantity', 
        'is_available', 'is_featured', 'rating', 'created_at'
    ]
    list_filter = [
        'category', 'is_available', 'is_featured', 'is_hot', 
        'created_at', 'category'
    ]
    search_fields = ['name', 'description', 'sku', 'tags']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['sku', 'rating', 'review_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'description', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_at_price')
        }),
        ('Images', {
            'fields': ('main_image', 'image_url')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'is_available')
        }),
        ('Product Attributes', {
            'fields': ('sizes', 'colors', 'weight', 'dimensions', 'materials', 'tags')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_hot', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('rating', 'review_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'is_primary', 'alt_text']
    list_filter = ['is_primary']
    search_fields = ['product__name', 'alt_text']
    ordering = ['product', 'order']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at', 'view_count', 'created_at']
    list_filter = ['is_published', 'published_at', 'created_at']
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_url')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status', 'notes', 'replied_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived']

    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_replied(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='replied', replied_at=timezone.now())
    mark_as_replied.short_description = "Mark selected messages as replied"

    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
    mark_as_archived.short_description = "Mark selected messages as archived"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'name', 'email', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['approve_reviews', 'disapprove_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "Disapprove selected reviews"
