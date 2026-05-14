"""
Authentication Tests
Comprehensive test suite following international testing standards
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .mfa_service import MFAService
import pyotp

User = get_user_model()


class UserModelTests(TestCase):
    """Test User model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPassword123!',
            role='Processor'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'Processor')
        self.assertTrue(self.user.check_password('TestPassword123!'))
    
    def test_storage_percentage(self):
        """Test storage percentage calculation"""
        self.user.storage_used = 500000000  # 500MB
        self.user.storage_limit = 1073741824  # 1GB
        self.assertAlmostEqual(self.user.storage_percentage, 46.57, places=1)
    
    def test_has_storage_available(self):
        """Test storage availability check"""
        self.user.storage_used = 500000000
        self.user.storage_limit = 1073741824
        self.assertTrue(self.user.has_storage_available(100000000))  # 100MB
        self.assertFalse(self.user.has_storage_available(600000000))  # 600MB


class AuthenticationAPITests(APITestCase):
    """Test authentication API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPassword123!',
            role='Processor'
        )
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPassword123!',
            'password2': 'NewPassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
    
    def test_user_login(self):
        """Test user login endpoint"""
        data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_profile_access_authenticated(self):
        """Test profile access with authentication"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'test@example.com')
    
    def test_profile_access_unauthenticated(self):
        """Test profile access without authentication"""
        response = self.client.get('/api/v1/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MFAServiceTests(TestCase):
    """Test MFA service"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPassword123!',
            role='Admin'
        )
        self.mfa_service = MFAService()
    
    def test_totp_setup(self):
        """Test TOTP setup"""
        result = self.mfa_service.setup_totp(self.user)
        self.assertTrue(result['success'])
        self.assertIn('secret', result)
        self.assertIn('qr_code', result)
        self.assertIn('backup_codes', result)
        self.assertEqual(len(result['backup_codes']), 10)
    
    def test_totp_verification(self):
        """Test TOTP token verification"""
        # Setup MFA
        result = self.mfa_service.setup_totp(self.user)
        secret = result['secret']
        
        # Generate valid token
        totp = pyotp.TOTP(secret)
        token = totp.now()
        
        # Verify setup
        verified = self.mfa_service.verify_totp_setup(self.user, token)
        self.assertTrue(verified)
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertTrue(self.user.mfa_enabled)
        self.assertEqual(self.user.mfa_secret, secret)
    
    def test_backup_code_verification(self):
        """Test backup code verification"""
        backup_codes = self.mfa_service.generate_backup_codes()
        self.user.mfa_enabled = True
        self.user.backup_codes = backup_codes
        self.user.save()
        
        # Verify valid backup code
        valid_code = backup_codes[0]
        verified = self.mfa_service.verify_backup_code(self.user, valid_code)
        self.assertTrue(verified)
        
        # Refresh user and check code was removed
        self.user.refresh_from_db()
        self.assertNotIn(valid_code, self.user.backup_codes)
        
        # Try to use same code again
        verified_again = self.mfa_service.verify_backup_code(self.user, valid_code)
        self.assertFalse(verified_again)
    
    def test_mfa_required_for_admin(self):
        """Test MFA is required for admin roles"""
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPassword123!',
            role='Super_Admin'
        )
        self.assertTrue(self.mfa_service.check_mfa_required(admin_user))
        
        processor_user = User.objects.create_user(
            username='processor',
            email='processor@example.com',
            password='ProcessorPassword123!',
            role='Processor'
        )
        self.assertFalse(self.mfa_service.check_mfa_required(processor_user))


class PasswordValidationTests(TestCase):
    """Test password validation"""
    
    def test_weak_password_rejected(self):
        """Test weak passwords are rejected"""
        weak_passwords = [
            'short',  # Too short
            'alllowercase123!',  # No uppercase
            'ALLUPPERCASE123!',  # No lowercase
            'NoNumbers!',  # No numbers
            'NoSpecial123',  # No special characters
            'password123!',  # Common password
        ]
        
        for password in weak_passwords:
            with self.assertRaises(Exception):
                User.objects.create_user(
                    username=f'user_{password}',
                    email=f'{password}@example.com',
                    password=password
                )
    
    def test_strong_password_accepted(self):
        """Test strong passwords are accepted"""
        user = User.objects.create_user(
            username='stronguser',
            email='strong@example.com',
            password='StrongPassword123!'
        )
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('StrongPassword123!'))


class RBACTests(TestCase):
    """Test Role-Based Access Control"""
    
    def setUp(self):
        self.super_admin = User.objects.create_user(
            username='superadmin',
            email='superadmin@example.com',
            password='SuperAdmin123!',
            role='Super_Admin'
        )
        self.viewer = User.objects.create_user(
            username='viewer',
            email='viewer@example.com',
            password='Viewer123!',
            role='Viewer'
        )
    
    def test_super_admin_permissions(self):
        """Test Super Admin has all permissions"""
        self.assertTrue(self.super_admin.has_permission('users.create'))
        self.assertTrue(self.super_admin.has_permission('documents.delete'))
        self.assertTrue(self.super_admin.has_permission('system.configure'))
    
    def test_viewer_permissions(self):
        """Test Viewer has limited permissions"""
        self.assertTrue(self.viewer.has_permission('documents.read'))
        self.assertFalse(self.viewer.has_permission('documents.create'))
        self.assertFalse(self.viewer.has_permission('documents.delete'))
        self.assertFalse(self.viewer.has_permission('users.create'))
