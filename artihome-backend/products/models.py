from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self): return self.name
    class Meta: verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    ah_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    waitlist_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def savings_pct(self):
        if self.ah_price and self.market_price and self.market_price > 0:
            return round((1 - float(self.ah_price)/float(self.market_price)) * 100)
        return 0
