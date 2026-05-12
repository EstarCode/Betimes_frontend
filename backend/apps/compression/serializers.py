"""
Serializers for PDF compression.
"""

from rest_framework import serializers
from .models import CompressionJob


class CompressionJobSerializer(serializers.ModelSerializer):
    """Serializer for CompressionJob model."""
    
    size_reduction = serializers.ReadOnlyField()
    original_file_url = serializers.SerializerMethodField()
    compressed_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CompressionJob
        fields = (
            'id', 'compression_level', 'status', 'original_size',
            'compressed_size', 'compression_ratio', 'size_reduction',
            'processing_time', 'error_message', 'created_at',
            'updated_at', 'completed_at', 'original_file_url',
            'compressed_file_url'
        )
        read_only_fields = (
            'id', 'status', 'original_size', 'compressed_size',
            'compression_ratio', 'processing_time', 'error_message',
            'created_at', 'updated_at', 'completed_at'
        )
    
    def get_original_file_url(self, obj):
        """Get URL for original file."""
        if obj.original_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.original_file.url)
        return None
    
    def get_compressed_file_url(self, obj):
        """Get URL for compressed file."""
        if obj.compressed_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.compressed_file.url)
        return None


class CompressionUploadSerializer(serializers.Serializer):
    """Serializer for PDF upload and compression request."""
    
    file = serializers.FileField()
    compression_level = serializers.ChoiceField(
        choices=['low', 'medium', 'high'],
        default='medium'
    )
    
    def validate_file(self, value):
        """Validate uploaded file."""
        # Check file extension
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        
        # Check file size (500MB max)
        max_size = 524288000  # 500MB in bytes
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size exceeds maximum allowed size of 500MB."
            )
        
        return value
