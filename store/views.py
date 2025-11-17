from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Product, Category, BlogPost, ContactMessage, NewsletterSubscriber, Review
from .forms import ContactForm, NewsletterForm, ReviewForm


def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(
        is_featured=True, 
        is_available=True
    )[:8]
    
    hot_products = Product.objects.filter(
        is_hot=True, 
        is_available=True
    )[:4]
    
    categories = Category.objects.filter(is_active=True)[:3]
    
    context = {
        'featured_products': featured_products,
        'hot_products': hot_products,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)


def home02(request):
    """Alternative home page 2"""
    return home(request)  # Can be customized later


def home03(request):
    """Alternative home page 3"""
    return home(request)  # Can be customized later


def product_list(request):
    """Product listing page with filtering"""
    products = Product.objects.filter(is_available=True)
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)
    else:
        category = None
    
    # Search filter
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Tag filter
    tag = request.GET.get('tag')
    if tag:
        products = products.filter(tags__icontains=tag)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'rating':
        products = products.order_by('-rating', '-review_count')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
        'tag': tag,
        'sort_by': sort_by,
    }
    return render(request, 'store/product.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Related products (same category)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    # Reviews
    reviews = Review.objects.filter(product=product, is_approved=True)[:10]
    
    # Review form
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, 'Thank you! Your review has been submitted and is pending approval.')
            return redirect('product_detail', slug=slug)
    else:
        review_form = ReviewForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'store/product-detail.html', context)


def blog_list(request):
    """Blog listing page"""
    posts = BlogPost.objects.filter(is_published=True)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'search_query': search_query,
    }
    return render(request, 'store/blog.html', context)


def blog_detail(request, slug):
    """Blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    # Related posts (latest posts)
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'store/blog-detail.html', context)


def about(request):
    """About page"""
    return render(request, 'store/about.html')


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'store/contact.html', context)


def shopping_cart(request):
    """Shopping cart page"""
    return render(request, 'store/shoping-cart.html')


def newsletter_subscribe(request):
    """Newsletter subscription AJAX endpoint"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
        else:
            return JsonResponse({
                'success': False, 
                'message': form.errors.get('email', ['Invalid email address'])[0]
            })
    return JsonResponse({'success': False, 'message': 'Invalid request'})
