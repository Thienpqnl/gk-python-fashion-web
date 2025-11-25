from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    """Shopping cart per user (skeleton)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    """Individual item in cart (skeleton)."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()  # Foreign key to products.Product
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.cart.id} - Product {self.product_id} (qty={self.quantity})"
