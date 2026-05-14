"""
Celery Tasks for Document Conversion
Requirement 21: Background Task Processing
"""
from celery import shared_task
import logging
import os
from .services import FileConversionService
from .ocr_service import OCRService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def convert_file_task(self, input_path, output_path, conversion_type):
    """
    Generic file conversion task
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
        conversion_type: Type of conversion (pdf_to_word, word_to_pdf, etc.)
    """
    try:
        logger.info(f"Starting {conversion_type} conversion: {input_path}")
        service = FileConversionService()
        
        if conversion_type == 'pdf_to_word':
            result = service.pdf_to_word(input_path, output_path)
        elif conversion_type == 'word_to_pdf':
            result = service.word_to_pdf(input_path, output_path)
        elif conversion_type == 'excel_to_pdf':
            result = service.excel_to_pdf(input_path, output_path)
        elif conversion_type == 'powerpoint_to_pdf':
            result = service.powerpoint_to_pdf(input_path, output_path)
        elif conversion_type == 'text_to_pdf':
            result = service.text_to_pdf(input_path, output_path)
        elif conversion_type == 'image_to_pdf':
            result = service.image_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unknown conversion type: {conversion_type}")
        
        logger.info(f"Conversion completed: {output_path}")
        return result
    except Exception as e:
        logger.exception(f"Conversion failed: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def convert_pdf_to_word_task(self, input_path, output_path):
    """
    Background task for PDF to Word conversion
    """
    try:
        logger.info(f"Starting PDF to Word conversion: {input_path}")
        service = FileConversionService()
        result = service.pdf_to_word(input_path, output_path)
        logger.info(f"PDF to Word conversion completed: {output_path}")
        return result
    except Exception as e:
        logger.exception(f"PDF to Word conversion failed: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def convert_word_to_pdf_task(self, input_path, output_path):
    """
    Background task for Word to PDF conversion
    """
    try:
        logger.info(f"Starting Word to PDF conversion: {input_path}")
        service = FileConversionService()
        result = service.word_to_pdf(input_path, output_path)
        logger.info(f"Word to PDF conversion completed: {output_path}")
        return result
    except Exception as e:
        logger.exception(f"Word to PDF conversion failed: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def convert_pdf_to_images_task(self, input_path, output_dir, dpi=150, format='jpg'):
    """
    Background task for PDF to images conversion
    """
    try:
        logger.info(f"Starting PDF to images conversion: {input_path}")
        service = FileConversionService()
        result = service.pdf_to_images(input_path, output_dir, dpi, format)
        logger.info(f"PDF to images conversion completed: {len(result['output_files'])} pages")
        return result
    except Exception as e:
        logger.exception(f"PDF to images conversion failed: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def ocr_extract_text_task(self, file_path, language='english', output_pdf_path=None):
    """
    Background task for OCR text extraction
    """
    try:
        logger.info(f"Starting OCR extraction: {file_path}")
        service = OCRService()
        
        if file_path.lower().endswith('.pdf'):
            result = service.extract_text_from_pdf(file_path, language, output_pdf_path)
        else:
            result = service.extract_text_from_image(file_path, language)
        
        logger.info(f"OCR extraction completed: {result['word_count']} words")
        return result
    except Exception as e:
        logger.exception(f"OCR extraction failed: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def convert_excel_to_pdf_task(self, input_path, output_path):
    """
    Background task for Excel to PDF conversion
    """
    try:
        logger.info(f"Starting Excel to PDF conversion: {input_path}")
        service = FileConversionService()
        result = service.excel_to_pdf(input_path, output_path)
        logger.info(f"Excel to PDF conversion completed: {output_path}")
        return result
    except Exception as e:
        logger.exception(f"Excel to PDF conversion failed: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def convert_powerpoint_to_pdf_task(self, input_path, output_path):
    """
    Background task for PowerPoint to PDF conversion
    """
    try:
        logger.info(f"Starting PowerPoint to PDF conversion: {input_path}")
        service = FileConversionService()
        result = service.powerpoint_to_pdf(input_path, output_path)
        logger.info(f"PowerPoint to PDF conversion completed: {output_path}")
        return result
    except Exception as e:
        logger.exception(f"PowerPoint to PDF conversion failed: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
