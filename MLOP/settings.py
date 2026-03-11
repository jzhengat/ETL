"""
Django settings for MLOP project (production-ready for Azure).
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-for-dev')
DEBUG = False  # Must be False in production

ALLOWED_HOSTS = [
    'joycedevresource-ddg5hrgbafaccaf6.centralus-01.azurewebsites.net',
    '.azurewebsites.net',
    'localhost',
    '127.0.0.1',
]

# Health check middleware to rewrite Azure internal IPs
class HealthCheckHostMiddleware:
    """
    Rewrite Azure health check hosts (169.254.*) to the canonical host.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host.startswith("169.254."):
            request.META["HTTP_HOST"] = "joycedevresource-ddg5hrgbafaccaf6.centralus-01.azurewebsites.net"
        return self.get_response(request)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'store',
    'corsheaders',
]

MIDDLEWARE = [
    'MLOP.settings.HealthCheckHostMiddleware',  # Top of the stack
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MLOP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MLOP.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://joycedevresource-ddg5hrgbafaccaf6.centralus-01.azurewebsites.net',
]
CORS_ALLOW_CREDENTIALS = True

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.azurewebsites.net',
    'https://joycedevresource-ddg5hrgbafaccaf6.centralus-01.azurewebsites.net',
]

# Logging to ignore DisallowedHost spam from Azure health checks
import logging

class IgnoreAzureDisallowedHost(logging.Filter):
    def filter(self, record):
        # Ignore messages from Azure internal IPs
        if '169.254.' in str(record.msg):
            return False
        return True

logging.getLogger('django.security.DisallowedHost').addFilter(IgnoreAzureDisallowedHost())

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'level': 'INFO'},
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}