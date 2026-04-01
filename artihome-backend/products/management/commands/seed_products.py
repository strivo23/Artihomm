from django.core.management.base import BaseCommand
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
