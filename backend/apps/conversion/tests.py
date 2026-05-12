"""
Tests for file conversion functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import ConversionJob
from .services import FileConversionService

User = get_user_model()


class ConversionServiceTestCase(TestCase):
    """Test cases for file conversion service."""
    
    def setUp(self):
        self.service = FileConversionService()
    
    def test_service_initialization(self):
        """Test service initializes correctly."""
        self.assertIsNotNone(self.service)


class ConversionAPITestCase(TestCase):
    """Test cases for conversion API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_conversion_job_list(self):
        """Test listing conversion jobs."""
        response = self.client.get('/api/convert/jobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_conversion_job_model(self):
        """Test conversion job model creation."""
        job = ConversionJob.objects.create(
            user=self.user,
            input_file=SimpleUploadedFile("sample.docx", b"fake-docx-content"),
            conversion_type='word_to_pdf',
            input_size=500000
        )
        self.assertEqual(job.status, 'pending')
        self.assertEqual(job.conversion_type, 'word_to_pdf')
        self.assertEqual(job.user, self.user)
