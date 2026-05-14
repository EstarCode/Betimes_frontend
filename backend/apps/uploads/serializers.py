"""
Serializers for chunked upload system
"""
from rest_framework import serializers
from .models import UploadSession, UploadChunk


class UploadSessionSerializer(serializers.ModelSerializer):
    """Serializer for upload sessions"""
    progress_percentage = serializers.ReadOnlyField()
    is_complete = serializers.ReadOnlyField()
    
    class Meta:
        model = UploadSession
        fields = [
            'id', 'filename', 'file_size', 'chunk_size', 'total_chunks',
            'uploaded_chunks', 'checksum_sha256', 'status', 'progress_percentage',
            'is_complete', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'uploaded_chunks', 'status', 'created_at', 'updated_at', 'completed_at']


class UploadChunkSerializer(serializers.ModelSerializer):
    """Serializer for upload chunks"""
    
    class Meta:
        model = UploadChunk
        fields = ['id', 'chunk_number', 'chunk_size', 'checksum_sha256', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class InitiateUploadSerializer(serializers.Serializer):
    """Serializer for initiating chunked upload"""
    filename = serializers.CharField(max_length=500)
    file_size = serializers.IntegerField(min_value=1)
    chunk_size = serializers.IntegerField(default=10485760, min_value=1048576)  # Min 1MB
    checksum_sha256 = serializers.CharField(max_length=64, required=False)


class UploadChunkRequestSerializer(serializers.Serializer):
    """Serializer for chunk upload request"""
    chunk_number = serializers.IntegerField(min_value=0)
    checksum_sha256 = serializers.CharField(max_length=64)
    file = serializers.FileField()


class CompleteUploadSerializer(serializers.Serializer):
    """Serializer for completing upload"""
    checksum_sha256 = serializers.CharField(max_length=64)
