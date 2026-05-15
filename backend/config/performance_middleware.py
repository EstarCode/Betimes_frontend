"""
Performance Optimization Middleware
For handling 100,000+ concurrent users
"""
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import hashlib
import time


class CacheMiddleware(MiddlewareMixin):
    """
    Aggressive caching for GET requests
    """
    CACHE_DURATION = 300  # 5 minutes
    CACHEABLE_PATHS = ['/api/v1/dashboard/', '/api/v1/analytics/', '/health/']
    
    def process_request(self, request):
        # Only cache GET requests
        if request.method != 'GET':
            return None
        
        # Check if path is cacheable
        if not any(request.path.startswith(path) for path in self.CACHEABLE_PATHS):
            return None
        
        # Generate cache key
        cache_key = self._generate_cache_key(request)
        
        # Try to get from cache
        cached_response = cache.get(cache_key)
        if cached_response:
            response = HttpResponse(
                cached_response['content'],
                status=cached_response['status'],
                content_type=cached_response['content_type']
            )
            response['X-Cache'] = 'HIT'
            return response
        
        return None
    
    def process_response(self, request, response):
        # Only cache successful GET requests
        if request.method != 'GET' or response.status_code != 200:
            return response
        
        # Check if path is cacheable
        if not any(request.path.startswith(path) for path in self.CACHEABLE_PATHS):
            return response
        
        # Generate cache key
        cache_key = self._generate_cache_key(request)
        
        # Cache the response
        cache.set(cache_key, {
            'content': response.content,
            'status': response.status_code,
            'content_type': response.get('Content-Type', 'text/html')
        }, self.CACHE_DURATION)
        
        response['X-Cache'] = 'MISS'
        return response
    
    def _generate_cache_key(self, request):
        """Generate unique cache key for request"""
        key_data = f"{request.path}:{request.GET.urlencode()}"
        return f"view_cache:{hashlib.md5(key_data.encode()).hexdigest()}"


class CompressionMiddleware(MiddlewareMixin):
    """
    Add compression headers for better bandwidth usage
    """
    def process_response(self, request, response):
        # Add Vary header for caching
        if 'Vary' not in response:
            response['Vary'] = 'Accept-Encoding'
        else:
            if 'Accept-Encoding' not in response['Vary']:
                response['Vary'] += ', Accept-Encoding'
        
        return response


class PerformanceHeadersMiddleware(MiddlewareMixin):
    """
    Add performance-related headers
    """
    def process_response(self, request, response):
        # Add cache control headers
        if request.method == 'GET' and response.status_code == 200:
            if '/api/' in request.path:
                response['Cache-Control'] = 'public, max-age=300'  # 5 minutes
            elif '/static/' in request.path:
                response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
        
        # Add performance hints
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        
        return response


class RequestTimingMiddleware(MiddlewareMixin):
    """
    Track request timing for monitoring
    """
    def process_request(self, request):
        request._start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            response['X-Request-Duration'] = f"{duration:.3f}s"
        return response
