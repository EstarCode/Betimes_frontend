"""
URL configuration for authentication.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    UserProfileView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    mfa_setup,
    mfa_verify_setup,
    mfa_disable,
    mfa_regenerate_backup_codes,
    mfa_verify_login
)

app_name = 'authentication'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # MFA endpoints
    path('mfa/setup/', mfa_setup, name='mfa_setup'),
    path('mfa/verify-setup/', mfa_verify_setup, name='mfa_verify_setup'),
    path('mfa/disable/', mfa_disable, name='mfa_disable'),
    path('mfa/regenerate-backup-codes/', mfa_regenerate_backup_codes, name='mfa_regenerate_backup_codes'),
    path('mfa/verify-login/', mfa_verify_login, name='mfa_verify_login'),
]
