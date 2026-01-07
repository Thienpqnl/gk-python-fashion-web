from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shop-index'),
    path('products/', views.products_page, name='shop-products'),
    path('product/<int:product_id>/', views.product_detail_page, name='shop-product-detail'),
    path('cart/', views.cart_page, name='shop-cart'),
    path('checkout/', views.checkout_page, name='shop-checkout'),
    path('ai-search/', views.ai_search_page, name='shop-ai-search'),
    path('order-history/', views.order_history_page, name='shop-order-history'),  
    path('order-success/<int:order_id>/', views.order_success, name='shop_order_success'),
]
