"""
Admin configuration for conversion.
"""

from django.contrib import admin
from .models import ConversionJob


@admin.register(ConversionJob)
class ConversionJobAdmin(admin.ModelAdmin):
    """Admin interface for ConversionJob model."""
    
    list_display = ('id', 'user', 'conversion_type', 'status', 'created_at')
    list_filter = ('status', 'conversion_type', 'created_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_at')
    ordering = ('-created_at',)
