from django.db import models

# reviews/models.py
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # Liên kết đơn hàng
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=20, default='Neutral', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"