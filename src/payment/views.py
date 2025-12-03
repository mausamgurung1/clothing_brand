import json
import requests
import base64
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone

from .models import Payment
from app.models import User, Cart, AddressModel, sub_placeorder, placeOrder

# Configure logging
logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def get_paypal_access_token():
    """Get PayPal OAuth access token"""
    url = f"{settings.PAYPAL_API_BASE}/v1/oauth2/token"

    # Encode credentials
    credentials = f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    try:
        logger.info("Requesting PayPal access token...")
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        token = response.json().get("access_token")
        logger.info("PayPal access token obtained successfully")
        return token
    except requests.exceptions.RequestException as e:
        logger.error(f"PayPal token error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting PayPal token: {str(e)}")
        return None


def verify_paypal_order(order_id):
    """Verify PayPal order on server side"""
    access_token = get_paypal_access_token()

    if not access_token:
        logger.error("Could not get PayPal access token")
        return None

    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders/{order_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        logger.info(f"Verifying PayPal order: {order_id}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        order_data = response.json()
        logger.info(f"PayPal order verified. Status: {order_data.get('status')}")
        return order_data
    except requests.exceptions.RequestException as e:
        logger.error(f"PayPal verification error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error verifying PayPal order: {str(e)}")
        return None


def create_stripe_payment_intent(request):
    """Create Stripe Payment Intent"""
    if request.method != 'POST' or 'user' not in request.session:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        user = User.objects.get(pk=request.session['user'])
        cart = Cart.objects.filter(uname=user)

        if not cart.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)

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
        logger.error(f"Stripe payment intent error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


def create_paypal_order(request):
    """Store PayPal order details in session"""
    if request.method != 'POST' or 'user' not in request.session:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

    try:
        data = json.loads(request.body)
        user = User.objects.get(pk=request.session['user'])
        cart = Cart.objects.filter(uname=user)

        if not cart.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'})

        total_usd = sum((item.total_price_usd or item.quantity * 10) for item in cart) + 1

        request.session['pending_order'] = {
            'user_id': user.id,
            'total_usd': round(total_usd, 2),
            'method': 'paypal',
            'payment_id': data.get('orderID', '')
        }
        request.session.modified = True

        logger.info(f"PayPal order created in session for user {user.id}")
        return JsonResponse({'success': True})

    except Exception as e:
        logger.error(f"Create PayPal order error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})


def capture_paypal_order(request):
    """Capture and verify PayPal payment, then create order"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    try:
        data = json.loads(request.body)
        order_id = data.get('orderID')

        logger.info(f"Starting PayPal capture for order: {order_id}")

        if not order_id:
            logger.error("No order ID provided")
            return JsonResponse({'success': False, 'error': 'No order ID provided'})

        # Check if user is logged in
        if 'user' not in request.session:
            logger.error("User not in session")
            return JsonResponse({'success': False, 'error': 'User not logged in'})

        # Verify PayPal order on server side
        paypal_order = verify_paypal_order(order_id)

        if not paypal_order:
            logger.error("Failed to verify PayPal order")
            return JsonResponse({
                'success': False,
                'error': 'Failed to verify payment with PayPal. Please contact support.'
            })

        # Check payment status
        order_status = paypal_order.get('status')
        logger.info(f"PayPal order status: {order_status}")

        if order_status not in ['APPROVED', 'COMPLETED']:
            logger.error(f"Invalid PayPal order status: {order_status}")
            return JsonResponse({
                'success': False,
                'error': f'Payment not completed. Status: {order_status}'
            })

        # Get session data
        payment_data = request.session.get('pending_order')
        if not payment_data:
            logger.error("No pending order in session")
            return JsonResponse({'success': False, 'error': 'Session expired. Please try again.'})

        # Get user and cart
        user = User.objects.get(pk=payment_data['user_id'])
        cart_items = Cart.objects.filter(uname=user)

        if not cart_items.exists():
            logger.error("Cart is empty")
            return JsonResponse({'success': False, 'error': 'Cart is empty'})

        # Get user address
        user_address = AddressModel.objects.filter(user_id=user).first()
        if not user_address:
            logger.error("No address found for user")
            return JsonResponse({'success': False, 'error': 'Please add a delivery address first'})

        # Verify payment amount matches
        paypal_amount = float(paypal_order.get('purchase_units', [{}])[0].get('amount', {}).get('value', 0))
        expected_amount = float(payment_data['total_usd'])

        logger.info(f"Amount verification - PayPal: {paypal_amount}, Expected: {expected_amount}")

        if abs(paypal_amount - expected_amount) > 0.01:  # Allow 1 cent difference for rounding
            logger.error(f"Amount mismatch - PayPal: {paypal_amount}, Expected: {expected_amount}")
            return JsonResponse({
                'success': False,
                'error': 'Payment amount mismatch. Please contact support.'
            })

        # Create order
        logger.info("Creating order in database...")
        order = placeOrder.objects.create(
            user_id=user,
            address_id=user_address,
            order_date=timezone.now().date(),
            payment_mode='PAYPAL',
            total_amount=payment_data['total_usd'],
            shipping_charge=1,
            total_quantity=sum(i.quantity for i in cart_items),
            order_status='Paid'
        )
        logger.info(f"Order created: {order.order_id}")

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

        # Clear cart
        cart_items.delete()
        logger.info("Cart cleared")

        # Save payment record
        Payment.objects.create(
            user=user,
            amount=payment_data['total_usd'],
            method='paypal',
            payment_id=order_id,
            status='COMPLETED',
            completed_at=timezone.now()
        )
        logger.info("Payment record saved")

        # Clear session
        request.session.pop('pending_order', None)
        request.session.modified = True

        logger.info(f"PayPal payment completed successfully for order {order.order_id}")
        return JsonResponse({
            'success': True,
            'order_id': order.order_id
        })

    except User.DoesNotExist:
        logger.error("User not found")
        return JsonResponse({'success': False, 'error': 'User not found'})
    except Exception as e:
        logger.error(f"Capture error: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})


def payment_success_stripe(request):
    """Handle Stripe payment success"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    try:
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')

        if not payment_intent_id:
            return JsonResponse({'success': False, 'error': 'No payment intent ID'})

        user = User.objects.get(pk=request.session['user'])
        cart_items = Cart.objects.filter(uname=user)

        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'})

        total_usd = sum((item.total_price_usd or item.quantity * 10) for item in cart_items) + 1

        # Get user address
        user_address = AddressModel.objects.filter(user_id=user).first()
        if not user_address:
            return JsonResponse({'success': False, 'error': 'Please add a delivery address first'})

        # Create order
        order = placeOrder.objects.create(
            user_id=user,
            address_id=user_address,
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

        # Clear cart
        cart_items.delete()

        # Save payment
        Payment.objects.create(
            user=user,
            amount=total_usd,
            method='stripe',
            payment_id=payment_intent_id,
            status='COMPLETED',
            completed_at=timezone.now()
        )

        return JsonResponse({
            'success': True,
            'order_id': order.order_id
        })

    except Exception as e:
        logger.error(f"Stripe success error: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)})


def payment_success_cod(request):
    """Handle Cash on Delivery"""
    if 'user' not in request.session:
        return redirect('login')

    try:
        user = User.objects.get(pk=request.session['user'])
        cart_items = Cart.objects.filter(uname=user)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty")
            return redirect('cart')

        total_usd = sum((item.total_price_usd or item.quantity * 10) for item in cart_items) + 1

        # Get user address
        user_address = AddressModel.objects.filter(user_id=user).first()
        if not user_address:
            messages.error(request, "Please add a delivery address")
            return redirect('checkout')

        # Create order
        order = placeOrder.objects.create(
            user_id=user,
            address_id=user_address,
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

        # Clear cart
        cart_items.delete()

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
        logger.error(f"COD error: {str(e)}", exc_info=True)
        messages.error(request, f"Error: {str(e)}")
        return redirect('checkout')