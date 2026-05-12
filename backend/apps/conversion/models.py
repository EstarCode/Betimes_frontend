"""
Models for file conversion.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid


class ConversionJob(models.Model):
    """Model to track file conversion jobs."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    CONVERSION_TYPE_CHOICES = [
        ('word_to_pdf', 'Word to PDF'),
        ('image_to_pdf', 'Image to PDF'),
        ('pdf_to_word', 'PDF to Word'),
        ('pdf_to_image', 'PDF to Image'),
        ('excel_to_pdf', 'Excel to PDF'),
        ('ppt_to_pdf', 'PowerPoint to PDF'),
        ('pdf_to_text', 'PDF to Text'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversion_jobs')
    
    input_file = models.FileField(upload_to='conversions/input/%Y/%m/%d/')
    output_file = models.FileField(upload_to='conversions/output/%Y/%m/%d/', null=True, blank=True)
    
    conversion_type = models.CharField(max_length=20, choices=CONVERSION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    input_size = models.BigIntegerField(default=0)
    output_size = models.BigIntegerField(default=0)
    processing_time = models.FloatField(default=0.0)
    
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'conversion_jobs'
        verbose_name = _('Conversion Job')
        verbose_name_plural = _('Conversion Jobs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['conversion_type']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.get_conversion_type_display()} - {self.status}"
