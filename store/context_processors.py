from .models import Category, Product


def categories(request):
    """Add categories to all templates"""
    return {
        'categories': Category.objects.filter(is_active=True),
    }


def cart_count(request):
    """Add cart item count to all templates"""
    # This is a placeholder - implement actual cart logic later
    cart_count = 0
    if hasattr(request, 'session'):
        cart = request.session.get('cart', {})
        cart_count = sum(item.get('quantity', 0) for item in cart.values())
    return {
        'cart_count': cart_count,
    }

