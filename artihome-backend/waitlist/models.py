from django.db import models
from django.conf import settings
from products.models import Product

class WaitlistEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waitlist_entries')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='waitlist_entries')
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    is_pledge = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name_plural = 'Waitlist Entries'

    def __str__(self): return f"{self.user.email} - {self.product.name}"
