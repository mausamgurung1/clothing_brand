from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home-02/', views.home02, name='home02'),
    path('home-03/', views.home03, name='home03'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product_list, name='product'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
