from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_cart, name='cart-get'),
    path('add/', views.add_to_cart, name='cart-add'),
    path('remove/', views.remove_from_cart, name='cart-remove'),
    path('update/', views.update_cart_item, name='cart-update'),
    path('clear/', views.clear_cart, name='cart-clear'),
]
