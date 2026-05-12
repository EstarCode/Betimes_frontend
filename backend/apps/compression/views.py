"""
Views for PDF compression.
"""

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import CompressionJob
from .serializers import CompressionJobSerializer, CompressionUploadSerializer
from .tasks import compress_pdf_task
import logging

logger = logging.getLogger(__name__)


class CompressionUploadView(views.APIView):
    """API endpoint for uploading and compressing PDFs."""
    
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """Handle PDF upload and start compression task."""
        serializer = CompressionUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check user storage
        file = serializer.validated_data['file']
        if not request.user.has_storage_available(file.size):
            return Response({
                'success': False,
                'error': {
                    'message': 'Insufficient storage space',
                    'details': {'storage': 'You have exceeded your storage limit'}
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create compression job
        job = CompressionJob.objects.create(
            user=request.user,
            original_file=file,
            compression_level=serializer.validated_data['compression_level'],
            original_size=file.size
        )
        
        # Start async compression task
        compress_pdf_task.delay(str(job.id))
        
        logger.info(f"Compression job {job.id} created for user {request.user.email}")
        
        return Response({
            'success': True,
            'message': 'File uploaded successfully. Compression started.',
            'data': CompressionJobSerializer(job, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)



class CompressionJobListView(generics.ListAPIView):
    """API endpoint for listing user's compression jobs."""
    
    permission_classes = (IsAuthenticated,)
    serializer_class = CompressionJobSerializer
    
    def get_queryset(self):
        """Get compression jobs for current user."""
        return CompressionJob.objects.filter(user=self.request.user)


class CompressionJobDetailView(generics.RetrieveAPIView):
    """API endpoint for retrieving compression job details."""
    
    permission_classes = (IsAuthenticated,)
    serializer_class = CompressionJobSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        """Get compression jobs for current user."""
        return CompressionJob.objects.filter(user=self.request.user)


class CompressionJobDeleteView(generics.DestroyAPIView):
    """API endpoint for deleting compression jobs."""
    
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    
    def get_queryset(self):
        """Get compression jobs for current user."""
        return CompressionJob.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Delete compression job and associated files."""
        instance = self.get_object()
        
        # Delete files
        if instance.original_file:
            instance.original_file.delete(save=False)
        if instance.compressed_file:
            instance.compressed_file.delete(save=False)
        
        instance.delete()
        
        return Response({
            'success': True,
            'message': 'Compression job deleted successfully'
        }, status=status.HTTP_200_OK)
