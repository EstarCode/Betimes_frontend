"""
Celery tasks for PDF compression.
"""

import os
import time
from celery import shared_task
from django.core.files import File
from django.utils import timezone
from datetime import timedelta
from .models import CompressionJob
from .services import PDFCompressionService
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def compress_pdf_task(self, job_id):
    """
    Celery task to compress a PDF file.
    
    Args:
        job_id: UUID of the CompressionJob
    
    Returns:
        dict: Task result with status and details
    """
    try:
        # Get the job
        job = CompressionJob.objects.get(id=job_id)
        job.status = 'processing'
        job.save()
        
        logger.info(f"Starting compression task for job {job_id}")
        
        # Start timing
        start_time = time.time()
        
        # Initialize compression service
        compression_service = PDFCompressionService()
        
        # Get file paths
        input_path = job.original_file.path
        output_filename = f"compressed_{os.path.basename(input_path)}"
        output_path = os.path.join(
            os.path.dirname(input_path).replace('original', 'compressed'),
            output_filename
        )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Validate PDF
        if not compression_service.validate_pdf(input_path):
            raise Exception("Invalid PDF file")
        
        # Compress the PDF
        result = compression_service.compress_pdf(
            input_path,
            output_path,
            job.compression_level
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time

        
        # Update job with results
        with open(output_path, 'rb') as f:
            job.compressed_file.save(output_filename, File(f), save=False)
        
        job.original_size = result['original_size']
        job.compressed_size = result['compressed_size']
        job.compression_ratio = result['compression_ratio']
        job.processing_time = processing_time
        job.status = 'completed'
        job.completed_at = timezone.now()
        job.save()
        
        logger.info(f"Compression task completed for job {job_id}")
        
        return {
            'status': 'success',
            'job_id': str(job_id),
            'compression_ratio': result['compression_ratio'],
            'processing_time': processing_time
        }
        
    except CompressionJob.DoesNotExist:
        logger.error(f"Job {job_id} not found")
        return {'status': 'error', 'message': 'Job not found'}
    
    except Exception as e:
        logger.exception(f"Compression task failed for job {job_id}: {str(e)}")
        
        # Update job status
        try:
            job = CompressionJob.objects.get(id=job_id)
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
def cleanup_old_files():
    """
    Celery task to cleanup old files (older than 7 days).
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=7)
        old_jobs = CompressionJob.objects.filter(created_at__lt=cutoff_date)
        
        count = 0
        for job in old_jobs:
            # Delete files
            if job.original_file:
                job.original_file.delete(save=False)
            if job.compressed_file:
                job.compressed_file.delete(save=False)
            
            job.delete()
            count += 1
        
        logger.info(f"Cleaned up {count} old compression jobs")
        return {'status': 'success', 'deleted_count': count}
        
    except Exception as e:
        logger.exception(f"Cleanup task failed: {str(e)}")
        return {'status': 'error', 'message': str(e)}


@shared_task
def cleanup_failed_jobs():
    """
    Celery task to cleanup failed jobs older than 24 hours.
    """
    try:
        cutoff_date = timezone.now() - timedelta(hours=24)
        failed_jobs = CompressionJob.objects.filter(
            status='failed',
            created_at__lt=cutoff_date
        )
        
        count = 0
        for job in failed_jobs:
            if job.original_file:
                job.original_file.delete(save=False)
            job.delete()
            count += 1
        
        logger.info(f"Cleaned up {count} failed compression jobs")
        return {'status': 'success', 'deleted_count': count}
        
    except Exception as e:
        logger.exception(f"Failed jobs cleanup task failed: {str(e)}")
        return {'status': 'error', 'message': str(e)}
