"""
Search Engine Models
Full-text search with PostgreSQL
Requirement 17: Global Search System
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
import uuid

User = get_user_model()


class DocumentIndex(models.Model):
    """
    Full-text search index for documents
    Uses PostgreSQL full-text search for performance
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Document reference
    document_id = models.UUIDField(db_index=True)
    filename = models.CharField(max_length=500)
    file_type = models.CharField(max_length=50, db_index=True)
    file_size = models.BigIntegerField()
    
    # Content
    content = models.TextField(blank=True)
    search_vector = SearchVectorField(null=True)
    
    # Metadata
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='indexed_documents')
    department = models.CharField(max_length=100, blank=True, db_index=True)
    
    # Workflow
    workflow_status = models.CharField(max_length=50, blank=True, db_index=True)
    
    # Timestamps
    created_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relevance scoring
    relevance_score = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'document_search_index'
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['owner', 'file_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['workflow_status']),
            models.Index(fields=['department']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.filename} - {self.file_type}"


class SearchQuery(models.Model):
    """
    Track search queries for analytics and optimization
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    query_text = models.TextField()
    filters = models.JSONField(default=dict, blank=True)
    result_count = models.IntegerField(default=0)
    execution_time_ms = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'search_queries'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.query_text[:50]} - {self.result_count} results"
