"""
Tests for PDF compression functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import CompressionJob
from .services import PDFCompressionService
import os
import tempfile

User = get_user_model()


class CompressionServiceTestCase(TestCase):
    """Test cases for PDF compression service."""
    
    def setUp(self):
        self.service = PDFCompressionService()
    
    def test_validate_pdf_valid(self):
        """Test PDF validation with valid PDF header."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(b'%PDF-1.4\n%Test PDF')
            tmp_path = tmp_file.name
        try:
            result = self.service.validate_pdf(tmp_path)
            self.assertTrue(result)
        finally:
            os.remove(tmp_path)
    
    def test_validate_pdf_invalid(self):
        """Test PDF validation with invalid file."""
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as tmp_file:
            tmp_file.write('Not a PDF')
            tmp_path = tmp_file.name
        try:
            result = self.service.validate_pdf(tmp_path)
            self.assertFalse(result)
        finally:
            os.remove(tmp_path)


class CompressionAPITestCase(TestCase):
    """Test cases for compression API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_compression_job_list(self):
        """Test listing compression jobs."""
        response = self.client.get('/api/compress/jobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_compression_job_create_no_file(self):
        """Test creating compression job without file."""
        response = self.client.post('/api/compress/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_compression_job_model(self):
        """Test compression job model creation."""
        job = CompressionJob.objects.create(
            user=self.user,
            original_file=SimpleUploadedFile("sample.pdf", b"%PDF-1.4\n"),
            compression_level='medium',
            original_size=1000000
        )
        self.assertEqual(job.status, 'pending')
        self.assertEqual(job.compression_level, 'medium')
        self.assertEqual(job.user, self.user)
    
    def test_compression_ratio_calculation(self):
        """Test compression ratio calculation."""
        job = CompressionJob.objects.create(
            user=self.user,
            original_file=SimpleUploadedFile("sample.pdf", b"%PDF-1.4\n"),
            original_size=1000000,
            compressed_size=500000
        )
        ratio = job.calculate_compression_ratio()
        self.assertEqual(ratio, 50.0)
