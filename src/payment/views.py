import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone

from .models import Payment
from app.models import User, Cart, AddressModel, sub_placeorder, placeOrder
# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment_intent(request):
    """Create Stripe Payment Intent"""
    if request.method != 'POST' or 'user' not in request.session:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        user = User.objects.get(pk=request.session['user'])
        cart = Cart.objects.filter(uname=user)

        # Calculate total in cents
        total_usd = sum((item.total_price_usd or item.quantity * 10) for item in cart) + 1
        amount_cents = int(total_usd * 100)

        # Create Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            metadata={
                'user_id': user.id,
                'user_email': user.email
            }
        )

        return JsonResponse({
            'clientSecret': intent.client_secret,
            'amount': total_usd
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def create_paypal_order(request):
    """Store PayPal order details"""
    if request.method != 'POST' or 'user' not in request.session:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

    try:
        data = json.loads(request.body)
        user = User.objects.get(pk=request.session['user'])
        cart = Cart.objects.filter(uname=user)

        total_usd = sum((item.total_price_usd or item.quantity * 10) for item in cart) + 1

        request.session['pending_order'] = {
            'user_id': user.id,
            'total_usd': round(total_usd, 2),
            'method': 'paypal',
            'payment_id': data.get('orderID', '')
        }

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def capture_paypal_order(request):
    """Capture PayPal payment and create order"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    try:
        data = json.loads(request.body)
        payment_data = request.session.get('pending_order')

        if not payment_data:
            return JsonResponse({'success': False, 'error': 'No pending order'})

        user = User.objects.get(pk=payment_data['user_id'])
        cart_items = Cart.objects.filter(uname=user)

        # Create order
        order = placeOrder.objects.create(
            user_id=user,
            address_id=AddressModel.objects.filter(user_id=user).first(),
            order_date=timezone.now().date(),
            payment_mode='PAYPAL',
            total_amount=payment_data['total_usd'],
            shipping_charge=1,
            total_quantity=sum(i.quantity for i in cart_items),
            order_status='Paid'
        )

        # Save order items
        for item in cart_items:
            sub_placeorder.objects.create(
                order_id=order,
                subproduct_id=item.subproduct,
                quantity=item.quantity,
                price=item.total_price_usd or item.quantity * 10,
                size=item.size,
                color=item.color
            )
            item.delete()

        # Save payment record
        Payment.objects.create(
            user=user,
            amount=payment_data['total_usd'],
            method='paypal',
            payment_id=data.get('orderID'),
            status='COMPLETED'
        )

        request.session.pop('pending_order', None)

        return JsonResponse({
            'success': True,
            'order_id': order.order_id
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def payment_success_stripe(request):
    """Handle Stripe payment success"""
    if request.method != 'POST':
        return JsonResponse({'success': False})

    try:
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')

        user = User.objects.get(pk=request.session['user'])
        cart_items = Cart.objects.filter(uname=user)

        total_usd = sum((item.total_price_usd or item.quantity * 10) for item in cart_items) + 1

        # Create order
        order = placeOrder.objects.create(
            user_id=user,
            address_id=AddressModel.objects.filter(user_id=user).first(),
            order_date=timezone.now().date(),
            payment_mode='STRIPE',
            total_amount=total_usd,
            shipping_charge=1,
            total_quantity=sum(i.quantity for i in cart_items),
            order_status='Paid'
        )

        # Save order items
        for item in cart_items:
            sub_placeorder.objects.create(
                order_id=order,
                subproduct_id=item.subproduct,
                quantity=item.quantity,
                price=item.total_price_usd or item.quantity * 10,
                size=item.size,
                color=item.color
            )
            item.delete()

        # Save payment
        Payment.objects.create(
            user=user,
            amount=total_usd,
            method='stripe',
            payment_id=payment_intent_id,
            status='COMPLETED'
        )

        return JsonResponse({
            'success': True,
            'order_id': order.order_id
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def payment_success_cod(request):
    """Handle Cash on Delivery"""
    if 'user' not in request.session:
        return redirect('login')

    try:
        user = User.objects.get(pk=request.session['user'])
        cart_items = Cart.objects.filter(uname=user)

        total_usd = sum((item.total_price_usd or item.quantity * 10) for item in cart_items) + 1

        # Create order
        order = placeOrder.objects.create(
            user_id=user,
            address_id=AddressModel.objects.filter(user_id=user).first(),
            order_date=timezone.now().date(),
            payment_mode='COD',
            total_amount=total_usd,
            shipping_charge=1,
            total_quantity=sum(i.quantity for i in cart_items),
            order_status='Pending'
        )

        # Save order items
        for item in cart_items:
            sub_placeorder.objects.create(
                order_id=order,
                subproduct_id=item.subproduct,
                quantity=item.quantity,
                price=item.total_price_usd or item.quantity * 10,
                size=item.size,
                color=item.color
            )
            item.delete()

        # Save payment
        Payment.objects.create(
            user=user,
            amount=total_usd,
            method='cod',
            status='PENDING'
        )

        messages.success(request, f"Order {order.order_id} placed successfully!")
        return redirect('order_history')

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('checkout')
