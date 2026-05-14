"""
Custom Exception Handlers
International Standard Error Handling (RFC 7807 - Problem Details for HTTP APIs)
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


# Custom Exceptions
class ConversionError(Exception):
    """Exception raised for file conversion errors"""
    pass


class CompressionError(Exception):
    """Exception raised for PDF compression errors"""
    pass


class PDFError(Exception):
    """Exception raised for PDF manipulation errors"""
    pass


class OCRError(Exception):
    """Exception raised for OCR processing errors"""
    pass


class SearchError(Exception):
    """Exception raised for search errors"""
    pass


class WorkflowError(Exception):
    """Exception raised for workflow errors"""
    pass


def custom_exception_handler(exc, context):
    """
    Custom exception handler following RFC 7807 standard
    Returns consistent error responses with proper logging
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    request = context.get('request')
    view = context.get('view')
    
    log_data = {
        'exception_type': type(exc).__name__,
        'exception_message': str(exc),
        'path': request.path if request else None,
        'method': request.method if request else None,
        'user': request.user.email if request and hasattr(request, 'user') and request.user.is_authenticated else 'anonymous',
        'view': view.__class__.__name__ if view else None,
    }
    
    logger.error(f"API Exception: {log_data}")
    
    # If response is None, it's not a DRF exception
    if response is None:
        # Handle custom exceptions
        if isinstance(exc, (ConversionError, CompressionError, PDFError, OCRError, SearchError, WorkflowError)):
            response = Response(
                {
                    'type': 'about:blank',
                    'title': type(exc).__name__,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'detail': str(exc),
                    'instance': request.path if request else None,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # Generic server error
            response = Response(
                {
                    'type': 'about:blank',
                    'title': 'Internal Server Error',
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'detail': 'An unexpected error occurred. Please try again later.',
                    'instance': request.path if request else None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        # Enhance DRF exception response with RFC 7807 format
        if isinstance(response.data, dict):
            error_data = {
                'type': 'about:blank',
                'title': response.data.get('detail', 'Error'),
                'status': response.status_code,
                'detail': response.data.get('detail', str(exc)),
                'instance': request.path if request else None,
            }
            
            # Add validation errors if present
            if 'detail' not in response.data:
                error_data['errors'] = response.data
            
            response.data = error_data
    
    return response


def handle_404(request, exception=None):
    """Custom 404 handler"""
    return Response(
        {
            'type': 'about:blank',
            'title': 'Not Found',
            'status': 404,
            'detail': 'The requested resource was not found.',
            'instance': request.path,
        },
        status=status.HTTP_404_NOT_FOUND
    )


def handle_500(request):
    """Custom 500 handler"""
    logger.critical(f"500 Error on {request.path}")
    return Response(
        {
            'type': 'about:blank',
            'title': 'Internal Server Error',
            'status': 500,
            'detail': 'An unexpected error occurred. Our team has been notified.',
            'instance': request.path,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
