"""
Views for enterprise dashboard
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from .models import SystemMetrics
from apps.uploads.models import UploadSession
from apps.versions.models import Document
from apps.authentication.models import User


class DashboardMetricsView(APIView):
    """
    Get real-time dashboard metrics
    
    GET /api/v1/dashboard/metrics/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get latest metrics or calculate
        latest_metrics = SystemMetrics.get_latest()
        
        if not latest_metrics or (timezone.now() - latest_metrics.timestamp).seconds > 30:
            # Calculate fresh metrics
            now = timezone.now()
            
            # Upload statistics
            uploads_24h = UploadSession.objects.filter(
                created_at__gte=now - timedelta(hours=24)
            ).count()
            
            uploads_7d = UploadSession.objects.filter(
                created_at__gte=now - timedelta(days=7)
            ).count()
            
            uploads_30d = UploadSession.objects.filter(
                created_at__gte=now - timedelta(days=30)
            ).count()
            
            # Job statistics
            from apps.conversion.models import ProcessingJob
            jobs_pending = ProcessingJob.objects.filter(status='pending').count()
            jobs_processing = ProcessingJob.objects.filter(status='processing').count()
            jobs_completed = ProcessingJob.objects.filter(status='completed').count()
            jobs_failed = ProcessingJob.objects.filter(status='failed').count()
            
            # User statistics
            active_users = User.objects.filter(is_active=True).count()
            total_users = User.objects.count()
            
            # Storage statistics
            total_storage = Document.objects.aggregate(
                total=Sum('file_size')
            )['total'] or 0
            
            metrics = {
                'uploads_24h': uploads_24h,
                'uploads_7d': uploads_7d,
                'uploads_30d': uploads_30d,
                'jobs_pending': jobs_pending,
                'jobs_processing': jobs_processing,
                'jobs_completed': jobs_completed,
                'jobs_failed': jobs_failed,
                'active_users': active_users,
                'total_users': total_users,
                'total_storage_bytes': total_storage,
                'timestamp': now
            }
        else:
            metrics = {
                'uploads_24h': latest_metrics.total_uploads_24h,
                'uploads_7d': latest_metrics.total_uploads_7d,
                'uploads_30d': latest_metrics.total_uploads_30d,
                'jobs_pending': latest_metrics.jobs_pending,
                'jobs_processing': latest_metrics.jobs_processing,
                'jobs_completed': latest_metrics.jobs_completed,
                'jobs_failed': latest_metrics.jobs_failed,
                'active_users': latest_metrics.active_users,
                'total_users': latest_metrics.total_users,
                'total_storage_bytes': latest_metrics.total_storage_bytes,
                'timestamp': latest_metrics.timestamp
            }
        
        return Response(metrics)


class UploadStatisticsView(APIView):
    """
    Get upload statistics
    
    GET /api/v1/dashboard/uploads/?period=7d
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        period = request.query_params.get('period', '7d')
        
        # Parse period
        if period == '24h':
            since = timezone.now() - timedelta(hours=24)
        elif period == '7d':
            since = timezone.now() - timedelta(days=7)
        elif period == '30d':
            since = timezone.now() - timedelta(days=30)
        else:
            since = timezone.now() - timedelta(days=7)
        
        uploads = UploadSession.objects.filter(created_at__gte=since)
        
        stats = {
            'total_uploads': uploads.count(),
            'completed': uploads.filter(status='completed').count(),
            'in_progress': uploads.filter(status='in_progress').count(),
            'failed': uploads.filter(status='failed').count(),
            'total_size': uploads.aggregate(total=Sum('file_size'))['total'] or 0
        }
        
        return Response(stats)


class StorageUsageView(APIView):
    """
    Get storage usage statistics
    
    GET /api/v1/dashboard/storage/?group_by=department
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        group_by = request.query_params.get('group_by', 'user')
        
        if group_by == 'department':
            usage = Document.objects.values('department').annotate(
                total_size=Sum('file_size'),
                document_count=Count('id')
            )
        elif group_by == 'user':
            usage = Document.objects.values('owner__email').annotate(
                total_size=Sum('file_size'),
                document_count=Count('id')
            )
        else:
            usage = []
        
        return Response({
            'group_by': group_by,
            'usage': list(usage)
        })
