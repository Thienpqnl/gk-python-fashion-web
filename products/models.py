from django.db import models


class Category(models.Model):
    """Product category skeleton."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Extended Product model (replaces shop.Product later)."""
    SEASON_SPRING = 'spring'
    SEASON_SUMMER = 'summer'
    SEASON_AUTUMN = 'autumn'
    SEASON_WINTER = 'winter'
    SEASON_ALL = 'all'
    SEASON_CHOICES = [
        (SEASON_SPRING, 'Spring'),
        (SEASON_SUMMER, 'Summer'),
        (SEASON_AUTUMN, 'Autumn'),
        (SEASON_WINTER, 'Winter'),
        (SEASON_ALL, 'All-season'),
    ]

    sku = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    image = models.CharField(max_length=500, blank=True)
    seasonal_discount_percent = models.PositiveIntegerField(default=0, help_text='Seasonal discount percent (0 = no discount)')
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, default=SEASON_ALL, blank=True, help_text='Season used for seasonal discounts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_on_seasonal_sale(self):
        """Return True if the product has a seasonal discount for the current season."""
        from django.conf import settings
        current = getattr(settings, 'CURRENT_SEASON', self.SEASON_ALL)
        applies = (self.season == current) or (self.season == self.SEASON_ALL)
        return self.seasonal_discount_percent > 0 and applies

    @property
    def discounted_price(self):
        """Return price after applying seasonal discount (integer)."""
        if not self.is_on_seasonal_sale:
            return self.price
        discount = (self.price * self.seasonal_discount_percent) // 100
        return self.price - discount

    def __str__(self):
        return self.title
