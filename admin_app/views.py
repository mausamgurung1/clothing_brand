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


# Create your views here.


# Save Image To Another Server
def save_img_to_another_server(file_obj, text):
    url = "https://images.prathmeshsoni.works/images/?format=json"

    files=[
        # ('file',('demo.png',open('demo.png','rb'),'image/png'))
        ('file', (file_obj.name, text, file_obj.content_type))
    ]
    headers = {
        'Authorization': 'token 9202c558d91744d146cf96f4f9bf464240acfbb9',
        'Origin': 'https://images.prathmeshsoni.works',
        'Referer': f'{url}',
    }

    response = requests.request("POST", url, headers=headers, data={}, files=files)
    try:
        json_data = response.json()
        return json_data['file']
    except:
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
            url = save_img_to_another_server(images, images.file.read())

            if not product or not description or not images or not productsize:
                messages.error(request, 'Please enter all fields')
                return redirect('add_product')
            

            subproduct_obj = SubProduct.objects.create(product_id=product, description=description, image=url)
            subproduct_obj.product_size_color.set(productsize)
            subproduct_obj.save()
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

        # Validate required fields first
        if not description or not productsize:
            messages.error(request, 'Please enter all required fields')
            return redirect('edit_product', id=id)

        # Handle image upload if provided
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
                    product.image = url
                    messages.success(request, 'Product image updated successfully!')
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
        product.save()
        
        messages.success(request, 'Product updated successfully!')
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
        # print(product_id)
        # print(size_id)
        # print(color_id)
        # print(stock_quantity)
        if not product_id or not size_id or not color_id or not stock_quantity:
            messages.error(request, 'Please enter all fields')
            return redirect('edit_quantity', id=id)
        # elif size_id
        try:
            stock_obj = ProductSizeNColor.objects.get(product_id=product_id, size_id=size_id, color_id=color_id)
            stock_obj.stock_quantity = stock_quantity
            stock_obj.save()
        except ProductSizeNColor.DoesNotExist:
            stock_obj = ProductSizeNColor.objects.create(product_id=product_id, size_id=size_id, color_id=color_id, stock_quantity=stock_quantity)
            stock_obj.save()
        
    context = {
        'product':product,
        'sizeandcolor':sizeandcolor,
        'sizes':sizes,
        'colors':colors,

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
    products = Product.objects.all().order_by('-created_at').prefetch_related('subproduct_set', 'product_size_color_set')
    
    # Add stock information to each product
    product_list_with_stock = []
    for product in products:
        # Get all subproducts for this product
        subproducts = product.subproduct_set.all()
        # Calculate total stock across all size/color combinations
        total_stock = product.product_size_color_set.aggregate(total=Sum('stock_quantity'))['total'] or 0
        # Get low stock count
        low_stock_count = product.product_size_color_set.filter(stock_quantity__lt=10).count()
        # Get out of stock count
        out_of_stock_count = product.product_size_color_set.filter(stock_quantity=0).count()
        
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
    order = get_object_or_404(placeOrder, order_id=order_id)
    order_items = sub_placeorder.objects.filter(order_id=order)
  
    subtotal = sum([item.subproduct_id.product.price * item.quantity for item in order_items])
    shipping_charge = 50
    total = subtotal + shipping_charge

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
    order = get_object_or_404(placeOrder, order_id=order_id)
    order.delete()
    return redirect('order_list')


@login_required(login_url='/admin/login/?next=/admin_side/')
@csrf_exempt
def update_order_status(request, order_id):
    """Update order status"""
    if request.method == 'POST':
        try:
            order = get_object_or_404(placeOrder, order_id=order_id)
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