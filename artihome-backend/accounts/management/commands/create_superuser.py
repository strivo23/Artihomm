from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
        else:
            User.objects.create_superuser(
                username='admin',
                email=os.getenv('ADMIN_EMAIL', 'admin@artihome.com'),
                password=os.getenv('ADMIN_PASSWORD', 'AdminPassword123!')
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
