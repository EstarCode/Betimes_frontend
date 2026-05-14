"""
Search Engine Service
Implements full-text search with PostgreSQL
Requirement 17: 2-second search across 1M documents
"""
import logging
import time
from typing import Dict, List, Optional
from django.db.models import Q, F
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from datetime import datetime, timedelta

from .models import DocumentIndex, SearchQuery as SearchQueryModel

logger = logging.getLogger(__name__)


class SearchService:
    """
    Enterprise search service with full-text search
    Performance target: < 2 seconds for 1M documents
    """
    
    def search(self, query_text: str, user, filters: Optional[Dict] = None,
               limit: int = 100, offset: int = 0) -> Dict:
        """
        Perform full-text search with filters
        
        Args:
            query_text: Search query
            user: User performing search
            filters: Optional filters (file_type, date_range, size_range, uploader, workflow_status)
            limit: Maximum results to return
            offset: Pagination offset
        
        Returns:
            dict: Search results with metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Search query: '{query_text}' by user {user.email}")
            
            # Build base queryset
            queryset = DocumentIndex.objects.all()
            
            # Apply access control - users can only search their own documents
            # unless they're admin
            if user.role not in ['Super_Admin', 'Admin']:
                queryset = queryset.filter(owner=user)
            
            # Apply filters
            if filters:
                queryset = self._apply_filters(queryset, filters)
            
            # Perform full-text search
            if query_text.strip():
                search_query = SearchQuery(query_text)
                search_vector = SearchVector('filename', weight='A') + \
                               SearchVector('content', weight='B') + \
                               SearchVector('title', weight='A') + \
                               SearchVector('description', weight='C')
                
                queryset = queryset.annotate(
                    rank=SearchRank(search_vector, search_query)
                ).filter(rank__gte=0.01).order_by('-rank')
            else:
                # No search query, just apply filters and sort by date
                queryset = queryset.order_by('-created_at')
            
            # Get total count before pagination
            total_count = queryset.count()
            
            # Apply pagination
            results = queryset[offset:offset + limit]
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    'id': str(doc.document_id),
                    'filename': doc.filename,
                    'file_type': doc.file_type,
                    'file_size': doc.file_size,
                    'title': doc.title,
                    'snippet': self._generate_snippet(doc.content, query_text),
                    'uploader': {
                        'id': doc.owner.id,
                        'email': doc.owner.email,
                        'name': f"{doc.owner.first_name} {doc.owner.last_name}".strip()
                    },
                    'department': doc.department,
                    'workflow_status': doc.workflow_status,
                    'created_at': doc.created_at.isoformat(),
                    'relevance_score': getattr(doc, 'rank', 0.0)
                })
            
            execution_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Log search query
            SearchQueryModel.objects.create(
                user=user,
                query_text=query_text,
                filters=filters or {},
                result_count=total_count,
                execution_time_ms=execution_time
            )
            
            logger.info(f"Search completed in {execution_time:.2f}ms: {total_count} results")
            
            return {
                'success': True,
                'query': query_text,
                'total_count': total_count,
                'results': formatted_results,
                'execution_time_ms': execution_time,
                'page': {
                    'limit': limit,
                    'offset': offset,
                    'has_more': total_count > (offset + limit)
                }
            }
            
        except Exception as e:
            logger.exception(f"Search failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'results': []
            }
    
    def _apply_filters(self, queryset, filters: Dict):
        """Apply search filters to queryset"""
        
        # File type filter
        if filters.get('file_type') and filters['file_type'] != 'all':
            queryset = queryset.filter(file_type=filters['file_type'])
        
        # Date range filter
        if filters.get('date_range'):
            date_filter = self._get_date_filter(filters['date_range'])
            if date_filter:
                queryset = queryset.filter(created_at__gte=date_filter)
        
        # Custom date range
        if filters.get('start_date'):
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        if filters.get('end_date'):
            queryset = queryset.filter(created_at__lte=filters['end_date'])
        
        # File size range
        if filters.get('min_size'):
            queryset = queryset.filter(file_size__gte=filters['min_size'])
        if filters.get('max_size'):
            queryset = queryset.filter(file_size__lte=filters['max_size'])
        
        # Uploader filter
        if filters.get('uploader'):
            queryset = queryset.filter(owner__email__icontains=filters['uploader'])
        
        # Workflow status filter
        if filters.get('workflow_status'):
            queryset = queryset.filter(workflow_status=filters['workflow_status'])
        
        # Department filter
        if filters.get('department'):
            queryset = queryset.filter(department=filters['department'])
        
        return queryset
    
    def _get_date_filter(self, date_range: str) -> Optional[datetime]:
        """Convert date range string to datetime filter"""
        now = datetime.now()
        
        if date_range == 'today':
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range == 'week':
            return now - timedelta(days=7)
        elif date_range == 'month':
            return now - timedelta(days=30)
        elif date_range == 'year':
            return now - timedelta(days=365)
        
        return None
    
    def _generate_snippet(self, content: str, query: str, max_length: int = 200) -> str:
        """Generate search result snippet with highlighted terms"""
        if not content:
            return "No preview available"
        
        # Simple snippet generation - find query in content
        content_lower = content.lower()
        query_lower = query.lower()
        
        if query_lower in content_lower:
            # Find position of query
            pos = content_lower.find(query_lower)
            
            # Get context around query
            start = max(0, pos - 50)
            end = min(len(content), pos + max_length)
            
            snippet = content[start:end]
            
            # Add ellipsis
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
            
            return snippet.strip()
        
        # No match, return beginning of content
        return content[:max_length] + ("..." if len(content) > max_length else "")
    
    def index_document(self, document_id: str, filename: str, file_type: str,
                      file_size: int, content: str, owner, **kwargs) -> bool:
        """
        Index a document for search
        
        Args:
            document_id: Document UUID
            filename: Document filename
            file_type: File type (pdf, docx, etc.)
            file_size: File size in bytes
            content: Extracted text content
            owner: User who owns the document
            **kwargs: Additional metadata (title, description, tags, department, workflow_status)
        
        Returns:
            bool: Success status
        """
        try:
            # Create or update index entry
            doc_index, created = DocumentIndex.objects.update_or_create(
                document_id=document_id,
                defaults={
                    'filename': filename,
                    'file_type': file_type,
                    'file_size': file_size,
                    'content': content[:100000],  # Limit content size
                    'title': kwargs.get('title', ''),
                    'description': kwargs.get('description', ''),
                    'tags': kwargs.get('tags', []),
                    'owner': owner,
                    'department': kwargs.get('department', ''),
                    'workflow_status': kwargs.get('workflow_status', ''),
                    'created_at': kwargs.get('created_at', datetime.now())
                }
            )
            
            # Update search vector
            doc_index.search_vector = SearchVector('filename', weight='A') + \
                                     SearchVector('content', weight='B') + \
                                     SearchVector('title', weight='A') + \
                                     SearchVector('description', weight='C')
            doc_index.save()
            
            action = "indexed" if created else "updated"
            logger.info(f"Document {action}: {filename} ({document_id})")
            
            return True
            
        except Exception as e:
            logger.exception(f"Failed to index document: {str(e)}")
            return False
    
    def remove_from_index(self, document_id: str) -> bool:
        """Remove document from search index"""
        try:
            DocumentIndex.objects.filter(document_id=document_id).delete()
            logger.info(f"Document removed from index: {document_id}")
            return True
        except Exception as e:
            logger.exception(f"Failed to remove from index: {str(e)}")
            return False
    
    def get_search_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """Get search suggestions based on partial query"""
        try:
            # Get recent successful searches
            suggestions = SearchQueryModel.objects.filter(
                query_text__istartswith=partial_query,
                result_count__gt=0
            ).values_list('query_text', flat=True).distinct()[:limit]
            
            return list(suggestions)
            
        except Exception as e:
            logger.exception(f"Failed to get suggestions: {str(e)}")
            return []
