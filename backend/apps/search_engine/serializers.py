"""
Search Engine Serializers
"""
from rest_framework import serializers


class SearchRequestSerializer(serializers.Serializer):
    """Serializer for search requests"""
    q = serializers.CharField(required=False, allow_blank=True, max_length=500)
    file_type = serializers.ChoiceField(
        choices=['all', 'pdf', 'docx', 'xlsx', 'pptx', 'jpg', 'png'],
        required=False,
        default='all'
    )
    date_range = serializers.ChoiceField(
        choices=['all', 'today', 'week', 'month', 'year'],
        required=False,
        default='all'
    )
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    min_size = serializers.IntegerField(required=False, min_value=0)
    max_size = serializers.IntegerField(required=False, min_value=0)
    uploader = serializers.CharField(required=False, max_length=255)
    workflow_status = serializers.CharField(required=False, max_length=50)
    department = serializers.CharField(required=False, max_length=100)
    limit = serializers.IntegerField(required=False, default=100, min_value=1, max_value=100)
    offset = serializers.IntegerField(required=False, default=0, min_value=0)
