from django.db import models
from django.conf import settings
from django.templatetags.static import static
# from app.models import User
# Create your models here.
import requests

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_id = models.ImageField(upload_to='images/products/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f'{self.name} - {self.price} | {self.category}'
    
            
class Size(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = 'Sizes'
    def __str__(self):
        return self.name

    
class Color(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name_plural = 'Colors'
    def __str__(self):
        return self.name


class ProductSizeNColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = 'ProductSizeNColors'
    
    def __str__(self):
        return f'{self.product} - {self.size} | {self.color} | {self.stock_quantity}'


    
class SubProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images/products/', blank=True, null=True)
    product_size_color = models.ManyToManyField(ProductSizeNColor)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # sizes = models.ManyToManyField(Size, through='SizeSubProduct')

    def get_stock_quantity(self):
        return sum([psc.stock_quantity for psc in self.product_size_color.all()])
    
    class Meta:
            verbose_name_plural = 'SubProducts'
    def __str__(self):
        return f'{self.product}'
    
    @property
    def image_url(self):
        """
        Provides a reliable image URL with fallbacks for remote images,
        locally stored media files, or placeholder image.
        """
        potential_sources = [self.image]
        if self.product and getattr(self.product, 'image_id', None):
            potential_sources.append(self.product.image_id)

        for source in potential_sources:
            if not source:
                continue

            # Django FileField provides .url for stored files
            try:
                if hasattr(source, "url"):
                    return source.url
            except ValueError:
                # Happens when file is missing; fall back to manual handling
                pass

            image_path = str(source).strip()
            if not image_path:
                continue

            if image_path.startswith("http://") or image_path.startswith("https://"):
                return image_path

            if image_path.startswith("/"):
                return image_path

            # External CDN paths (images/...)
            if image_path.startswith("images/") and image_path.startswith("images/products/https") is False:
                media_prefix = settings.MEDIA_URL.rstrip("/")
                return f"{media_prefix}/{image_path.lstrip('/')}"

            if image_path.startswith("images/products/https"):
                # Some historical records saved full URL prefixed with images/products/
                cleaned = image_path.split("images/products/", 1)[-1]
                if cleaned.startswith("http"):
                    return cleaned

            # Default to MEDIA
            media_prefix = settings.MEDIA_URL.rstrip("/")
            return f"{media_prefix}/{image_path.lstrip('/')}"

        return static('img/empty_cart.png')
    
