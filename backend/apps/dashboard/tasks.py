"""
Celery Tasks for Dashboard Metrics
Requirement 21: Background Task Processing
Requirement 16: Real-time metrics
"""
from celery import shared_task
import logging
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from datetime import timedelta
from .models import SystemMetrics
from apps.uploads.models import UploadSession
from apps.authentication.models import User

logger = logging.getLogger(__name__)


@shared_task
def update_metrics_task():
    """
    Update system metrics
    Runs every 5 minutes
    """
    logger.info("Updating system metrics")
    
    try:
        now = timezone.now()
        
        # Calculate upload metrics
        uploads_24h = UploadSession.objects.filter(
            created_at__gte=now - timedelta(hours=24),
            status='completed'
        ).count()
        
        uploads_7d = UploadSession.objects.filter(
            created_at__gte=now - timedelta(days=7),
            status='completed'
        ).count()
        
        uploads_30d = UploadSession.objects.filter(
            created_at__gte=now - timedelta(days=30),
            status='completed'
        ).count()
        
        # Calculate success rate
        total_uploads = UploadSession.objects.filter(
            created_at__gte=now - timedelta(hours=24)
        ).count()
        
        upload_success_rate = (uploads_24h / total_uploads * 100) if total_uploads > 0 else 100.0
        
        # Calculate processing metrics
        from apps.conversion.models import ConversionJob
        
        jobs_pending = ConversionJob.objects.filter(status='pending').count() if hasattr(ConversionJob, 'objects') else 0
        jobs_processing = ConversionJob.objects.filter(status='processing').count() if hasattr(ConversionJob, 'objects') else 0
        jobs_completed = ConversionJob.objects.filter(status='completed').count() if hasattr(ConversionJob, 'objects') else 0
        jobs_failed = ConversionJob.objects.filter(status='failed').count() if hasattr(ConversionJob, 'objects') else 0
        
        # Calculate user metrics
        active_users = User.objects.filter(
            last_login__gte=now - timedelta(hours=24)
        ).count()
        
        total_users = User.objects.count()
        
        # Calculate storage metrics
        total_storage = User.objects.aggregate(
            total=Sum('storage_used')
        )['total'] or 0
        
        # Create metrics snapshot
        metrics = SystemMetrics.objects.create(
            total_uploads_24h=uploads_24h,
            total_uploads_7d=uploads_7d,
            total_uploads_30d=uploads_30d,
            upload_success_rate=upload_success_rate,
            jobs_pending=jobs_pending,
            jobs_processing=jobs_processing,
            jobs_completed=jobs_completed,
            jobs_failed=jobs_failed,
            queue_depth=jobs_pending + jobs_processing,
            active_users=active_users,
            total_users=total_users,
            total_storage_bytes=total_storage,
        )
        
        logger.info(f"System metrics updated: {metrics.id}")
        return {'success': True, 'metrics_id': str(metrics.id)}
        
    except Exception as e:
        logger.exception(f"Failed to update metrics: {str(e)}")
        return {'success': False, 'error': str(e)}
