"""
Serializers for file conversion.
"""

from rest_framework import serializers
from .models import ConversionJob


class ConversionJobSerializer(serializers.ModelSerializer):
    """Serializer for ConversionJob model."""
    
    input_file_url = serializers.SerializerMethodField()
    output_file_url = serializers.SerializerMethodField()
    conversion_type_display = serializers.CharField(source='get_conversion_type_display', read_only=True)
    
    class Meta:
        model = ConversionJob
        fields = (
            'id', 'conversion_type', 'conversion_type_display', 'status',
            'input_size', 'output_size', 'processing_time', 'error_message',
            'created_at', 'updated_at', 'completed_at',
            'input_file_url', 'output_file_url'
        )
        read_only_fields = (
            'id', 'status', 'input_size', 'output_size', 'processing_time',
            'error_message', 'created_at', 'updated_at', 'completed_at'
        )
    
    def get_input_file_url(self, obj):
        if obj.input_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.input_file.url)
        return None
    
    def get_output_file_url(self, obj):
        if obj.output_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.output_file.url)
        return None


class ConversionUploadSerializer(serializers.Serializer):
    """Serializer for file upload and conversion request."""
    
    file = serializers.FileField()
    conversion_type = serializers.ChoiceField(choices=[
        'word_to_pdf', 'image_to_pdf', 'pdf_to_word',
        'pdf_to_image', 'excel_to_pdf', 'ppt_to_pdf', 'pdf_to_text'
    ])
