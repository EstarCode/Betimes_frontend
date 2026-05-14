"""
PDF Tools Serializers
"""
from rest_framework import serializers


class PDFSplitByRangeSerializer(serializers.Serializer):
    """Serializer for PDF split by page range"""
    page_ranges = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of page ranges with start, end, and output_name"
    )
    
    def validate_page_ranges(self, value):
        for range_spec in value:
            if 'start' not in range_spec or 'end' not in range_spec:
                raise serializers.ValidationError("Each range must have 'start' and 'end'")
            if range_spec['start'] > range_spec['end']:
                raise serializers.ValidationError("Start page must be <= end page")
        return value


class PDFMergeSerializer(serializers.Serializer):
    """Serializer for PDF merge"""
    files = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of files with path and optional title"
    )
    create_toc = serializers.BooleanField(default=True)
    
    def validate_files(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Cannot merge more than 100 files")
        if len(value) < 2:
            raise serializers.ValidationError("At least 2 files required for merge")
        
        for file_spec in value:
            if 'path' not in file_spec:
                raise serializers.ValidationError("Each file must have 'path'")
        
        return value


class PDFExtractPagesSerializer(serializers.Serializer):
    """Serializer for page extraction"""
    page_numbers = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        help_text="List of page numbers to extract (1-indexed)"
    )


class PDFRotateSerializer(serializers.Serializer):
    """Serializer for page rotation"""
    rotation = serializers.ChoiceField(choices=[90, 180, 270])
    pages = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_null=True,
        help_text="Page numbers to rotate (empty = all pages)"
    )
