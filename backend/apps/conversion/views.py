"""
Views for file conversion.
"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ConversionJob
from .serializers import ConversionJobSerializer, ConversionUploadSerializer
from .tasks import convert_file_task
import logging

logger = logging.getLogger(__name__)


class ConversionUploadView(views.APIView):
    """API endpoint for file conversion."""
    
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        serializer = ConversionUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data['file']
        
        # Check user storage
        if not request.user.has_storage_available(file.size):
            return Response({
                'success': False,
                'error': {
                    'message': 'Insufficient storage space',
                    'details': {'storage': 'You have exceeded your storage limit'}
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        job = ConversionJob.objects.create(
            user=request.user,
            input_file=file,
            conversion_type=serializer.validated_data['conversion_type'],
            input_size=file.size
        )
        
        # Start async conversion task
        convert_file_task.delay(str(job.id))
        
        logger.info(f"Conversion job {job.id} created for user {request.user.email}")
        
        return Response({
            'success': True,
            'message': 'File uploaded successfully. Conversion started.',
            'data': ConversionJobSerializer(job, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)


class ConversionJobListView(generics.ListAPIView):
    """API endpoint for listing conversion jobs."""
    
    permission_classes = (IsAuthenticated,)
    serializer_class = ConversionJobSerializer
    
    def get_queryset(self):
        return ConversionJob.objects.filter(user=self.request.user)


class ConversionJobDetailView(generics.RetrieveAPIView):
    """API endpoint for conversion job details."""
    
    permission_classes = (IsAuthenticated,)
    serializer_class = ConversionJobSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return ConversionJob.objects.filter(user=self.request.user)
