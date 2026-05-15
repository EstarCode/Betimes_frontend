#!/usr/bin/env python
"""
Production Readiness Checklist
Run this before deploying to catch common issues
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.db import connection


def check_secret_key():
    """Verify SECRET_KEY is set and not default"""
    if 'insecure' in settings.SECRET_KEY.lower():
        return False, "❌ SECRET_KEY is using default insecure value"
    if len(settings.SECRET_KEY) < 50:
        return False, "❌ SECRET_KEY is too short (minimum 50 characters)"
    return True, "✅ SECRET_KEY is properly configured"


def check_debug_mode():
    """Verify DEBUG is False in production"""
    if settings.DEBUG:
        return False, "❌ DEBUG is True (must be False in production)"
    return True, "✅ DEBUG is False"


def check_allowed_hosts():
    """Verify ALLOWED_HOSTS is configured"""
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
        return False, "❌ ALLOWED_HOSTS is not properly configured"
    return True, f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}"


def check_database():
    """Verify database connection"""
    try:
        connection.ensure_connection()
        return True, "✅ Database connection successful"
    except Exception as e:
        return False, f"❌ Database connection failed: {str(e)}"


def check_migrations():
    """Verify all migrations are applied"""
    try:
        from io import StringIO
        out = StringIO()
        call_command('showmigrations', '--plan', stdout=out)
        output = out.getvalue()
        if '[ ]' in output:
            return False, "❌ Unapplied migrations found"
        return True, "✅ All migrations applied"
    except Exception as e:
        return False, f"❌ Migration check failed: {str(e)}"


def check_static_files():
    """Verify static files are configured"""
    if not settings.STATIC_ROOT:
        return False, "❌ STATIC_ROOT is not configured"
    return True, f"✅ STATIC_ROOT: {settings.STATIC_ROOT}"


def check_cors():
    """Verify CORS is configured"""
    if not hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
        return False, "❌ CORS_ALLOWED_ORIGINS is not configured"
    if not settings.CORS_ALLOWED_ORIGINS:
        return False, "❌ CORS_ALLOWED_ORIGINS is empty"
    return True, f"✅ CORS configured for {len(settings.CORS_ALLOWED_ORIGINS)} origins"


def check_security_middleware():
    """Verify security middleware is enabled"""
    required_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ]
    missing = [m for m in required_middleware if m not in settings.MIDDLEWARE]
    if missing:
        return False, f"❌ Missing security middleware: {missing}"
    return True, "✅ Security middleware enabled"


def run_checks():
    """Run all production checks"""
    print("\n" + "="*60)
    print("🔍 PRODUCTION READINESS CHECKLIST")
    print("="*60 + "\n")
    
    checks = [
        ("Secret Key", check_secret_key),
        ("Debug Mode", check_debug_mode),
        ("Allowed Hosts", check_allowed_hosts),
        ("Database", check_database),
        ("Migrations", check_migrations),
        ("Static Files", check_static_files),
        ("CORS", check_cors),
        ("Security Middleware", check_security_middleware),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            passed, message = check_func()
            results.append((name, passed, message))
            print(f"{message}")
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"❌ {name}: Error - {str(e)}")
    
    print("\n" + "="*60)
    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)
    
    if passed_count == total_count:
        print(f"✅ ALL CHECKS PASSED ({passed_count}/{total_count})")
        print("="*60 + "\n")
        return 0
    else:
        print(f"❌ SOME CHECKS FAILED ({passed_count}/{total_count})")
        print("="*60 + "\n")
        return 1


if __name__ == '__main__':
    sys.exit(run_checks())
