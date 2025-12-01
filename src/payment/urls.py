
from django.contrib import admin
from django.urls import path
# from .views import *
from app.views import *
from src.payment import views
from admin_app.views import *
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('create-stripe-payment-intent/', views.create_stripe_payment_intent, name='create_stripe_payment_intent'),
    path('create-paypal-order/', views.create_paypal_order, name='create_paypal_order'),
    path('capture-paypal-order/', views.capture_paypal_order, name='capture_paypal_order'),
    path('payment-success-stripe/', views.payment_success_stripe, name='payment_success_stripe'),
    path('payment-success-cod/', views.payment_success_cod, name='payment_success_cod'),
]

