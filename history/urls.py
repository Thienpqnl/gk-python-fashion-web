from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.order_history_view, name='order-history-page'),
    # Đường dẫn API (JS sẽ gọi vào đây)
    path('list/', views.list_user_orders, name='api-history-list'),
    path('detail/<int:order_id>/', views.get_order_detail, name='api-history-detail'),
    path('cancel/<int:order_id>/', views.cancel_order, name='api-history-cancel'),
]