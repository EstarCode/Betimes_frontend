"""
API views for chunked upload system
Supports resumable uploads up to 10GB with parallel chunk processing
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import UploadSession, UploadChunk
from .serializers import (
    UploadSessionSerializer,
    InitiateUploadSerializer,
    UploadChunkRequestSerializer,
    CompleteUploadSerializer
)
from .services import ChunkedUploadService


class ChunkedUploadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing chunked file uploads
    
    Endpoints:
    - POST /api/v1/uploads/initiate/ - Initialize upload session
    - POST /api/v1/uploads/{id}/chunk/ - Upload a chunk
    - POST /api/v1/uploads/{id}/complete/ - Complete upload
    - GET /api/v1/uploads/{id}/progress/ - Get upload progress
    - DELETE /api/v1/uploads/{id}/cancel/ - Cancel upload
    - GET /api/v1/uploads/ - List user's upload sessions
    """
    serializer_class = UploadSessionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        """Return upload sessions for current user"""
        return UploadSession.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """
        Initialize a new chunked upload session
        
        Request body:
        {
            "filename": "large_file.pdf",
            "file_size": 10737418240,  # 10GB in bytes
            "chunk_size": 10485760,     # 10MB (optional)
            "checksum_sha256": "abc123..." # Optional
        }
        
        Response:
        {
            "id": "uuid",
            "filename": "large_file.pdf",
            "file_size": 10737418240,
            "chunk_size": 10485760,
            "total_chunks": 1024,
            "uploaded_chunks": 0,
            "status": "in_progress",
            "progress_percentage": 0.0,
            "created_at": "2024-01-01T00:00:00Z"
        }
        """
        serializer = InitiateUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            upload_session = ChunkedUploadService.initiate_upload(
                user=request.user,
                filename=serializer.validated_data['filename'],
                file_size=serializer.validated_data['file_size'],
                chunk_size=serializer.validated_data.get('chunk_size'),
                checksum=serializer.validated_data.get('checksum_sha256')
            )
            
            response_serializer = UploadSessionSerializer(upload_session)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def chunk(self, request, pk=None):
        """
        Upload a single chunk
        
        Request (multipart/form-data):
        - chunk_number: 0
        - checksum_sha256: "abc123..."
        - file: <binary chunk data>
        
        Response:
        {
            "chunk_number": 0,
            "uploaded_chunks": 1,
            "total_chunks": 1024,
            "progress_percentage": 0.1,
            "status": "in_progress"
        }
        """
        upload_session = get_object_or_404(UploadSession, pk=pk, user=request.user)
        
        serializer = UploadChunkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            chunk = ChunkedUploadService.upload_chunk(
                upload_session=upload_session,
                chunk_number=serializer.validated_data['chunk_number'],
                chunk_file=serializer.validated_data['file'],
                checksum=serializer.validated_data['checksum_sha256']
            )
            
            return Response({
                'chunk_number': chunk.chunk_number,
                'uploaded_chunks': upload_session.uploaded_chunks,
                'total_chunks': upload_session.total_chunks,
                'progress_percentage': upload_session.progress_percentage,
                'status': upload_session.status
            }, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Complete the upload by merging all chunks
        
        Request body:
        {
            "checksum_sha256": "abc123..."  # Optional final checksum
        }
        
        Response:
        {
            "status": "completed",
            "file_path": "uploads/user_id/filename",
            "checksum_sha256": "abc123...",
            "completed_at": "2024-01-01T00:00:00Z"
        }
        """
        upload_session = get_object_or_404(UploadSession, pk=pk, user=request.user)
        
        serializer = CompleteUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            file_path = ChunkedUploadService.complete_upload(
                upload_session=upload_session,
                final_checksum=serializer.validated_data.get('checksum_sha256')
            )
            
            return Response({
                'status': upload_session.status,
                'file_path': file_path,
                'checksum_sha256': upload_session.checksum_sha256,
                'completed_at': upload_session.completed_at
            }, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """
        Get upload progress
        
        Response:
        {
            "session_id": "uuid",
            "filename": "large_file.pdf",
            "file_size": 10737418240,
            "total_chunks": 1024,
            "uploaded_chunks": 512,
            "progress_percentage": 50.0,
            "status": "in_progress",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:30:00Z"
        }
        """
        upload_session = get_object_or_404(UploadSession, pk=pk, user=request.user)
        progress_data = ChunkedUploadService.get_upload_progress(upload_session)
        return Response(progress_data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def cancel(self, request, pk=None):
        """
        Cancel an upload session
        
        Response:
        {
            "message": "Upload cancelled successfully"
        }
        """
        upload_session = get_object_or_404(UploadSession, pk=pk, user=request.user)
        
        ChunkedUploadService.cancel_upload(upload_session)
        
        return Response(
            {'message': 'Upload cancelled successfully'},
            status=status.HTTP_200_OK
        )
