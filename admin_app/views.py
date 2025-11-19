from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect

from django.views.decorators.csrf import csrf_exempt
from app.models import *
from admin_app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.db.models import Sum, Q, Count, F
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
import json
import requests


# Create your views here.


# Save Image To Another Server
def save_img_to_another_server(file_obj, text):
    """
    Upload image to external server
    Returns the image URL on success, empty string on failure
    """
    if not file_obj or not text:
        return ''
    
    url = "https://images.prathmeshsoni.works/images/?format=json"

    try:
        files = [
            ('file', (file_obj.name, text, file_obj.content_type or 'image/jpeg'))
        ]
        headers = {
            'Authorization': 'token 9202c558d91744d146cf96f4f9bf464240acfbb9',
            'Origin': 'https://images.prathmeshsoni.works',
            'Referer': url,
        }

        response = requests.post(url, headers=headers, data={}, files=files, timeout=30)
        response.raise_for_status()  # Raise exception for bad status codes
        
        try:
            json_data = response.json()
            print(f"Full JSON response from image server: {json_data}")
            if 'file' in json_data:
                image_url = json_data['file']
                # Log the returned URL for debugging
                print(f"Image upload successful. Server returned URL: {image_url}")
                print(f"URL type: {type(image_url)}, Length: {len(str(image_url))}")
                return image_url
            else:
                print(f"Image upload response missing 'file' key. Available keys: {list(json_data.keys())}")
                print(f"Full response: {json_data}")
                return ''
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response content: {response.text[:200]}")
            return ''
    except requests.exceptions.RequestException as e:
        print(f"Error uploading image to server: {e}")
        return ''
    except Exception as e:
        print(f"Unexpected error in image upload: {e}")
        return ''


def add_product(request):
    if request.method == 'POST':
        if 'product_form' in request.POST:
            product_name = request.POST.get('product_name')
            product_price = request.POST.get('product_price')
            category = request.POST.get('category')

            if not product_name or not product_price or not category:
                messages.error(request, 'Please enter all fields')
                return redirect('add_product')
            
            product_obj = Product.objects.create(name=product_name, price=product_price, category_id=category)
            product_obj.save()
        elif 'sub_product_form' in request.POST:
            product = request.POST.get('product')
            description = request.POST.get('description')
            images = request.FILES.get('images')

            productsize = request.POST.getlist('productsize')

            if not product or not description or not productsize:
                messages.error(request, 'Please enter all required fields')
                return redirect('add_product')
            
            if not images:
                messages.error(request, 'Please select an image')
                return redirect('add_product')
            
            # Validate image file
            if images.size > 10 * 1024 * 1024:  # 10MB limit
                messages.error(request, 'Image file is too large. Maximum size is 10MB')
                return redirect('add_product')
            
            # Validate image type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if images.content_type not in allowed_types:
                messages.error(request, 'Invalid image format. Please upload JPEG, PNG, GIF, or WebP')
                return redirect('add_product')
            
            # Read image file content
            try:
                if hasattr(images, 'read'):
                    image_content = images.read()
                    # Reset file pointer for potential re-reading
                    if hasattr(images, 'seek'):
                        images.seek(0)
                else:
                    messages.error(request, 'Error reading image file')
                    return redirect('add_product')
            except Exception as e:
                messages.error(request, f'Error reading image file: {str(e)}')
                return redirect('add_product')
            
            # Upload image to external server
            url = save_img_to_another_server(images, image_content)
            
            if not url or url.strip() == '':
                messages.error(request, 'Failed to upload image. Please try again.')
                return redirect('add_product')

            # Ensure the URL is stored correctly
            # If the server returns a full URL, use it; otherwise prepend the base URL
            if not url.startswith('http'):
                # If it's a relative path starting with images/, prepend the server URL
                if url.startswith('images/'):
                    image_url = f'https://images.prathmeshsoni.works/{url}'
                else:
                    image_url = url
            else:
                image_url = url

            subproduct_obj = SubProduct.objects.create(product_id=product, description=description, image=image_url)
            subproduct_obj.product_size_color.set(productsize)
            subproduct_obj.save()
            messages.success(request, f'Product added successfully! Image URL: {image_url[:50]}...')
        elif 'size_form' in request.POST:
            product = request.POST.get('product')
            size = request.POST.get('sizes')
            color = request.POST.get('colors')
            quantity = request.POST.get('stock')
            
                       
            if not product or not size or not color or not quantity:
                messages.error(request, 'Please enter all fields')
                return redirect('add_product')  
            elif ProductSizeNColor.objects.filter(product_id=product, size_id=size, color_id=color).exists():
                messages.error(request, 'Size and color is  already exists', extra_tags='size_exists')
                return redirect('add_product')
            
            size_obj = ProductSizeNColor.objects.create(product_id=product, size_id=size, color_id=color, stock_quantity=quantity)
            size_obj.save()


    categories = Category.objects.all()
    product = Product.objects.all()
    size = Size.objects.all()
    color = Color.objects.all()
    sizeandcolor__ = ProductSizeNColor.objects.all()
    
    # print(sizeandcolor__)


    context = {
        'categories':categories,
        'products':product,
        'sizes':size,
        'colors':color,
        'sizeandcolor':sizeandcolor__,
    }

    return render(request, 'add_product.html',context)


def edit_product(request, id):
    product = SubProduct.objects.get(id=id)
    sizeandcolor = ProductSizeNColor.objects.all()
    # print(sizeandcolor)

    excluded_sizes = product.product_size_color.all()
    # print(excluded_sizes)
    available_sizes = sizeandcolor.exclude(id__in=excluded_sizes)

    size_color = product.product_size_color.all()
    # print(product.product_size_color.all())

    if request.method == 'POST':
        description = request.POST.get('description')
        productsize = request.POST.getlist('productsize')
        image = request.FILES.get('images')
        remove_image = request.POST.get('remove_image', '0') == '1'
        image_updated = False
        image_url_saved = ''

        # Validate required fields first
        if not description or not productsize:
            messages.error(request, 'Please enter all required fields')
            return redirect('edit_product', id=id)

        # Handle image removal if requested
        if remove_image:
            product.image = ''
            from django.utils import timezone
            product.updated_at = timezone.now()
            product.save()
            product.refresh_from_db()
            print(f"Image removed for product {product.id}")
            messages.success(request, 'Product image removed successfully!')
        
        # Handle image upload if provided (this will override remove if both are set)
        if image is not None and image.size > 0:
            try:
                # Read the file content
                # Reset file pointer to beginning in case it was read before
                if hasattr(image, 'seek'):
                    image.seek(0)
                
                # Read file content - try different methods for compatibility
                if hasattr(image, 'read'):
                    image_content = image.read()
                elif hasattr(image, 'file') and hasattr(image.file, 'read'):
                    image_content = image.file.read()
                else:
                    # Fallback: read chunks
                    image_content = b''
                    for chunk in image.chunks():
                        image_content += chunk
                
                # Upload image to server
                url = save_img_to_another_server(image, image_content)
                
                # Only update image if upload was successful
                if url and url.strip() and url != '':
                    # Ensure the URL is stored correctly
                    # If the server returns a full URL, use it; otherwise prepend the base URL
                    if not url.startswith('http'):
                        # If it's a relative path starting with images/, prepend the server URL
                        if url.startswith('images/'):
                            image_url = f'https://images.prathmeshsoni.works/{url}'
                        else:
                            image_url = url
                    else:
                        image_url = url
                    
                    old_image = product.image
                    product.image = image_url
                    # Force update the updated_at timestamp for cache-busting
                    from django.utils import timezone
                    product.updated_at = timezone.now()
                    product.save()
                    product.refresh_from_db()
                    
                    # Verify the save
                    verify_product = SubProduct.objects.get(id=product.id)
                    print(f"Image updated in edit_product for product {product.id}:")
                    print(f"  Old URL: {old_image}")
                    print(f"  New URL: {verify_product.image}")
                    print(f"  Updated at: {verify_product.updated_at}")
                    print(f"  Verification: URLs match = {verify_product.image == image_url}")
                    
                    image_updated = True
                    image_url_saved = image_url
                    messages.success(request, 'Product image updated successfully!')
                    messages.info(request, f'New image URL: {image_url[:80]}...')
                else:
                    messages.warning(request, 'Image upload failed. Please try again or keep existing image.')
            except Exception as e:
                import traceback
                print(f"Error uploading image: {str(e)}")
                print(traceback.format_exc())
                messages.error(request, f'Error uploading image: {str(e)}')
                # Keep existing image if upload fails
        
        # Update product details
        product.description = description
        size = productsize + list(size_color)   
        product.product_size_color.set(size)
        
        # Refresh product from database to get latest image and updated_at after POST
        product.refresh_from_db()
        product.save()
        
        messages.success(request, 'Product updated successfully!')
        
        # If image was updated, redirect back to edit page to show new image
        if image_updated and image_url_saved:
            return redirect('edit_product', id=id)
        
        return redirect('allproduct')
    
    

    context = {
        'product': product,
        'sizeandcolor':available_sizes,



    }
    return render(request, 'edit_product.html', context)

def edit_quantity(request,id):
    product = SubProduct.objects.get(id=id)
    # print(product)
    sizeandcolor = ProductSizeNColor.objects.filter(product=product.product_id)
    # print(sizeandcolor)

    unique_sizes = [size.size for size in sizeandcolor]
    sizes = set(unique_sizes)
    # print(sizes)

    unique_colors = [color.color for color in sizeandcolor]
    colors = set(unique_colors)
    # print(colors)


    if request.method == 'POST':
        product_id = request.POST.get('product')
        size_id = request.POST.get('sizes')
        color_id = request.POST.get('colors')
        stock_quantity = request.POST.get('stock')
        image = request.FILES.get('images')
        remove_image = request.POST.get('remove_image', '0') == '1'
        
        # Handle image removal ONLY if no new image is being uploaded
        # If both remove and upload are selected, upload takes precedence (don't remove)
        image_uploaded = False
        if remove_image and (image is None or image.size == 0):
            product.image = ''
            from django.utils import timezone
            product.updated_at = timezone.now()
            product.save()
            product.refresh_from_db()
            print(f"Image removed for product {product.id}")
            messages.success(request, 'Product image removed successfully!')
        
        # Handle image upload if provided (this will override remove if both are set)
        if image is not None and image.size > 0:
            try:
                # Validate image file
                if image.size > 10 * 1024 * 1024:  # 10MB limit
                    messages.error(request, 'Image file is too large. Maximum size is 10MB')
                    return redirect('edit_quantity', id=id)
                
                # Validate image type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if image.content_type not in allowed_types:
                    messages.error(request, 'Invalid image format. Please upload JPEG, PNG, GIF, or WebP')
                    return redirect('edit_quantity', id=id)
                
                # Read image file content
                if hasattr(image, 'read'):
                    image_content = image.read()
                    # Reset file pointer for potential re-reading
                    if hasattr(image, 'seek'):
                        image.seek(0)
                else:
                    messages.error(request, 'Error reading image file')
                    return redirect('edit_quantity', id=id)
                
                # Upload image to external server
                url = save_img_to_another_server(image, image_content)
                
                # Only update image if upload was successful
                if url and url.strip() and url != '':
                    old_image = product.image
                    # Ensure the URL is stored correctly
                    # If the server returns a full URL, use it; otherwise prepend the base URL
                    if not url.startswith('http'):
                        # If it's a relative path starting with images/, prepend the server URL
                        if url.startswith('images/'):
                            image_url = f'https://images.prathmeshsoni.works/{url}'
                        else:
                            image_url = url
                    else:
                        image_url = url
                    
                    # Update the product image
                    product.image = image_url
                    # Force update the updated_at timestamp for cache-busting
                    from django.utils import timezone
                    product.updated_at = timezone.now()
                    product.save()
                    # Force refresh to ensure it's persisted
                    product.refresh_from_db()
                    
                    # Verify the save
                    verify_product = SubProduct.objects.get(id=product.id)
                    print(f"Image updated for product {product.id}:")
                    print(f"  Old URL: {old_image}")
                    print(f"  New URL: {verify_product.image}")
                    print(f"  Updated at: {verify_product.updated_at}")
                    print(f"  Verification: URLs match = {verify_product.image == image_url}")
                    
                    image_uploaded = True
                    messages.success(request, f'Product image updated successfully!')
                    messages.info(request, f'New image URL: {image_url[:80]}...')
                else:
                    print(f"Image upload failed for product {product.id}: Empty URL returned")
                    print(f"Server response URL: {url if url else 'None'}")
                    messages.warning(request, 'Image upload failed. Please try again or keep existing image.')
            except Exception as e:
                import traceback
                print(f"Error uploading image: {str(e)}")
                print(traceback.format_exc())
                messages.error(request, f'Error uploading image: {str(e)}')
                # Keep existing image if upload fails
        
        # Check if only image was updated/removed (no stock fields provided)
        image_only_update = (image_uploaded or remove_image) and (not product_id or not size_id or not color_id or not stock_quantity)
        
        # If only image was updated/removed, redirect to show the change
        if image_only_update:
            if image_uploaded:
                messages.info(request, 'Image updated successfully! If you want to update stock, please fill in all stock fields.')
            elif remove_image:
                messages.info(request, 'Image removed successfully! If you want to update stock, please fill in all stock fields.')
            return redirect('edit_quantity', id=id)
        
        # If stock fields are provided, validate and update stock
        if not product_id or not size_id or not color_id or not stock_quantity:
            messages.error(request, 'Please enter all fields (size, color, and stock quantity)')
            return redirect('edit_quantity', id=id)
        
        # Validate stock quantity is a positive integer
        try:
            stock_quantity = int(stock_quantity)
            if stock_quantity < 0:
                messages.error(request, 'Stock quantity must be a positive number')
                return redirect('edit_quantity', id=id)
        except ValueError:
            messages.error(request, 'Stock quantity must be a valid number')
            return redirect('edit_quantity', id=id)
        
        try:
            size_obj = Size.objects.get(id=size_id)
            color_obj = Color.objects.get(id=color_id)
        except (Size.DoesNotExist, Color.DoesNotExist):
            messages.error(request, 'Invalid size or color selected')
            return redirect('edit_quantity', id=id)
        
        try:
            stock_obj = ProductSizeNColor.objects.get(product_id=product_id, size_id=size_id, color_id=color_id)
            old_stock = stock_obj.stock_quantity
            stock_obj.stock_quantity = stock_quantity
            stock_obj.save()
            messages.success(request, f'Stock updated successfully! {size_obj.name} / {color_obj.name}: {old_stock} → {stock_quantity}')
        except ProductSizeNColor.DoesNotExist:
            stock_obj = ProductSizeNColor.objects.create(product_id=product_id, size_id=size_id, color_id=color_id, stock_quantity=stock_quantity)
            stock_obj.save()
            messages.success(request, f'New stock entry created! {size_obj.name} / {color_obj.name}: {stock_quantity}')
    
    # Refresh product from database to get latest image and updated_at after POST
    if request.method == 'POST':
        product.refresh_from_db()
        # Re-fetch related data
        sizeandcolor = ProductSizeNColor.objects.filter(product=product.product_id)
        unique_sizes = [size.size for size in sizeandcolor]
        sizes = set(unique_sizes)
        unique_colors = [color.color for color in sizeandcolor]
        colors = set(unique_colors)
    
    context = {
        'product': product,
        'sizeandcolor': sizeandcolor,
        'sizes': sizes,
        'colors': colors,
    }

    return render(request, 'edit_quantity.html', context)



def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if not category_name:
            messages.error(request, 'Please enter a category')
            return redirect('add_category')
        else:
            category_obj = Category.objects.filter(name=category_name)
            if category_obj.exists():
                messages.error(request, 'Category already exists')
                return redirect('add_category')
        category_obj = Category.objects.create(name=category_name)
        category_obj.save()
    return render(request, 'add_category.html')

def add_size(request):
    if request.method == 'POST':
        size_name = request.POST.get('size_name')

        if not size_name:
            messages.error(request, 'Please enter a size')
            return redirect('add_size')
        else:
            size_obj = Size.objects.filter(name=size_name)
            if size_obj.exists():
                messages.error(request, 'Size already exists')
                return redirect('add_size')
        
        size_obj = Size.objects.create(name=size_name)
        size_obj.save()
    return render(request, 'add_size.html')

def add_color(request):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        if not color_name:
            messages.error(request, 'Please enter a color')
            return redirect('add_color')
        else:
            color_obj = Color.objects.filter(name=color_name)
            if color_obj.exists():
                messages.error(request, 'Color already exists')
                return redirect('add_color')
            
        color_obj = Color.objects.create(name=color_name)
        color_obj.save()
    return render(request, 'add_color.html')




@csrf_exempt
def getcolor(request):
    size_id = request.GET.get('size_id')
    product_id = request.GET.get('product_id')
    
    colors = ProductSizeNColor.objects.filter(size_id=size_id, product_id=product_id)
    
    data = [{'id': color.color.id, 'name': color.color.name} for color in colors]
    
    return JsonResponse({'colors': data})

@csrf_exempt
def getstock(request):
    product_id = request.GET.get('product_id')
    size_id = request.GET.get('size_id')
    color_id = request.GET.get('color_id')
    
    try:
        stock_obj = ProductSizeNColor.objects.get(product_id=product_id, size_id=size_id, color_id=color_id)
        stock = stock_obj.stock_quantity
    except ProductSizeNColor.DoesNotExist:
        stock = 0
    return JsonResponse({'stock':stock})



@login_required(login_url='/admin/login/?next=/admin_side/')
def remove_product(request, id):
    product = SubProduct.objects.get(id=id)
    product.delete()
    return redirect('allproduct')


@login_required(login_url='/admin/login/?next=/admin_side/')
def allproduct(request):
    products = SubProduct.objects.all().order_by('-created_at').select_related('product', 'product__category').prefetch_related('product_size_color')
   
    # Add stock information to each product
    for product in products:
        product.total_stock = product.get_stock_quantity()
        product.low_stock_variants = product.product_size_color.filter(stock_quantity__lt=10, stock_quantity__gt=0).count()
        product.out_of_stock_variants = product.product_size_color.filter(stock_quantity=0).count()
        product.variant_count = product.product_size_color.count()
   
    context = {
        'products': products,
    }
    return render(request, 'all_product.html', context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def remove_products(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product_list')


@login_required(login_url='/admin/login/?next=/admin_side/')
def product_list(request):
    # Get all products with their stock information
    products = Product.objects.all().order_by('-created_at').prefetch_related('subproduct_set')
    
    # Add stock information to each product
    product_list_with_stock = []
    for product in products:
        # Get all subproducts for this product
        subproducts = product.subproduct_set.all()
        
        # Get all ProductSizeNColor objects for this product using reverse ForeignKey relation
        # Django auto-generates reverse relation as productsizencolor_set (all lowercase)
        size_color_combos = product.productsizencolor_set.all()
        
        # Calculate total stock across all size/color combinations
        total_stock = size_color_combos.aggregate(total=Sum('stock_quantity'))['total'] or 0
        
        # Get low stock count (stock < 10 but > 0)
        low_stock_count = size_color_combos.filter(stock_quantity__lt=10, stock_quantity__gt=0).count()
        
        # Get out of stock count (stock = 0)
        out_of_stock_count = size_color_combos.filter(stock_quantity=0).count()
        
        product_list_with_stock.append({
            'product': product,
            'total_stock': total_stock,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'subproducts': subproducts,
        })
    
    context = {
        'products': product_list_with_stock,
    }
    return render(request, 'product_list.html', context)

@login_required(login_url='/admin/login/?next=/admin_side/')
def admin_side(request):
    return redirect('admin_dashboard')

@staff_member_required
def admin_logout(request):
    logout(request)
    return redirect('admin_side')

@login_required(login_url='/admin/login/?next=/admin_side/')
def user_list(request):
    users = User.objects.all().order_by('-created_at')
    context = {
        'users':users,
    }
    return render(request, 'user_list.html', context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def order_list(request):
    orders = placeOrder.objects.all().order_by('-order_date')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    
    # Get counts for filter tabs
    total_orders = placeOrder.objects.all().count()
    pending_count = placeOrder.objects.filter(order_status='Pending').count()
    delivered_count = placeOrder.objects.filter(order_status='Delivered').count()
    cancelled_count = placeOrder.objects.filter(order_status='Cancelled').count()
    returned_count = placeOrder.objects.filter(order_status='Returned').count()
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'total_orders': total_orders,
        'pending_count': pending_count,
        'delivered_count': delivered_count,
        'cancelled_count': cancelled_count,
        'returned_count': returned_count,
    }
    return render(request, 'order_list.html', context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at')
    # print(contacts)
    
    context = {
        'contacts':contacts,
    }
    return render(request, 'contact_list.html', context)

@login_required(login_url='/admin/login/?next=/admin_side/')
def order_detail(request, order_id):
    try:
        # First try to find by order_id field
        order = placeOrder.objects.get(order_id=order_id)
    except placeOrder.DoesNotExist:
        # If not found by order_id, try by primary key (for backward compatibility)
        try:
            order = placeOrder.objects.get(id=order_id)
        except placeOrder.DoesNotExist:
            messages.error(request, f'Order #{order_id} not found.')
            return redirect('order_list')
    
    order_items = sub_placeorder.objects.filter(order_id=order)
  
    subtotal = sum([item.subproduct_id.product.price * item.quantity for item in order_items])
    shipping_charge = order.shipping_charge if order.shipping_charge else 50
    total = order.total_amount if order.total_amount else (subtotal + shipping_charge)

    context = {
        'order': order,
        'order_items': order_items,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'total': total,
    }
    return render(request, 'order_detail.html', context)


@login_required(login_url='/admin/login/?next=/admin_side/')
def order_delete(request, order_id):
    try:
        # First try to find by order_id field
        order = placeOrder.objects.get(order_id=order_id)
    except placeOrder.DoesNotExist:
        # If not found by order_id, try by primary key
        try:
            order = placeOrder.objects.get(id=order_id)
        except placeOrder.DoesNotExist:
            messages.error(request, f'Order #{order_id} not found.')
            return redirect('order_list')
    
    order_id_value = order.order_id  # Store before deletion
    order.delete()
    messages.success(request, f'Order #{order_id_value} has been deleted successfully.')
    return redirect('order_list')


@login_required(login_url='/admin/login/?next=/admin_side/')
@csrf_exempt
def update_order_status(request, order_id):
    """Update order status"""
    if request.method == 'POST':
        try:
            # First try to find by order_id field
            try:
                order = placeOrder.objects.get(order_id=order_id)
            except placeOrder.DoesNotExist:
                # If not found by order_id, try by primary key
                try:
                    order = placeOrder.objects.get(id=order_id)
                except placeOrder.DoesNotExist:
                    messages.error(request, f'Order #{order_id} not found.')
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': f'Order #{order_id} not found.'}, status=404)
                    return redirect('order_list')
            
            new_status = request.POST.get('status')
            
            # Validate status
            valid_statuses = ['Pending', 'Delivered', 'Cancelled', 'Returned']
            if new_status in valid_statuses:
                old_status = order.order_status
                order.order_status = new_status
                order.save()
                
                messages.success(request, f'Order #{order.order_id} status updated from {old_status} to {new_status}')
                
                # If updating via AJAX, return JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f'Status updated to {new_status}',
                        'status': new_status
                    })
            else:
                messages.error(request, 'Invalid order status')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid order status'
                    }, status=400)
        except Exception as e:
            messages.error(request, f'Error updating order status: {str(e)}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                }, status=500)
    
    # Redirect back to order detail or list
    redirect_url = request.POST.get('redirect_url', 'order_list')
    if redirect_url == 'order_detail':
        return redirect('order_detail', order_id=order_id)
    return redirect('order_list')


def redirect_to_admin(request):
    return redirect('admin_dashboard')

def admin_logout(request):
    logout(request)
    return redirect('admin_side')

@login_required(login_url='/admin/login/?next=/admin_side/')
def admin_dashboard(request):
    # Basic statistics
    total_booking = placeOrder.objects.all().count()
    total_user = User.objects.all().count()
    total_product = SubProduct.objects.all().count()
    
    # Calculate total earning (handle None values)
    total_earning = placeOrder.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # Order status counts
    return_order = placeOrder.objects.filter(order_status='Returned').count()
    cancel_order = placeOrder.objects.filter(order_status='Cancelled').count()
    delivered_order = placeOrder.objects.filter(order_status='Delivered').count()
    pending_order = placeOrder.objects.filter(order_status='Pending').count()
    
    # Recent statistics (last 30 days)
    last_30_days = datetime.now() - timedelta(days=30)
    orders_last_month = placeOrder.objects.filter(order_date__gte=last_30_days).count()
    earning_last_month = placeOrder.objects.filter(
        order_date__gte=last_30_days
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Growth calculations
    orders_growth = ((orders_last_month / total_booking * 100) if total_booking > 0 else 0) if orders_last_month > 0 else 0
    earning_growth = ((earning_last_month / total_earning * 100) if total_earning > 0 else 0) if earning_last_month > 0 else 0
    
    # Recent orders (last 10)
    recent_orders = placeOrder.objects.all().order_by('-order_date')[:10]
    
    # Low stock products (stock < 10)
    low_stock_products = ProductSizeNColor.objects.filter(stock_quantity__lt=10)[:5]
    low_stock_count = ProductSizeNColor.objects.filter(stock_quantity__lt=10).count()
    
    # Category-wise statistics
    category_stats = Category.objects.annotate(
        product_count=Count('product__subproduct'),
        order_count=Count('product__subproduct__sub_placeorder__order_id', distinct=True)
    )
    
    # Monthly data for charts
    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year, 12, 31)
    
    man_purchases = sub_placeorder.objects.filter(
        subproduct_id__product_id__category__name__icontains='Man',
        created_at__range=(start_date, end_date)
    ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('quantity')).values('month', 'total')

    woman_purchases = sub_placeorder.objects.filter(
        subproduct_id__product__category__name__icontains='Woman',
        created_at__range=(start_date, end_date)
    ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('quantity')).values('month', 'total')

    kid_purchases = sub_placeorder.objects.filter(
        subproduct_id__product__category__name__icontains='Kid',
        created_at__range=(start_date, end_date)
    ).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('quantity')).values('month', 'total')

    def format_monthly_data(queryset):
        monthly_data = {i: 0 for i in range(1, 13)}
        for item in queryset:
            monthly_data[item['month'].month] = item['total']
        return [monthly_data[i] for i in range(1, 13)]

    man_purchases_monthly = format_monthly_data(man_purchases)
    woman_purchases_monthly = format_monthly_data(woman_purchases)
    kid_purchases_monthly = format_monthly_data(kid_purchases)

    total_earning_monthly = placeOrder.objects.filter(
        order_date__range=(start_date, end_date)
    ).annotate(month=TruncMonth('order_date')).values('month').annotate(total=Sum('total_amount')).values('month', 'total')

    total_earning_Monthly = format_monthly_data(total_earning_monthly)
    
    context = {
        'total_booking': total_booking,
        'total_user': total_user,
        'total_product': total_product,
        'total_earning': total_earning,
        'return_order': return_order,
        'cancel_order': cancel_order,
        'delivered_order': delivered_order,
        'pending_order': pending_order,
        'orders_last_month': orders_last_month,
        'earning_last_month': earning_last_month,
        'orders_growth': round(orders_growth, 1),
        'earning_growth': round(earning_growth, 1),
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'low_stock_count': low_stock_count,
        'category_stats': category_stats,
        'man_purchases_monthly': json.dumps(man_purchases_monthly),
        'woman_purchases_monthly': json.dumps(woman_purchases_monthly),
        'kids_purchases_monthly': json.dumps(kid_purchases_monthly), 
        'total_earning_Monthly': json.dumps(total_earning_Monthly),
    }
    return render(request, 'admin_dashboard.html', context)





@csrf_exempt
def get_product_sizencolor(requset):
    product_id = requset.POST.get('id')
    product = Product.objects.get(id=product_id)
    productsizecolor = ProductSizeNColor.objects.filter(product=product)
    data = []
    for sizecolor in productsizecolor:
        product_name = f'{sizecolor.product.name} - {sizecolor.size.name}-{sizecolor.color.name}'
        data.append({
            'product_name':product_name,
            'id':sizecolor.id
        })
    a = {'list':data}
    return JsonResponse(a, safe=False)


@csrf_exempt
def edit_product_sizencolor(request):
    product_id = request.POST.get('id')
    selected_size_ids = request.POST.getlist('selected_sizes')  # Get the selected size IDs

    product = Product.objects.get(id=product_id)
    product_size_colors = ProductSizeNColor.objects.filter(product=product)
    data = []
    for sizecolor in product_size_colors:
        product_name = f' {sizecolor.product.name} - {sizecolor.size.name} - {sizecolor.color.name}'
        data.append({
            'product_name': product_name,
            'id': sizecolor.id
        })

    response_data = {'list': data}
    return JsonResponse(response_data, safe=False)