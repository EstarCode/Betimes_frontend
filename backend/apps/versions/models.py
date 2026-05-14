"""
Document Version Control Models
Tracks document versions with history and rollback capability
"""
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Document(models.Model):
    """
    Main document model with version tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=500)
    original_filename = models.CharField(max_length=500)
    file_type = models.CharField(max_length=50)
    current_version = models.IntegerField(default=1)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100, blank=True)
    checksum_sha256 = models.CharField(max_length=64)
    storage_path = models.TextField()
    storage_bucket = models.CharField(max_length=255, blank=True)
    encrypted = models.BooleanField(default=True)
    encryption_key_id = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    department = models.CharField(max_length=100, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'documents'
        indexes = [
            models.Index(fields=['owner', 'is_deleted']),
            models.Index(fields=['file_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['checksum_sha256']),
            models.Index(fields=['department']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.filename} (v{self.current_version})"


class DocumentVersion(models.Model):
    """
    Individual version of a document
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    file_size = models.BigIntegerField()
    checksum_sha256 = models.CharField(max_length=64)
    storage_path = models.TextField()
    is_rollback = models.BooleanField(default=False)
    rollback_from_version = models.IntegerField(null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'document_versions'
        unique_together = [['document', 'version_number']]
        indexes = [
            models.Index(fields=['document', 'version_number']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-version_number']
    
    def __str__(self):
        return f"{self.document.filename} v{self.version_number}"
