"""
Search Engine Views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import SearchService
from .serializers import SearchRequestSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_documents(request):
    """
    Search documents with full-text search and filters
    
    GET /api/v1/search/?q=query&file_type=pdf&date_range=month&limit=50&offset=0
    
    Query Parameters:
    - q: Search query text
    - file_type: Filter by file type (pdf, docx, xlsx, pptx, jpg, png, all)
    - date_range: Filter by date (today, week, month, year, all)
    - start_date: Custom start date (ISO format)
    - end_date: Custom end date (ISO format)
    - min_size: Minimum file size in bytes
    - max_size: Maximum file size in bytes
    - uploader: Filter by uploader email
    - workflow_status: Filter by workflow status
    - department: Filter by department
    - limit: Results per page (default 100, max 100)
    - offset: Pagination offset (default 0)
    """
    serializer = SearchRequestSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    
    query_text = serializer.validated_data.get('q', '')
    filters = {
        'file_type': serializer.validated_data.get('file_type'),
        'date_range': serializer.validated_data.get('date_range'),
        'start_date': serializer.validated_data.get('start_date'),
        'end_date': serializer.validated_data.get('end_date'),
        'min_size': serializer.validated_data.get('min_size'),
        'max_size': serializer.validated_data.get('max_size'),
        'uploader': serializer.validated_data.get('uploader'),
        'workflow_status': serializer.validated_data.get('workflow_status'),
        'department': serializer.validated_data.get('department'),
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    limit = serializer.validated_data.get('limit', 100)
    offset = serializer.validated_data.get('offset', 0)
    
    search_service = SearchService()
    result = search_service.search(
        query_text=query_text,
        user=request.user,
        filters=filters,
        limit=limit,
        offset=offset
    )
    
    if result['success']:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': result.get('error', 'Search failed')},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_suggestions(request):
    """
    Get search suggestions
    
    GET /api/v1/search/suggestions/?q=partial
    """
    partial_query = request.query_params.get('q', '')
    
    if len(partial_query) < 2:
        return Response({'suggestions': []}, status=status.HTTP_200_OK)
    
    search_service = SearchService()
    suggestions = search_service.get_search_suggestions(partial_query)
    
    return Response({'suggestions': suggestions}, status=status.HTTP_200_OK)
