"""
PDF Tools Views
Implements PDF split, merge, and manipulation endpoints
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid

from .services import PDFToolsService
from .serializers import (
    PDFSplitByRangeSerializer,
    PDFMergeSerializer,
    PDFExtractPagesSerializer,
    PDFRotateSerializer
)


class PDFToolsViewSet(viewsets.ViewSet):
    """
    ViewSet for PDF manipulation operations
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pdf_service = PDFToolsService()
    
    @action(detail=False, methods=['post'], url_path='split-by-range')
    def split_by_range(self, request):
        """
        Split PDF by page ranges
        
        POST /api/v1/tools/pdf/split-by-range/
        Body: {
            "file_path": "/path/to/file.pdf",
            "page_ranges": [
                {"start": 1, "end": 5, "output_name": "part1.pdf"},
                {"start": 6, "end": 10, "output_name": "part2.pdf"}
            ]
        }
        """
        serializer = PDFSplitByRangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_path = request.data.get('file_path')
        if not file_path or not os.path.exists(file_path):
            return Response(
                {'error': 'Invalid file path'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create output directory
            output_dir = os.path.join(
                settings.MEDIA_ROOT,
                'pdf_splits',
                str(request.user.id),
                str(uuid.uuid4())
            )
            
            result = self.pdf_service.split_pdf_by_range(
                input_path=file_path,
                output_dir=output_dir,
                page_ranges=serializer.validated_data['page_ranges']
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='split-by-bookmarks')
    def split_by_bookmarks(self, request):
        """
        Split PDF by bookmark boundaries
        
        POST /api/v1/tools/pdf/split-by-bookmarks/
        Body: {
            "file_path": "/path/to/file.pdf"
        }
        """
        file_path = request.data.get('file_path')
        if not file_path or not os.path.exists(file_path):
            return Response(
                {'error': 'Invalid file path'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            output_dir = os.path.join(
                settings.MEDIA_ROOT,
                'pdf_splits',
                str(request.user.id),
                str(uuid.uuid4())
            )
            
            result = self.pdf_service.split_pdf_by_bookmarks(
                input_path=file_path,
                output_dir=output_dir
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='merge')
    def merge(self, request):
        """
        Merge multiple PDF files
        
        POST /api/v1/tools/pdf/merge/
        Body: {
            "files": [
                {"path": "/path/to/file1.pdf", "title": "Chapter 1"},
                {"path": "/path/to/file2.pdf", "title": "Chapter 2"}
            ],
            "create_toc": true
        }
        """
        serializer = PDFMergeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            output_path = os.path.join(
                settings.MEDIA_ROOT,
                'pdf_merges',
                str(request.user.id),
                f"{uuid.uuid4()}.pdf"
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            result = self.pdf_service.merge_pdfs(
                input_files=serializer.validated_data['files'],
                output_path=output_path,
                create_toc=serializer.validated_data['create_toc']
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='extract-pages')
    def extract_pages(self, request):
        """
        Extract specific pages from PDF
        
        POST /api/v1/tools/pdf/extract-pages/
        Body: {
            "file_path": "/path/to/file.pdf",
            "page_numbers": [1, 3, 5, 7]
        }
        """
        serializer = PDFExtractPagesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_path = request.data.get('file_path')
        if not file_path or not os.path.exists(file_path):
            return Response(
                {'error': 'Invalid file path'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            output_path = os.path.join(
                settings.MEDIA_ROOT,
                'pdf_extracts',
                str(request.user.id),
                f"{uuid.uuid4()}.pdf"
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            result = self.pdf_service.extract_pages(
                input_path=file_path,
                output_path=output_path,
                page_numbers=serializer.validated_data['page_numbers']
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='rotate')
    def rotate(self, request):
        """
        Rotate PDF pages
        
        POST /api/v1/tools/pdf/rotate/
        Body: {
            "file_path": "/path/to/file.pdf",
            "rotation": 90,
            "pages": [1, 2, 3]  // optional, empty = all pages
        }
        """
        serializer = PDFRotateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_path = request.data.get('file_path')
        if not file_path or not os.path.exists(file_path):
            return Response(
                {'error': 'Invalid file path'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            output_path = os.path.join(
                settings.MEDIA_ROOT,
                'pdf_rotated',
                str(request.user.id),
                f"{uuid.uuid4()}.pdf"
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            result = self.pdf_service.rotate_pages(
                input_path=file_path,
                output_path=output_path,
                rotation=serializer.validated_data['rotation'],
                pages=serializer.validated_data.get('pages')
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='info')
    def get_info(self, request):
        """
        Get PDF information and metadata
        
        POST /api/v1/tools/pdf/info/
        Body: {
            "file_path": "/path/to/file.pdf"
        }
        """
        file_path = request.data.get('file_path')
        if not file_path or not os.path.exists(file_path):
            return Response(
                {'error': 'Invalid file path'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = self.pdf_service.get_pdf_info(file_path)
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
