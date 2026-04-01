from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY    = os.getenv('SECRET_KEY', 'unsafe-dev-secret-do-not-use-in-production')
DEBUG         = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     BASE_DIR / 'db.sqlite3',
    }
}

# Allow all origins in dev so React on localhost:5173 works without CORS errors
CORS_ALLOW_ALL_ORIGINS = True