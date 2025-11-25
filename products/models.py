from django.db import models


class Category(models.Model):
    """Product category skeleton."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Extended Product model (replaces shop.Product later)."""
    sku = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    image = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
