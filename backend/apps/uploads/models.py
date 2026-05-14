"""
Chunked Upload Models for handling large file uploads up to 10GB
Supports resumable uploads with integrity validation
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid

User = get_user_model()


class UploadSession(models.Model):
    """
    Manages chunked upload sessions for large files
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_sessions')
    filename = models.CharField(max_length=500)
    file_size = models.BigIntegerField(validators=[MinValueValidator(0)])
    chunk_size = models.IntegerField(default=10485760)  # 10MB default
    total_chunks = models.IntegerField(validators=[MinValueValidator(1)])
    uploaded_chunks = models.IntegerField(default=0)
    checksum_sha256 = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    storage_temp_path = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'upload_sessions'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.filename} - {self.status}"
    
    @property
    def progress_percentage(self):
        """Calculate upload progress percentage"""
        if self.total_chunks == 0:
            return 0
        return (self.uploaded_chunks / self.total_chunks) * 100
    
    @property
    def is_complete(self):
        """Check if all chunks are uploaded"""
        return self.uploaded_chunks == self.total_chunks


class UploadChunk(models.Model):
    """
    Represents individual chunks of a file upload
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload_session = models.ForeignKey(
        UploadSession, 
        on_delete=models.CASCADE, 
        related_name='chunks'
    )
    chunk_number = models.IntegerField(validators=[MinValueValidator(0)])
    chunk_size = models.IntegerField(validators=[MinValueValidator(0)])
    checksum_sha256 = models.CharField(max_length=64)
    storage_path = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'upload_chunks'
        unique_together = [['upload_session', 'chunk_number']]
        indexes = [
            models.Index(fields=['upload_session', 'chunk_number']),
        ]
        ordering = ['chunk_number']
    
    def __str__(self):
        return f"Chunk {self.chunk_number} of {self.upload_session.filename}"
