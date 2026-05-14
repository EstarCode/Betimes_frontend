"""
Custom Security Middleware
Implements OWASP Security Best Practices
"""
import logging
import time
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    Implements OWASP recommendations
    """
    
    def process_response(self, request, response):
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove server header
        if 'Server' in response:
            del response['Server']
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware
    Prevents brute force and DDoS attacks
    """
    
    def process_request(self, request):
        if not settings.DEBUG:
            # Get client IP
            ip = self.get_client_ip(request)
            
            # Different limits for different endpoints
            if request.path.startswith('/api/v1/auth/login/'):
                limit = 5  # 5 login attempts per minute
                window = 60
            elif request.path.startswith('/api/v1/auth/'):
                limit = 20  # 20 auth requests per minute
                window = 60
            else:
                limit = 100  # 100 general requests per minute
                window = 60
            
            cache_key = f"rate_limit:{ip}:{request.path}"
            requests = cache.get(cache_key, 0)
            
            if requests >= limit:
                logger.warning(f"Rate limit exceeded for IP {ip} on {request.path}")
                return JsonResponse({
                    'type': 'about:blank',
                    'title': 'Too Many Requests',
                    'status': 429,
                    'detail': f'Rate limit exceeded. Please try again in {window} seconds.',
                    'instance': request.path,
                }, status=429)
            
            cache.set(cache_key, requests + 1, window)
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Log all API requests for audit and monitoring
    """
    
    def process_request(self, request):
        request.start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log slow requests (> 2 seconds)
            if duration > 2.0:
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.2f}s - User: {getattr(request.user, 'email', 'anonymous')}"
                )
            
            # Log all API requests in production
            if not settings.DEBUG and request.path.startswith('/api/'):
                logger.info(
                    f"{request.method} {request.path} "
                    f"- Status: {response.status_code} "
                    f"- Duration: {duration:.3f}s "
                    f"- User: {getattr(request.user, 'email', 'anonymous')}"
                )
        
        return response


class InputSanitizationMiddleware(MiddlewareMixin):
    """
    Sanitize user input to prevent injection attacks
    """
    
    DANGEROUS_PATTERNS = [
        '<script',
        'javascript:',
        'onerror=',
        'onload=',
        '../',
        '..\\',
    ]
    
    def process_request(self, request):
        # Check query parameters
        for key, value in request.GET.items():
            if isinstance(value, str) and self.contains_dangerous_pattern(value):
                logger.warning(f"Dangerous pattern detected in query param: {key}={value}")
                return JsonResponse({
                    'type': 'about:blank',
                    'title': 'Bad Request',
                    'status': 400,
                    'detail': 'Invalid input detected.',
                    'instance': request.path,
                }, status=400)
        
        return None
    
    def contains_dangerous_pattern(self, value):
        """Check if value contains dangerous patterns"""
        value_lower = value.lower()
        return any(pattern in value_lower for pattern in self.DANGEROUS_PATTERNS)


class CORSSecurityMiddleware(MiddlewareMixin):
    """
    Enhanced CORS security
    """
    
    def process_response(self, request, response):
        # Only allow CORS for API endpoints
        if request.path.startswith('/api/'):
            origin = request.META.get('HTTP_ORIGIN')
            
            # Check if origin is allowed
            allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
            
            if origin in allowed_origins:
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
                response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response['Access-Control-Max-Age'] = '3600'
        
        return response
