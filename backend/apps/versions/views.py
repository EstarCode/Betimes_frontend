"""
Views for document version control
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentVersionSerializer, RollbackRequestSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for document management with version control
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return documents for current user or all if admin"""
        user = self.request.user
        if user.role in ['Super_Admin', 'Admin']:
            return Document.objects.filter(is_deleted=False)
        return Document.objects.filter(owner=user, is_deleted=False)
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """
        List all versions of a document
        
        GET /api/v1/documents/{id}/versions/
        """
        document = self.get_object()
        versions = document.versions.all()
        serializer = DocumentVersionSerializer(versions, many=True)
        return Response({
            'document_id': document.id,
            'current_version': document.current_version,
            'total_versions': versions.count(),
            'versions': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def rollback(self, request, pk=None):
        """
        Rollback document to a previous version
        
        POST /api/v1/documents/{id}/rollback/
        Body: {"version_number": 3, "change_description": "Reverted changes"}
        """
        document = self.get_object()
        serializer = RollbackRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        version_number = serializer.validated_data['version_number']
        change_description = serializer.validated_data.get('change_description', '')
        
        # Get the version to rollback to
        try:
            target_version = document.versions.get(version_number=version_number)
        except DocumentVersion.DoesNotExist:
            return Response(
                {'error': f'Version {version_number} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create new version as rollback
        new_version_number = document.current_version + 1
        new_version = DocumentVersion.objects.create(
            document=document,
            version_number=new_version_number,
            file_size=target_version.file_size,
            checksum_sha256=target_version.checksum_sha256,
            storage_path=target_version.storage_path,
            is_rollback=True,
            rollback_from_version=version_number,
            modified_by=request.user,
            change_description=change_description or f'Rolled back to version {version_number}'
        )
        
        # Update document
        document.current_version = new_version_number
        document.file_size = target_version.file_size
        document.checksum_sha256 = target_version.checksum_sha256
        document.storage_path = target_version.storage_path
        document.save()
        
        return Response({
            'message': f'Successfully rolled back to version {version_number}',
            'new_version': new_version_number,
            'version': DocumentVersionSerializer(new_version).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def compare(self, request, pk=None):
        """
        Compare two versions of a document
        
        GET /api/v1/documents/{id}/compare/?v1=1&v2=2
        """
        document = self.get_object()
        v1 = request.query_params.get('v1')
        v2 = request.query_params.get('v2')
        
        if not v1 or not v2:
            return Response(
                {'error': 'Both v1 and v2 parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            version1 = document.versions.get(version_number=int(v1))
            version2 = document.versions.get(version_number=int(v2))
        except DocumentVersion.DoesNotExist:
            return Response(
                {'error': 'One or both versions not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'document_id': document.id,
            'version1': DocumentVersionSerializer(version1).data,
            'version2': DocumentVersionSerializer(version2).data,
            'size_difference': version2.file_size - version1.file_size,
            'checksum_match': version1.checksum_sha256 == version2.checksum_sha256
        })
