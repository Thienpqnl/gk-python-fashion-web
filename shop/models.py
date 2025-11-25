from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)  # store in smallest currency unit (e.g., cents or VND)
    image = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
