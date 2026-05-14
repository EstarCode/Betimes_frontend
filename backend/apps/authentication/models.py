"""
User model for authentication.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser with enterprise features.
    Supports MFA, RBAC, session management, and audit logging.
    """
    ROLE_CHOICES = [
        ('Super_Admin', 'Super Admin'),
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Reviewer', 'Reviewer'),
        ('Processor', 'Processor'),
        ('Viewer', 'Viewer'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Viewer')
    department = models.CharField(max_length=100, blank=True)
    
    # Storage management
    is_premium = models.BooleanField(default=False)
    storage_used = models.BigIntegerField(default=0, help_text="Storage used in bytes")
    storage_limit = models.BigIntegerField(default=1073741824, help_text="Storage limit in bytes (default 1GB)")
    
    # MFA fields
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True)
    backup_codes = models.JSONField(default=list, blank=True)
    
    # Security fields
    password_changed_at = models.DateTimeField(null=True, blank=True)
    password_history = models.JSONField(default=list, blank=True)  # Store last 5 password hashes
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return self.email

    @property
    def storage_percentage(self):
        """Calculate storage usage percentage."""
        if self.storage_limit == 0:
            return 0
        return (self.storage_used / self.storage_limit) * 100

    def has_storage_available(self, file_size):
        """Check if user has enough storage for a file."""
        return (self.storage_used + file_size) <= self.storage_limit
    
    @property
    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until:
            from django.utils import timezone
            return timezone.now() < self.account_locked_until
        return False
    
    @property
    def requires_mfa(self):
        """Check if user role requires MFA"""
        return self.role in ['Super_Admin', 'Admin']
    
    def has_permission(self, permission):
        """Check if user has a specific permission based on role"""
        from .permissions import ROLE_PERMISSIONS
        return permission in ROLE_PERMISSIONS.get(self.role, [])
