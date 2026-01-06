# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.list_user_orders, name='orders-list'),
#     path('<int:order_id>/', views.get_order_detail, name='order-detail'),
#     path('create/', views.create_order_from_cart, name='order-create'),
#     path('<int:order_id>/update-status/', views.update_order_status, name='order-update-status'),
#     path('<int:order_id>/cancel/', views.cancel_order, name='order-cancel'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='api-order-create'),

]