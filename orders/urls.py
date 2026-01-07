from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='api-order-create'),
    path('payment/', views.payment_return, name='payment_return'),
]