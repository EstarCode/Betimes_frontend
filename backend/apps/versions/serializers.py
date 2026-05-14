"""
Serializers for document version control
"""
from rest_framework import serializers
from .models import Document, DocumentVersion


class DocumentVersionSerializer(serializers.ModelSerializer):
    """Serializer for document versions"""
    modified_by_email = serializers.EmailField(source='modified_by.email', read_only=True)
    
    class Meta:
        model = DocumentVersion
        fields = [
            'id', 'version_number', 'file_size', 'checksum_sha256',
            'storage_path', 'is_rollback', 'rollback_from_version',
            'modified_by', 'modified_by_email', 'change_description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for documents"""
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    current_version_info = DocumentVersionSerializer(source='versions.first', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'filename', 'original_filename', 'file_type', 'current_version',
            'file_size', 'mime_type', 'checksum_sha256', 'storage_path',
            'encrypted', 'owner', 'owner_email', 'department', 'is_deleted',
            'created_at', 'updated_at', 'current_version_info'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'current_version']


class RollbackRequestSerializer(serializers.Serializer):
    """Serializer for rollback request"""
    version_number = serializers.IntegerField(min_value=1)
    change_description = serializers.CharField(required=False, allow_blank=True)
