"""
Models for PDF compression.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid


class CompressionJob(models.Model):
    """Model to track PDF compression jobs."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    COMPRESSION_LEVEL_CHOICES = [
        ('low', 'Low Compression'),
        ('medium', 'Medium Compression'),
        ('high', 'High Compression'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='compression_jobs')
    original_file = models.FileField(upload_to='uploads/original/%Y/%m/%d/')
    compressed_file = models.FileField(upload_to='uploads/compressed/%Y/%m/%d/', null=True, blank=True)
    
    compression_level = models.CharField(max_length=10, choices=COMPRESSION_LEVEL_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    original_size = models.BigIntegerField(default=0, help_text="Original file size in bytes")
    compressed_size = models.BigIntegerField(default=0, help_text="Compressed file size in bytes")
    compression_ratio = models.FloatField(default=0.0, help_text="Compression ratio percentage")
    
    processing_time = models.FloatField(default=0.0, help_text="Processing time in seconds")
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'compression_jobs'
        verbose_name = _('Compression Job')
        verbose_name_plural = _('Compression Jobs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.compression_level} - {self.status}"

    @property
    def size_reduction(self):
        """Calculate size reduction in bytes."""
        if self.compressed_size:
            return self.original_size - self.compressed_size
        return 0

    def calculate_compression_ratio(self):
        """Calculate and update compression ratio."""
        if self.original_size > 0 and self.compressed_size > 0:
            reduction = ((self.original_size - self.compressed_size) / self.original_size) * 100
            self.compression_ratio = round(reduction, 2)
        return self.compression_ratio
