"""
Tests for authentication functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test cases for User model."""
    
    def test_create_user(self):
        """Test creating a new user."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_premium)
    
    def test_storage_percentage(self):
        """Test storage percentage calculation."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        user.storage_used = 536870912  # 512MB
        user.storage_limit = 1073741824  # 1GB
        self.assertEqual(user.storage_percentage, 50.0)
    
    def test_has_storage_available(self):
        """Test storage availability check."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        user.storage_used = 0
        user.storage_limit = 1073741824  # 1GB
        
        # Should have space for 100MB file
        self.assertTrue(user.has_storage_available(104857600))
        
        # Should not have space for 2GB file
        self.assertFalse(user.has_storage_available(2147483648))


class AuthenticationAPITestCase(TestCase):
    """Test cases for authentication API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_registration(self):
        """Test user registration endpoint."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
    
    def test_user_login(self):
        """Test user login endpoint."""
        # Create user
        User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        # Login
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])
    
    def test_user_profile(self):
        """Test user profile endpoint."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'test@example.com')
