from django.core.management.base import BaseCommand
from django.utils import timezone
from store.models import Category, Product, BlogPost
import random


class Command(BaseCommand):
    help = 'Create sample data for Baabuu Clothing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--products',
            type=int,
            default=20,
            help='Number of products to create',
        )
        parser.add_argument(
            '--blog-posts',
            type=int,
            default=5,
            help='Number of blog posts to create',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create Categories
        categories_data = [
            {'name': 'Women', 'description': 'Women\'s clothing collection'},
            {'name': 'Men', 'description': 'Men\'s clothing collection'},
            {'name': 'Bag', 'description': 'Bags and accessories'},
            {'name': 'Shoes', 'description': 'Footwear collection'},
            {'name': 'Watches', 'description': 'Watches and timepieces'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        
        # Sample product names and prices
        product_samples = [
            {'name': 'Esprit Ruffle Shirt', 'price': 16.64, 'category': 'Women'},
            {'name': 'Herschel supply', 'price': 35.31, 'category': 'Women'},
            {'name': 'Only Check Trouser', 'price': 25.50, 'category': 'Men'},
            {'name': 'Classic Trench Coat', 'price': 75.00, 'category': 'Women'},
            {'name': 'Front Pocket Jumper', 'price': 34.75, 'category': 'Women'},
            {'name': 'Vintage Inspired Classic', 'price': 93.20, 'category': 'Watches'},
            {'name': 'Shirt in Stretch Cotton', 'price': 52.66, 'category': 'Women'},
            {'name': 'Pieces Metallic Printed', 'price': 18.96, 'category': 'Women'},
            {'name': 'Converse All Star Hi Plimsolls', 'price': 75.00, 'category': 'Shoes'},
            {'name': 'Femme T-Shirt In Stripe', 'price': 25.85, 'category': 'Women'},
            {'name': 'Herschel supply', 'price': 63.16, 'category': 'Men'},
            {'name': 'T-Shirt with Sleeve', 'price': 18.49, 'category': 'Women'},
            {'name': 'Pretty Little Thing', 'price': 54.79, 'category': 'Women'},
            {'name': 'Mini Silver Mesh Watch', 'price': 86.85, 'category': 'Watches'},
            {'name': 'Square Neck Back', 'price': 29.64, 'category': 'Women'},
        ]
        
        # Create Products
        product_count = options['products']
        for i in range(product_count):
            sample = random.choice(product_samples)
            category = categories[sample['category']]
            
            # Generate image URL from existing static images
            image_num = (i % 16) + 1
            image_url = f'/static/images/product-{image_num:02d}.jpg'
            
            product, created = Product.objects.get_or_create(
                name=f"{sample['name']} #{i+1}" if i >= len(product_samples) else sample['name'],
                defaults={
                    'description': f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                 f"Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                                 f"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
                    'short_description': f"High quality {sample['name'].lower()}",
                    'price': sample['price'] + random.uniform(-5, 10),
                    'category': category,
                    'image_url': image_url,
                    'stock_quantity': random.randint(10, 100),
                    'is_available': True,
                    'is_featured': random.choice([True, False, False]),  # 1/3 chance
                    'is_hot': random.choice([True, False, False, False]),  # 1/4 chance
                    'sizes': 'S,M,L,XL',
                    'colors': 'Black,Blue,Grey,White',
                    'weight': round(random.uniform(0.1, 2.0), 2),
                    'dimensions': f"{random.randint(80, 120)} x {random.randint(30, 50)} x {random.randint(80, 120)} cm",
                    'materials': '60% cotton, 40% polyester',
                    'tags': 'Fashion,Lifestyle,Denim',
                    'rating': round(random.uniform(3.5, 5.0), 2),
                    'review_count': random.randint(0, 50),
                    'published_at': timezone.now(),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
        
        # Create Blog Posts
        blog_samples = [
            {
                'title': 'The Ultimate Guide to Fashion Trends 2024',
                'excerpt': 'Discover the latest fashion trends that will dominate 2024.',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
                'image_url': '/static/images/blog-01.jpg',
            },
            {
                'title': 'How to Style Your Wardrobe Like a Pro',
                'excerpt': 'Learn professional styling tips to elevate your fashion game.',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
                'image_url': '/static/images/blog-02.jpg',
            },
            {
                'title': 'Sustainable Fashion: A Complete Guide',
                'excerpt': 'Understanding sustainable fashion and making eco-friendly choices.',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
                'image_url': '/static/images/blog-03.jpg',
            },
            {
                'title': 'Men\'s Fashion Essentials for Every Season',
                'excerpt': 'Essential clothing items every man should have in his wardrobe.',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
                'image_url': '/static/images/blog-04.jpg',
            },
            {
                'title': 'Accessorizing: The Art of Completing Your Look',
                'excerpt': 'How to choose and style accessories to complete your outfit.',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
                'image_url': '/static/images/blog-05.jpg',
            },
        ]
        
        blog_count = options['blog_posts']
        for i in range(min(blog_count, len(blog_samples))):
            sample = blog_samples[i]
            post, created = BlogPost.objects.get_or_create(
                title=sample['title'],
                defaults={
                    'author': 'Fashion Editor',
                    'content': sample['content'] * 5,  # Make it longer
                    'excerpt': sample['excerpt'],
                    'image_url': sample['image_url'],
                    'is_published': True,
                    'published_at': timezone.now() - timezone.timedelta(days=i),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created blog post: {post.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created sample data!'))
        self.stdout.write(self.style.SUCCESS(f'Categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Products: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Blog Posts: {BlogPost.objects.count()}'))

