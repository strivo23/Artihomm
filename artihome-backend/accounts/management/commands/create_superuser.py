from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if not admin_email or not admin_password:
            self.stdout.write(
                self.style.WARNING(
                    'ADMIN_EMAIL/ADMIN_PASSWORD not set; skipping automatic superuser creation'
                )
            )
            return

        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return

        User.objects.create_superuser(email=admin_email, password=admin_password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
