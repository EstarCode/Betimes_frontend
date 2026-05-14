"""
Notification System Models
Supports email, SMS, in-app, Slack, and Microsoft Teams notifications
"""
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Notification(models.Model):
    """
    Individual notification
    """
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('in_app', 'In-App'),
        ('slack', 'Slack'),
        ('teams', 'Microsoft Teams'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50)
    channel = models.CharField(max_length=50, choices=CHANNEL_CHOICES)
    subject = models.CharField(max_length=500, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.type} to {self.user} via {self.channel}"
    
    @property
    def is_read(self):
        return self.read_at is not None


class NotificationPreference(models.Model):
    """
    User notification preferences
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    in_app_enabled = models.BooleanField(default=True)
    slack_enabled = models.BooleanField(default=False)
    teams_enabled = models.BooleanField(default=False)
    event_preferences = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'notification_preferences'
    
    def __str__(self):
        return f"Preferences for {self.user}"
