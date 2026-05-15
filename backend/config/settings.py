"""
Django settings for PDF Utility SaaS Platform.
"""

import os
import sys
from pathlib import Path
from datetime import timedelta
import environ

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
TESTING = env.bool('TESTING', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg',
    'django_extensions',
    
    # Local apps - Core
    'apps.authentication',
    
    # Local apps - Enterprise Features
    'apps.uploads',  # Chunked upload system
    'apps.versions',  # Document version control
    'apps.workflows',  # Enterprise workflows
    'apps.audit',  # Audit logging
    'apps.notifications',  # Multi-channel notifications
    'apps.dashboard',  # Real-time metrics
    'apps.search_engine',  # Full-text search
    
    # Local apps - Document Processing
    'apps.compression',  # PDF compression
    'apps.conversion',  # Document conversion + OCR
    'apps.pdf_tools',  # PDF split/merge/manipulation
    'apps.analytics',  # Analytics
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom security middleware
    'config.middleware.SecurityHeadersMiddleware',
    'config.middleware.RateLimitMiddleware',
    'config.middleware.RequestLoggingMiddleware',
    'config.middleware.InputSanitizationMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Use dj-database-url for better PostgreSQL URL parsing
import dj_database_url

DATABASE_URL = env('DATABASE_URL', default='')

if DATABASE_URL and DATABASE_URL.strip():
    # Production: Use DATABASE_URL from environment
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'apps.authentication.validators.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'apps.authentication.validators.UppercaseValidator',
    },
    {
        'NAME': 'apps.authentication.validators.LowercaseValidator',
    },
    {
        'NAME': 'apps.authentication.validators.NumberValidator',
    },
    {
        'NAME': 'apps.authentication.validators.SpecialCharacterValidator',
    },
    {
        'NAME': 'apps.authentication.validators.CommonPasswordValidator',
    },
    {
        'NAME': 'apps.authentication.validators.PasswordHistoryValidator',
    },
    {
        'NAME': 'apps.authentication.validators.MaximumLengthValidator',
        'OPTIONS': {
            'max_length': 128,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'authentication.User'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # Allow anonymous access
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [],  # No rate limiting for free usage
    'DEFAULT_THROTTLE_RATES': {},
    'EXCEPTION_HANDLER': 'config.error_handlers.custom_exception_handler',
}

if TESTING:
    REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
    REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env.int('JWT_ACCESS_TOKEN_LIFETIME', default=60)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=env.int('JWT_REFRESH_TOKEN_LIFETIME', default=1440)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Settings - Production Ready
CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=[
        'http://localhost:5173',
        'http://localhost:3000',
        'https://betimes.onrender.com',
        'https://betimes.vercel.app',
        'https://document-processing-system.vercel.app',
    ]
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-request-id',
]
CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=[
        'https://betimes.onrender.com',
    ]
)

# Celery Configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

# Redis Cache
REDIS_URL = env('REDIS_URL', default='')
USE_REDIS_CACHE = env.bool('USE_REDIS_CACHE', default=bool(REDIS_URL))

if TESTING or not USE_REDIS_CACHE:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'app-cache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

# File Upload Settings (Unlimited for enterprise use)
MAX_UPLOAD_SIZE = env.int('MAX_UPLOAD_SIZE', default=10737418240)  # 10GB default
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB in memory
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB in memory

ALLOWED_EXTENSIONS = env.list(
    'ALLOWED_EXTENSIONS',
    default=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'xlsx', 'pptx']
)

# Ghostscript Configuration
GHOSTSCRIPT_PATH = env('GHOSTSCRIPT_PATH', default='/usr/bin/gs')

COMPRESSION_PROFILES = {
    'low': {
        'setting': '/prepress',
        'description': 'High quality, small reduction',
        'dpi': 300,
    },
    'medium': {
        'setting': '/ebook',
        'description': 'Balanced quality and size',
        'dpi': 150,
    },
    'high': {
        'setting': '/screen',
        'description': 'Maximum reduction for smallest file size',
        'dpi': 72,
    }
}

# Email Configuration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Keep production security settings enabled, but avoid HTTPS redirect loops in test runs.
IS_TEST_ENV = TESTING or any(arg in {'test', 'pytest'} for arg in sys.argv)

if not DEBUG and not IS_TEST_ENV:
    # Respect TLS termination at reverse proxies/load balancers.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',  # Reduce database query logging
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'WARNING',  # Reduce autoreload warnings
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# Suppress specific warnings in production
if not DEBUG:
    import warnings
    warnings.filterwarnings('ignore', message='.*Engine not recognized from url.*')
    warnings.filterwarnings('ignore', message='.*DateTimeField.*received a naive datetime.*')
