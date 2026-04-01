import os

files = {
    'artihome-frontend/vercel.json': '''{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}''',
    'artihome-frontend/.gitignore': '''# Dependencies
node_modules/

# Build output
dist/
dist-ssr/
build/

# Environment variables
.env
.env.*
!.env.example

# Vite
*.local

# IDE
.vscode/
.idea/
.DS_Store

# Logs
npm-debug.log*
yarn-debug.log*''',
    'artihome-backend/.gitignore': '''# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so
*.egg
*.egg-info/
dist/
build/

# Virtual environment
venv/
env/
.venv/

# Django
*.log
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment variables — NEVER commit these
.env
.env.*
!.env.example

# Google credentials
credentials.json

# IDE
.vscode/
.idea/
.DS_Store''',
    'artihome-backend/artihome_project/settings/__init__.py': '',
    'artihome-backend/artihome_project/settings/base.py': '''from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'accounts',
    'products',
    'waitlist',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'artihome_project.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': { 'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'artihome_project.wsgi.application'
AUTH_USER_MODEL   = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'
USE_I18N      = True
USE_TZ        = True

STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':    timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME':   timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':    True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES':        ('Bearer',),
}

CORS_ALLOW_CREDENTIALS = True''',
    'artihome-backend/artihome_project/settings/dev.py': '''from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY    = os.getenv('SECRET_KEY', 'unsafe-dev-secret-do-not-use-in-production')
DEBUG         = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     BASE_DIR / 'db.sqlite3',
    }
}

# Allow all origins in dev so React on localhost:5173 works without CORS errors
CORS_ALLOW_ALL_ORIGINS = True''',
    'artihome-backend/artihome_project/settings/prod.py': '''from .base import *
import os
import dj_database_url

SECRET_KEY    = os.environ['SECRET_KEY']
DEBUG         = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_ALL_ORIGINS = False

SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_BROWSER_XSS_FILTER       = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
SECURE_HSTS_SECONDS             = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
X_FRAME_OPTIONS                 = "DENY"''',
    'artihome-backend/artihome_project/wsgi.py': '''import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artihome_project.settings.dev')
application = get_wsgi_application()''',
    'artihome-backend/manage.py': '''#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artihome_project.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()''',
    'artihome-backend/requirements.txt': '''Django==4.2.9
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
dj-database-url==2.1.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
Pillow==10.2.0
python-dotenv==1.0.1''',
    'artihome-backend/render.yaml': '''services:
  - type: web
    name: artihome-backend
    env: python
    plan: free
    buildCommand: "./build.sh"
    startCommand: "gunicorn artihome_project.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: artihome_project.settings.prod
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: artihome-backend.onrender.com
      - key: CORS_ALLOWED_ORIGINS
        value: https://artihome.vercel.app
      - key: DATABASE_URL
        fromDatabase:
          name: artihome-db
          property: connectionString

databases:
  - name: artihome-db
    plan: free
    databaseName: artihome
    user: artihome_user''',
    'artihome-backend/build.sh': '''#!/usr/bin/env bash
set -o errexit

echo "--- Installing dependencies ---"
pip install -r requirements.txt

echo "--- Collecting static files ---"
python manage.py collectstatic --no-input

echo "--- Running migrations ---"
python manage.py migrate

echo "--- Seeding products ---"
python manage.py seed_products

echo "--- Build complete ---"
''',
    'artihome-backend/waitlist/admin.py': '''from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import WaitlistEntry

@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display    = ('get_email', 'product', 'name', 'phone', 'city', 'is_pledge', 'created_at')
    list_filter     = ('is_pledge', 'product__category', 'city', 'product')
    search_fields   = ('user__email', 'name', 'phone', 'product__name', 'city')
    readonly_fields = ('created_at', 'user')
    ordering        = ('-created_at',)
    date_hierarchy  = 'created_at'
    actions         = ['export_as_csv']

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="artihome_waitlist.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Name', 'Email', 'Phone', 'City',
            'Product', 'Category', 'Price (Rs.)', 'Requirements', 'Pledge'
        ])
        for entry in queryset.select_related('user', 'product'):
            # Fallback handling for missing attributes during transition
            writer.writerow([
                entry.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(entry, 'created_at') else '',
                getattr(entry, 'name', ''),
                entry.user.email if hasattr(entry, 'user') and entry.user else '',
                getattr(entry, 'phone', ''),
                getattr(entry, 'city', ''),
                entry.product.name if hasattr(entry, 'product') and entry.product else '',
                getattr(entry.product, 'category', ''),
                getattr(entry.product, 'ah_price', getattr(entry.product, 'estimated_price', 0)) if hasattr(entry, 'product') else 0,
                getattr(entry, 'requirements', ''),
                'Yes' if getattr(entry, 'is_pledge', False) else 'No',
            ])
        return response
    export_as_csv.short_description = 'Export selected entries to CSV'
''',
    'artihome-backend/.env.example': '''# Copy this file to .env — never commit .env to git

SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Settings module
# Local: artihome_project.settings.dev
# Prod:  artihome_project.settings.prod
DJANGO_SETTINGS_MODULE=artihome_project.settings.dev

# PostgreSQL
DB_NAME=artihome
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# CORS — your Vercel frontend URL
CORS_ALLOWED_ORIGINS=http://localhost:5173''',
    'artihome-frontend/.env.example': '''# Copy to .env — never commit .env to git

# Local dev:   http://localhost:8000/api
# Production:  https://your-app.onrender.com/api
VITE_API_URL=http://localhost:8000/api'''
}

import os
for path, content in files.items():
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if os.path.exists('artihome-backend/artihome_project/settings.py'):
    os.remove('artihome-backend/artihome_project/settings.py')

print('All files successfully updated.')
