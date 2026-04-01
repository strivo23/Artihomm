import os

files = {}

files['artihome-backend/accounts/serializers.py'] = """from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'city', 'phone')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'city', 'phone')
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active: return user
        raise serializers.ValidationError("Incorrect Credentials")
"""

files['artihome-backend/accounts/views.py'] = """from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'user': UserSerializer(user).data, 'token': get_tokens_for_user(user)}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        return Response({'user': UserSerializer(user).data, 'token': get_tokens_for_user(user)})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = RefreshToken(request.data["refresh"])
        token.blacklist()
        return Response(status=205)
    except Exception as e:
        return Response(status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(UserSerializer(request.user).data)
"""

files['artihome-backend/products/__init__.py'] = ""
files['artihome-backend/products/urls.py'] = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list')
]
"""
files['artihome-backend/products/models.py'] = """from django.db import models

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
    image_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    waitlist_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): return self.name
"""

files['artihome-backend/products/admin.py'] = """from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'estimated_price', 'waitlist_count', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
"""

files['artihome-backend/products/serializers.py'] = """from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'category_name', 'description', 
                  'estimated_price', 'image_url', 'waitlist_count', 'is_active')
"""

files['artihome-backend/products/views.py'] = """from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-waitlist_count')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
"""

files['artihome-backend/products/management/__init__.py'] = ""
files['artihome-backend/products/management/commands/__init__.py'] = ""
files['artihome-backend/products/management/commands/seed_products.py'] = """from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with initial products'
    def handle(self, *args, **kwargs):
        c_lounge, _ = Category.objects.get_or_create(name='Lounge', slug='lounge')
        c_work, _ = Category.objects.get_or_create(name='Workspace', slug='workspace')
        c_bedroom, _ = Category.objects.get_or_create(name='Bedroom', slug='bedroom')
        
        products = [
            {'category': c_lounge, 'name': 'The Cloud Sofa', 'slug': 'cloud-sofa', 'price': '1299.00', 'desc': 'Ultimate comfort with deep seating.', 'img': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&q=80', 'count': 42},
            {'category': c_work, 'name': 'Ergo Pro Desk', 'slug': 'ergo-pro-desk', 'price': '799.00', 'desc': 'Smart standing desk with memory settings.', 'img': 'https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&q=80', 'count': 18},
            {'category': c_bedroom, 'name': 'Zenith Bed Frame', 'slug': 'zenith-bed', 'price': '950.00', 'desc': 'Minimalist oak bed frame with built-in storage.', 'img': 'https://images.unsplash.com/photo-1505693314120-0d443867891c?auto=format&fit=crop&q=80', 'count': 35},
            {'category': c_lounge, 'name': 'Velvet Accent Chair', 'slug': 'velvet-accent', 'price': '350.00', 'desc': 'Bold colors and a sculptural frame.', 'img': 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&q=80', 'count': 12},
        ]
        
        for p in products:
            obj, created = Product.objects.get_or_create(
                slug=p['slug'],
                defaults={'category': p['category'], 'name': p['name'], 'estimated_price': p['price'], 
                          'description': p['desc'], 'image_url': p['img'], 'waitlist_count': p['count']}
            )
            if created: self.stdout.write(f"Created {p['name']}")
"""

files['artihome-backend/waitlist/__init__.py'] = ""
files['artihome-backend/waitlist/urls.py'] = """from django.urls import path
from . import views

urlpatterns = [
    path('join/<int:product_id>/', views.join_waitlist, name='join_waitlist'),
    path('leave/<int:product_id>/', views.leave_waitlist, name='leave_waitlist'),
    path('my/', views.user_waitlists, name='user_waitlists'),
]
"""
files['artihome-backend/waitlist/models.py'] = """from django.db import models
from django.conf import settings
from products.models import Product

class WaitlistEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waitlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='waitlist_entries')
    pledged_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name_plural = 'Waitlist Entries'

    def __str__(self): return f"{self.user.email} - {self.product.name}"
"""

files['artihome-backend/waitlist/admin.py'] = """from django.contrib import admin
from .models import WaitlistEntry

@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'pledged_price', 'joined_at')
    list_filter = ('product', 'joined_at')
    search_fields = ('user__email', 'product__name')
"""

files['artihome-backend/waitlist/serializers.py'] = """from rest_framework import serializers
from .models import WaitlistEntry
from products.serializers import ProductSerializer

class WaitlistEntrySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = WaitlistEntry
        fields = ('id', 'product', 'pledged_price', 'joined_at')
"""

files['artihome-backend/waitlist/views.py'] = """from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import WaitlistEntry
from products.models import Product
from .serializers import WaitlistEntrySerializer
from django.db.models import F

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_waitlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    pledged = request.data.get('pledged_price')
    
    entry, created = WaitlistEntry.objects.get_or_create(
        user=request.user, product=product,
        defaults={'pledged_price': pledged}
    )
    
    if created:
        product.waitlist_count = F('waitlist_count') + 1
        product.save(update_fields=['waitlist_count'])
        return Response({'status': 'joined', 'waitlist_count': product.waitlist_count + 1}, status=201)
    
    if pledged and entry.pledged_price != pledged:
        entry.pledged_price = pledged
        entry.save()
    return Response({'status': 'already_joined'}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_waitlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    deleted, _ = WaitlistEntry.objects.filter(user=request.user, product=product).delete()
    if deleted:
        product.waitlist_count = F('waitlist_count') - 1
        product.save(update_fields=['waitlist_count'])
    return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_waitlists(request):
    entries = WaitlistEntry.objects.filter(user=request.user).select_related('product')
    serializer = WaitlistEntrySerializer(entries, many=True)
    return Response(serializer.data)
"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
