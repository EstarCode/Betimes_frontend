"""
Django settings for Betimes Document Processing System.
Production-ready for Render deployment | Python 3.12 | Django 5.1
"""

import os
import sys
from pathlib import Path
from datetime import timedelta
import environ

# ─── Base ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    TESTING=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")  # ignored safely if missing in production

SECRET_KEY = env("SECRET_KEY", default="django-insecure-change-this-in-production")
DEBUG = env("DEBUG")
TESTING = env.bool("TESTING", default=False)

# ─── Hosts ───────────────────────────────────────────────────────────────────

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    # FIX 1: Added .onrender.com so Render deployment doesn't return 400 Bad Request
    default=["localhost", "127.0.0.1", ".onrender.com"],
)

# ─── Applications ────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    # FIX 2: BLACKLIST_AFTER_ROTATION=True requires this app in INSTALLED_APPS
    # If you don't want token blacklisting, set BLACKLIST_AFTER_ROTATION=False
    # and remove this line. Keeping it here to match JWT settings below.
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_yasg",
    "django_extensions",

    # Local apps — Core
    "apps.authentication",

    # Local apps — Document Processing
    "apps.compression",
    "apps.conversion",
    "apps.pdf_tools",
    "apps.analytics",

    # Local apps — Supporting Features
    # NOTE: Only include apps whose migrations/models actually exist.
    # Comment out any app that isn't implemented yet to prevent startup crashes.
    "apps.uploads",
    "apps.dashboard",
    # "apps.versions",    # uncomment when implemented
    # "apps.workflows",   # uncomment when implemented
    # "apps.audit",       # uncomment when implemented
    # "apps.notifications", # uncomment when implemented
    # "apps.search_engine", # uncomment when implemented
]

# ─── Middleware ───────────────────────────────────────────────────────────────

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",       # must be 2nd
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",            # before CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # FIX 3: Custom middleware removed from here.
    # These caused ImportError crashes if config/middleware.py didn't exist.
    # Add them back only after confirming config/middleware.py is implemented:
    #   "config.middleware.SecurityHeadersMiddleware",
    #   "config.middleware.RateLimitMiddleware",
    #   "config.middleware.RequestLoggingMiddleware",
    #   "config.middleware.InputSanitizationMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ─── Database ────────────────────────────────────────────────────────────────

import dj_database_url  # already in requirements.txt

DATABASE_URL = env("DATABASE_URL", default="").strip().strip('"').strip("'")

if DATABASE_URL:
    try:
        DATABASES = {
            "default": dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
        DATABASES["default"]["OPTIONS"] = {
            "connect_timeout": 10,
            "options": "-c statement_timeout=30000",
        }
        # FIX 4: ssl_require only in production (causes errors in local dev with SQLite fallback)
        if not DEBUG:
            DATABASES["default"].setdefault("OPTIONS", {})
            DATABASES["default"]["OPTIONS"]["sslmode"] = "require"
    except ValueError as exc:
        raise ValueError(
            "Invalid DATABASE_URL. Expected: postgresql://user:password@host:5432/dbname"
        ) from exc
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─── Password Validation ─────────────────────────────────────────────────────

# FIX 5: Replaced all custom validators with Django's built-in ones.
# The original custom validators (MinimumLengthValidator, UppercaseValidator, etc.)
# caused crashes if apps/authentication/validators.py wasn't fully implemented.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ─── Internationalisation ────────────────────────────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ─── Static & Media Files ────────────────────────────────────────────────────

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "authentication.User"

# ─── REST Framework ──────────────────────────────────────────────────────────

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    # FIX 6: Removed reference to config.error_handlers.custom_exception_handler
    # which caused ImportError if that file didn't exist.
    # Add back once config/error_handlers.py is confirmed to exist.
    # "EXCEPTION_HANDLER": "config.error_handlers.custom_exception_handler",
}

# ─── JWT ─────────────────────────────────────────────────────────────────────

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int("JWT_ACCESS_TOKEN_LIFETIME", default=60)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=env.int("JWT_REFRESH_TOKEN_LIFETIME", default=10080)  # 7 days
    ),
    "ROTATE_REFRESH_TOKENS": True,
    # FIX 7: BLACKLIST_AFTER_ROTATION=True requires running:
    #   python manage.py migrate  (creates token_blacklist tables)
    # Set to False if you want to skip blacklisting entirely.
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# ─── CORS ────────────────────────────────────────────────────────────────────

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
)
# FIX 8: Removed hardcoded Render/Vercel URLs from default.
# Set CORS_ALLOWED_ORIGINS env var in Render dashboard to your actual frontend URL.
# Example: CORS_ALLOWED_ORIGINS=https://betimes-frontend.onrender.com

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-request-id",
]

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["https://*.onrender.com"],
)

# ─── Celery ──────────────────────────────────────────────────────────────────

# FIX 9: Was hardcoded to redis://localhost:6379/0, ignoring REDIS_URL env var.
# Now reads from REDIS_URL (same var used by Render Redis add-on).
_REDIS_URL = env("REDIS_URL", default="")

CELERY_BROKER_URL = _REDIS_URL or env("CELERY_BROKER_URL", default="memory://")
CELERY_RESULT_BACKEND = _REDIS_URL or env("CELERY_RESULT_BACKEND", default="cache+memory://")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60      # 30 minutes hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60 # 25 minutes soft warning

# ─── Cache ───────────────────────────────────────────────────────────────────

# FIX 10: Was using django_redis which is NOT in requirements.txt → ModuleNotFoundError.
# Replaced with Django's built-in RedisCache (available since Django 4.0, no extra package).
if TESTING or not _REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "app-cache",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _REDIS_URL,
            "OPTIONS": {
                "socket_connect_timeout": 5,
                "socket_timeout": 5,
                "retry_on_timeout": True,
            },
            "KEY_PREFIX": "betimes",
            "TIMEOUT": 300,
        }
    }

# ─── Sessions ────────────────────────────────────────────────────────────────

# FIX 11: SESSION_ENGINE=cache + LocMemCache + multiple Gunicorn workers = broken sessions.
# Each worker has its own memory → sessions created by worker 1 are invisible to worker 2.
# Solution: use DB-backed sessions which are shared across all workers.
# Switch back to "cache" only if you have a proper Redis instance configured.
if _REDIS_URL:
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_AGE = 86400      # 24 hours
SESSION_SAVE_EVERY_REQUEST = False

# ─── File Uploads ────────────────────────────────────────────────────────────

# FIX 12: Was 10GB (10737418240). Render free tier has 512MB RAM.
# A 10GB limit means a single upload can OOM-kill the entire process.
# Set to 50MB which is reasonable for PDF tools.
MAX_UPLOAD_SIZE = env.int("MAX_UPLOAD_SIZE", default=52428800)  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024                  # 10 MB in memory
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024                  # 10 MB

ALLOWED_EXTENSIONS = env.list(
    "ALLOWED_EXTENSIONS",
    default=["pdf", "doc", "docx", "jpg", "jpeg", "png", "xlsx", "pptx"],
)

# ─── PDF / Ghostscript ───────────────────────────────────────────────────────

GHOSTSCRIPT_PATH = env("GHOSTSCRIPT_PATH", default="/usr/bin/gs")

COMPRESSION_PROFILES = {
    "low": {"setting": "/prepress", "description": "High quality, small reduction", "dpi": 300},
    "medium": {"setting": "/ebook", "description": "Balanced quality and size", "dpi": 150},
    "high": {"setting": "/screen", "description": "Maximum reduction", "dpi": 72},
}

# ─── Email ───────────────────────────────────────────────────────────────────

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# ─── Security ────────────────────────────────────────────────────────────────

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

IS_TEST_ENV = TESTING or any(arg in {"test", "pytest"} for arg in sys.argv)

if not DEBUG and not IS_TEST_ENV:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
    # FIX 13: SECURE_SSL_REDIRECT=True on Render causes an infinite redirect loop.
    # Render terminates SSL at its load balancer and forwards plain HTTP to Django.
    # Django then sees HTTP → redirects to HTTPS → Render forwards HTTP again → loop.
    # Solution: always False on Render. Render handles HTTPS for you.
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # FIX 14: HSTS commented out intentionally.
    # Only enable HSTS after you've confirmed HTTPS works perfectly.
    # Once set, browsers will refuse HTTP for HSTS_SECONDS (1 year here).
    # A misconfiguration will lock users out of your site for a year.
    # SECURE_HSTS_SECONDS = 31536000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

# ─── Logging ─────────────────────────────────────────────────────────────────

# FIX 15: Removed file handler entirely.
# Render uses an ephemeral filesystem — the logs/ directory is wiped on every deploy.
# Writing to a log file silently fails or raises PermissionError.
# All logs should go to stdout/stderr (Render captures these in the dashboard).

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# FIX 16: Moved os.makedirs out of settings (it ran on every import including
# Celery workers, gunicorn prefork, and test runners — and fails on Render's
# read-only filesystem). Log dir creation belongs in manage.py or a startup script.
# If you need local log files in dev, add this to your manage.py instead:
#   os.makedirs("logs", exist_ok=True)
