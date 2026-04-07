from rest_framework import serializers
from .models import WaitlistEntry
from products.serializers import ProductSerializer

class WaitlistEntrySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = WaitlistEntry
        fields = ('id', 'product', 'name', 'phone', 'city', 'requirements', 'is_pledge', 'created_at')
