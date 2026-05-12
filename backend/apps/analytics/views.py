"""
Views for analytics.
"""

from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.compression.models import CompressionJob
from apps.conversion.models import ConversionJob
from django.db.models import Count, Sum, Avg


class UserAnalyticsView(views.APIView):
    """API endpoint for user analytics."""
    
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        
        # Compression stats
        compression_stats = CompressionJob.objects.filter(user=user).aggregate(
            total_jobs=Count('id'),
            total_original_size=Sum('original_size'),
            total_compressed_size=Sum('compressed_size'),
            avg_compression_ratio=Avg('compression_ratio')
        )
        
        # Conversion stats
        conversion_stats = ConversionJob.objects.filter(user=user).aggregate(
            total_jobs=Count('id')
        )
        
        return Response({
            'success': True,
            'data': {
                'compression': compression_stats,
                'conversion': conversion_stats,
                'storage': {
                    'used': user.storage_used,
                    'limit': user.storage_limit,
                    'percentage': user.storage_percentage
                }
            }
        })
