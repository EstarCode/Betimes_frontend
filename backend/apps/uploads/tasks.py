"""
Celery Tasks for Upload Management
Requirement 21: Background Task Processing
"""
from celery import shared_task
import logging
import os
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def cleanup_temp_files_task():
    """
    Clean up expired temporary files
    Runs daily at 2 AM
    """
    logger.info("Starting temporary files cleanup task")
    
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    if not os.path.exists(temp_dir):
        logger.info("Temp directory does not exist")
        return {'deleted_count': 0}
    
    cutoff_time = timezone.now() - timedelta(days=1)
    deleted_count = 0
    
    try:
        for root, dirs, files in os.walk(temp_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Check file modification time
                file_mtime = os.path.getmtime(file_path)
                file_datetime = timezone.datetime.fromtimestamp(file_mtime, tz=timezone.utc)
                
                if file_datetime < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        logger.debug(f"Deleted temp file: {file_path}")
                    except Exception as e:
                        logger.error(f"Failed to delete {file_path}: {str(e)}")
        
        logger.info(f"Cleaned up {deleted_count} temporary files")
        return {'deleted_count': deleted_count}
        
    except Exception as e:
        logger.exception(f"Temp files cleanup failed: {str(e)}")
        return {'deleted_count': deleted_count, 'error': str(e)}


@shared_task
def cleanup_incomplete_uploads_task():
    """
    Clean up incomplete upload sessions older than 24 hours
    """
    from .models import UploadSession
    
    logger.info("Starting incomplete uploads cleanup task")
    
    cutoff_time = timezone.now() - timedelta(hours=24)
    
    deleted_count, _ = UploadSession.objects.filter(
        status='in_progress',
        created_at__lt=cutoff_time
    ).delete()
    
    logger.info(f"Cleaned up {deleted_count} incomplete upload sessions")
    return {'deleted_count': deleted_count}
