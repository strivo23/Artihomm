import os

dirs = [
    'artihome-backend',
    'artihome-backend/artihome_project',
    'artihome-backend/artihome_project/settings',
    'artihome-backend/accounts',
    'artihome-backend/products',
    'artihome-backend/products/management',
    'artihome-backend/products/management/commands',
    'artihome-backend/waitlist'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

files = {}

files['artihome-backend/requirements.txt'] = """Django==4.2.9
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
dj-database-url==2.1.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
Pillow==10.2.0
python-dotenv==1.0.1
"""

files['artihome-backend/render.yaml'] = """services:
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
  - type: pserv
    name: artihome-db
    plan: free
    databaseName: artihome
    databaseUser: artihome_user
"""

files['artihome-backend/build.sh'] = """#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_products
"""

files['artihome-backend/.env.example'] = """SECRET_KEY=change-me
DEBUG=True
"""

files['artihome-backend/manage.py'] = """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artihome_project.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""

files['artihome-backend/artihome_project/__init__.py'] = ""
files['artihome-backend/artihome_project/settings/__init__.py'] = ""
files['artihome-backend/artihome_project/urls.py'] = """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/waitlist/', include('waitlist.urls')),
]
"""
files['artihome-backend/artihome_project/wsgi.py'] = """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artihome_project.settings.prod')
application = get_wsgi_application()
"""

files['artihome-backend/artihome_project/settings/base.py'] = """import os
from pathlib import Path
from datetime import timedelta

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
AUTH_USER_MODEL = 'accounts.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'artihome_project.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""

files['artihome-backend/artihome_project/settings/dev.py'] = """from .base import *

SECRET_KEY = 'dev-secret-key-123!!'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CORS_ALLOW_ALL_ORIGINS = True
"""

files['artihome-backend/artihome_project/settings/prod.py'] = """from .base import *
import dj_database_url
import os

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=True)}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
"""

files['artihome-backend/accounts/__init__.py'] = ""
files['artihome-backend/accounts/urls.py'] = """from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.me_view, name='me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
"""
files['artihome-backend/accounts/models.py'] = """from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self): return self.email
"""

files['artihome-backend/accounts/admin.py'] = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'city', 'phone', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_active', 'city')
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
