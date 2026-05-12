"""
Admin configuration for compression.
"""

from django.contrib import admin
from .models import CompressionJob


@admin.register(CompressionJob)
class CompressionJobAdmin(admin.ModelAdmin):
    """Admin interface for CompressionJob model."""
    
    list_display = ('id', 'user', 'compression_level', 'status', 'compression_ratio', 'created_at')
    list_filter = ('status', 'compression_level', 'created_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Job Information', {
            'fields': ('id', 'user', 'status', 'compression_level')
        }),
        ('Files', {
            'fields': ('original_file', 'compressed_file')
        }),
        ('Metrics', {
            'fields': ('original_size', 'compressed_size', 'compression_ratio', 'processing_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
