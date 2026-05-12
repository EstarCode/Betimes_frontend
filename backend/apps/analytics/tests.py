"""
Tests for analytics functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.compression.models import CompressionJob

User = get_user_model()


class AnalyticsAPITestCase(TestCase):
    """Test cases for analytics API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_user_analytics(self):
        """Test user analytics endpoint."""
        # Create some test data
        CompressionJob.objects.create(
            user=self.user,
            original_file=SimpleUploadedFile("sample.pdf", b"%PDF-1.4\n"),
            compression_level='medium',
            original_size=1000000,
            compressed_size=500000,
            compression_ratio=50.0,
            status='completed'
        )
        
        response = self.client.get('/api/analytics/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('compression', response.data['data'])
        self.assertIn('storage', response.data['data'])
