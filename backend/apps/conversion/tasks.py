"""
Celery tasks for file conversion.
"""

import os
import time
from celery import shared_task
from django.core.files import File
from django.utils import timezone
from datetime import timedelta
from .models import ConversionJob
from .services import FileConversionService
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def convert_file_task(self, job_id):
    """
    Celery task to convert a file.
    
    Args:
        job_id: UUID of the ConversionJob
    
    Returns:
        dict: Task result with status and details
    """
    try:
        # Get the job
        job = ConversionJob.objects.get(id=job_id)
        job.status = 'processing'
        job.save()
        
        logger.info(f"Starting conversion task for job {job_id}")
        
        # Start timing
        start_time = time.time()
        
        # Initialize conversion service
        conversion_service = FileConversionService()
        
        # Get file paths
        input_path = job.input_file.path
        output_filename = f"converted_{os.path.splitext(os.path.basename(input_path))[0]}"
        
        # Determine output extension based on conversion type
        if 'to_pdf' in job.conversion_type:
            output_filename += '.pdf'
        elif 'to_word' in job.conversion_type:
            output_filename += '.docx'
        elif 'to_image' in job.conversion_type:
            output_filename += '.png'
        elif 'to_text' in job.conversion_type:
            output_filename += '.txt'
        else:
            output_filename += '.pdf'
        
        output_path = os.path.join(
            os.path.dirname(input_path).replace('input', 'output'),
            output_filename
        )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Perform conversion based on type
        if job.conversion_type == 'word_to_pdf':
            conversion_service.word_to_pdf(input_path, output_path)
        elif job.conversion_type == 'image_to_pdf':
            conversion_service.image_to_pdf(input_path, output_path)
        elif job.conversion_type == 'pdf_to_image':
            conversion_service.pdf_to_image(input_path, output_path)
        elif job.conversion_type == 'pdf_to_text':
            conversion_service.pdf_to_text(input_path, output_path)
        elif job.conversion_type == 'excel_to_pdf':
            conversion_service.excel_to_pdf(input_path, output_path)
        elif job.conversion_type == 'ppt_to_pdf':
            conversion_service.ppt_to_pdf(input_path, output_path)
        else:
            raise Exception(f"Unsupported conversion type: {job.conversion_type}")
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update job with results
        with open(output_path, 'rb') as f:
            job.output_file.save(output_filename, File(f), save=False)
        
        job.output_size = os.path.getsize(output_path)
        job.processing_time = processing_time
        job.status = 'completed'
        job.completed_at = timezone.now()
        job.save()
        
        logger.info(f"Conversion task completed for job {job_id}")
        
        return {
            'status': 'success',
            'job_id': str(job_id),
            'processing_time': processing_time
        }
        
    except ConversionJob.DoesNotExist:
        logger.error(f"Job {job_id} not found")
        return {'status': 'error', 'message': 'Job not found'}
    
    except Exception as e:
        logger.exception(f"Conversion task failed for job {job_id}: {str(e)}")
        
        # Update job status
        try:
            job = ConversionJob.objects.get(id=job_id)
            job.status = 'failed'
            job.error_message = str(e)
            job.save()
        except:
            pass
        
        # Retry the task
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        
        return {'status': 'error', 'message': str(e)}


@shared_task
def cleanup_old_conversion_files():
    """
    Celery task to cleanup old conversion files (older than 7 days).
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=7)
        old_jobs = ConversionJob.objects.filter(created_at__lt=cutoff_date)
        
        count = 0
        for job in old_jobs:
            # Delete files
            if job.input_file:
                job.input_file.delete(save=False)
            if job.output_file:
                job.output_file.delete(save=False)
            
            job.delete()
            count += 1
        
        logger.info(f"Cleaned up {count} old conversion jobs")
        return {'status': 'success', 'deleted_count': count}
        
    except Exception as e:
        logger.exception(f"Cleanup task failed: {str(e)}")
        return {'status': 'error', 'message': str(e)}
