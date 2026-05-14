"""
Celery Tasks for PDF Compression
Requirement 21: Background Task Processing
"""
from celery import shared_task
import logging
from .services import PDFCompressionService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def compress_pdf_task(self, input_path, output_path, compression_level='medium'):
    """
    Background task for PDF compression
    
    Args:
        input_path: Path to input PDF
        output_path: Path to save compressed PDF
        compression_level: Compression level (low, medium, high)
    
    Returns:
        dict: Compression results
    """
    try:
        logger.info(f"Starting PDF compression: {input_path} (level: {compression_level})")
        service = PDFCompressionService()
        result = service.compress_pdf(input_path, output_path, compression_level)
        logger.info(f"PDF compression completed: {result['compression_ratio']}% reduction")
        return result
    except Exception as e:
        logger.exception(f"PDF compression failed: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
