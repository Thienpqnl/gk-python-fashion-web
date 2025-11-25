from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """Order placed by user (skeleton)."""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_price = models.IntegerField(default=0)
    shipping_address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    """Individual item in order (skeleton)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()
    product_title = models.CharField(max_length=200, blank=True)
    product_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Order {self.order.id} - Product {self.product_id}"
