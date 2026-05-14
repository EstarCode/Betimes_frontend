"""
Dashboard and Metrics Models
Real-time system metrics and activity tracking
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class SystemMetrics(models.Model):
    """
    System-wide metrics snapshot
    """
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Upload metrics
    total_uploads_24h = models.IntegerField(default=0)
    total_uploads_7d = models.IntegerField(default=0)
    total_uploads_30d = models.IntegerField(default=0)
    upload_success_rate = models.FloatField(default=0.0)
    
    # Processing metrics
    jobs_pending = models.IntegerField(default=0)
    jobs_processing = models.IntegerField(default=0)
    jobs_completed = models.IntegerField(default=0)
    jobs_failed = models.IntegerField(default=0)
    queue_depth = models.IntegerField(default=0)
    avg_wait_time_seconds = models.FloatField(default=0.0)
    
    # User metrics
    active_users = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    
    # Storage metrics
    total_storage_bytes = models.BigIntegerField(default=0)
    storage_by_department = models.JSONField(default=dict, blank=True)
    
    # Performance metrics
    api_response_time_p50 = models.FloatField(default=0.0)
    api_response_time_p95 = models.FloatField(default=0.0)
    api_response_time_p99 = models.FloatField(default=0.0)
    queue_processing_rate = models.FloatField(default=0.0)
    error_rate = models.FloatField(default=0.0)
    cache_hit_rate = models.FloatField(default=0.0)
    
    # System health
    cpu_usage_percent = models.FloatField(default=0.0)
    memory_usage_percent = models.FloatField(default=0.0)
    disk_usage_percent = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'system_metrics'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"Metrics at {self.timestamp}"
    
    @classmethod
    def get_latest(cls):
        """Get the most recent metrics snapshot"""
        return cls.objects.first()
    
    @classmethod
    def get_time_series(cls, hours=24):
        """Get metrics for the last N hours"""
        since = timezone.now() - timedelta(hours=hours)
        return cls.objects.filter(timestamp__gte=since)


class UserActivity(models.Model):
    """
    Track user activity for analytics
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'user_activities'
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type', '-timestamp']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.activity_type} at {self.timestamp}"
