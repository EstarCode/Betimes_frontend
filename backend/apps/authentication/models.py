"""
User model for authentication.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_premium = models.BooleanField(default=False)
    storage_used = models.BigIntegerField(default=0, help_text="Storage used in bytes")
    storage_limit = models.BigIntegerField(default=1073741824, help_text="Storage limit in bytes (default 1GB)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

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
