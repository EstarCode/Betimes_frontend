"""
Health Check Endpoints
For monitoring and load balancer health checks
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Basic health check endpoint
    Returns 200 if service is running
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'betimes-enterprise',
        'version': '1.0.0'
    })


def readiness_check(request):
    """
    Readiness check - verifies all dependencies are available
    Used by Kubernetes/load balancers to determine if service can accept traffic
    """
    checks = {
        'database': check_database(),
        'cache': check_cache(),
        'celery': check_celery(),
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return JsonResponse({
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks
    }, status=status_code)


def liveness_check(request):
    """
    Liveness check - verifies service is alive
    Used by Kubernetes to restart unhealthy pods
    """
    return JsonResponse({
        'status': 'alive',
        'service': 'betimes-enterprise'
    })


def check_database():
    """Check database connectivity"""
    try:
        connection.ensure_connection()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False


def check_cache():
    """Check Redis cache connectivity"""
    try:
        cache.set('health_check', 'ok', 10)
        value = cache.get('health_check')
        return value == 'ok'
    except Exception as e:
        logger.error(f"Cache health check failed: {str(e)}")
        return False


def check_celery():
    """Check Celery worker connectivity"""
    try:
        from config.celery import app
        inspector = app.control.inspect()
        stats = inspector.stats()
        return stats is not None and len(stats) > 0
    except Exception as e:
        logger.error(f"Celery health check failed: {str(e)}")
        return False
