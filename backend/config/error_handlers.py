"""
Comprehensive error handlers following RFC 7807 (Problem Details for HTTP APIs)
and OWASP best practices
"""
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
import logging
import traceback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns RFC 7807 compliant error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data
        custom_response_data = {
            'type': f'about:blank',
            'title': exc.__class__.__name__,
            'status': response.status_code,
            'detail': str(exc),
            'instance': context['request'].path
        }
        
        # Add validation errors if present
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                custom_response_data['errors'] = exc.detail
            elif isinstance(exc.detail, list):
                custom_response_data['errors'] = exc.detail
        
        response.data = custom_response_data
        
        # Log the error
        logger.error(
            f"API Error: {exc.__class__.__name__} - {str(exc)}",
            extra={
                'status_code': response.status_code,
                'path': context['request'].path,
                'method': context['request'].method,
            }
        )
    
    return response


def handler400(request, exception=None):
    """Handle 400 Bad Request errors"""
    return JsonResponse({
        'type': 'about:blank',
        'title': 'Bad Request',
        'status': 400,
        'detail': 'The request could not be understood by the server.',
        'instance': request.path
    }, status=400)


def handler403(request, exception=None):
    """Handle 403 Forbidden errors"""
    return JsonResponse({
        'type': 'about:blank',
        'title': 'Forbidden',
        'status': 403,
        'detail': 'You do not have permission to access this resource.',
        'instance': request.path
    }, status=403)


def handler404(request, exception=None):
    """Handle 404 Not Found errors"""
    return JsonResponse({
        'type': 'about:blank',
        'title': 'Not Found',
        'status': 404,
        'detail': 'The requested resource was not found.',
        'instance': request.path
    }, status=404)


def handler500(request):
    """Handle 500 Internal Server Error"""
    logger.error(
        "Internal Server Error",
        extra={
            'path': request.path,
            'method': request.method,
        },
        exc_info=True
    )
    
    return JsonResponse({
        'type': 'about:blank',
        'title': 'Internal Server Error',
        'status': 500,
        'detail': 'An unexpected error occurred. Please try again later.',
        'instance': request.path
    }, status=500)
