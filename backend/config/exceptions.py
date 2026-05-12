"""
Custom exception handler for consistent API error responses.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data
        custom_response_data = {
            'success': False,
            'error': {
                'message': str(exc),
                'details': response.data if isinstance(response.data, dict) else {'detail': response.data}
            }
        }
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
    else:
        # Handle unexpected errors
        logger.exception(f"Unhandled exception: {exc}")
        response = Response(
            {
                'success': False,
                'error': {
                    'message': 'An unexpected error occurred.',
                    'details': {'detail': str(exc)}
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response


class FileValidationError(Exception):
    """Custom exception for file validation errors."""
    pass


class CompressionError(Exception):
    """Custom exception for compression errors."""
    pass


class ConversionError(Exception):
    """Custom exception for conversion errors."""
    pass


class PDFProcessingError(Exception):
    """Custom exception for PDF processing errors."""
    pass
