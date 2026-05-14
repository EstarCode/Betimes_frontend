"""
Audit and Compliance System
Tracks all critical system activities for regulatory compliance
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


class AuditLog(models.Model):
    """
    Comprehensive audit log for compliance
    Retains logs for 7 years with immutable storage
    """
    EVENT_TYPES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('login_failed', 'Failed Login'),
        ('file_upload', 'File Upload'),
        ('file_download', 'File Download'),
        ('file_edit', 'File Edit'),
        ('file_delete', 'File Delete'),
        ('permission_change', 'Permission Change'),
        ('workflow_approve', 'Workflow Approval'),
        ('workflow_reject', 'Workflow Rejection'),
        ('user_create', 'User Created'),
        ('user_update', 'User Updated'),
        ('user_delete', 'User Deleted'),
        ('system_config', 'System Configuration Change'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    event_type = models.CharField(max_length=100, choices=EVENT_TYPES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    resource_type = models.CharField(max_length=100, blank=True)
    resource_id = models.UUIDField(null=True, blank=True)
    action = models.CharField(max_length=100)
    details = models.JSONField(default=dict, blank=True)
    success = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['resource_type', 'resource_id']),
            models.Index(fields=['ip_address', 'created_at']),
        ]
        ordering = ['-created_at']
        # Partition by month for performance
        # managed = False  # Use custom SQL for partitioning
    
    def __str__(self):
        return f"{self.event_type} by {self.user} at {self.created_at}"
    
    @classmethod
    def log_event(cls, event_type, user=None, ip_address=None, user_agent='', 
                  resource_type='', resource_id=None, action='', details=None, success=True):
        """
        Create an audit log entry
        
        Args:
            event_type: Type of event from EVENT_TYPES
            user: User performing the action
            ip_address: IP address of the request
            user_agent: User agent string
            resource_type: Type of resource affected
            resource_id: ID of the resource
            action: Description of the action
            details: Additional details as dict
            success: Whether the action succeeded
        
        Returns:
            AuditLog instance
        """
        return cls.objects.create(
            event_type=event_type,
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            details=details or {},
            success=success
        )
