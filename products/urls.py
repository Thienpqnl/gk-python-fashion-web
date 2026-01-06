from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_products, name='products-list'),
    path('<int:product_id>/', views.product_detail_view, name='product-detail'),
    path('search/', views.search_products, name='products-search'),
    path('category/<int:category_id>/', views.filter_by_category, name='products-by-category'),
]
