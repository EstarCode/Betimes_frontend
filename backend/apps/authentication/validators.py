"""
Custom Password Validators
Implements OWASP Password Guidelines
Requirement 15: Password Requirements
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MinimumLengthValidator:
    """
    Validate password has minimum 12 characters
    """
    def __init__(self, min_length=12):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Password must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters."
            % {'min_length': self.min_length}
        )


class UppercaseValidator:
    """
    Validate password contains at least one uppercase letter
    """
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter.")


class LowercaseValidator:
    """
    Validate password contains at least one lowercase letter
    """
    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _("Your password must contain at least one lowercase letter.")


class NumberValidator:
    """
    Validate password contains at least one number
    """
    def validate(self, password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Password must contain at least one number."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _("Your password must contain at least one number.")


class SpecialCharacterValidator:
    """
    Validate password contains at least one special character
    """
    def validate(self, password, user=None):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _("Your password must contain at least one special character.")


class CommonPasswordValidator:
    """
    Validate password is not in common passwords list
    """
    COMMON_PASSWORDS = [
        'password', 'password123', '123456', '12345678', 'qwerty',
        'abc123', 'monkey', '1234567', 'letmein', 'trustno1',
        'dragon', 'baseball', 'iloveyou', 'master', 'sunshine',
        'ashley', 'bailey', 'passw0rd', 'shadow', '123123',
        'admin', 'administrator', 'root', 'toor', 'pass',
    ]

    def validate(self, password, user=None):
        if password.lower() in self.COMMON_PASSWORDS:
            raise ValidationError(
                _("This password is too common. Please choose a more secure password."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Your password can't be a commonly used password.")


class PasswordHistoryValidator:
    """
    Validate password hasn't been used in last 5 passwords
    Requirement 15: Prevent password reuse
    """
    def validate(self, password, user=None):
        if user and hasattr(user, 'password_history'):
            from django.contrib.auth.hashers import check_password
            
            password_history = user.password_history or []
            
            for old_password_hash in password_history[-5:]:  # Check last 5 passwords
                if check_password(password, old_password_hash):
                    raise ValidationError(
                        _("You cannot reuse any of your last 5 passwords."),
                        code='password_reused',
                    )

    def get_help_text(self):
        return _("Your password can't be one of your last 5 passwords.")


class MaximumLengthValidator:
    """
    Validate password doesn't exceed maximum length (prevent DoS)
    """
    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _("Password must not exceed %(max_length)d characters."),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return _(
            "Your password must not exceed %(max_length)d characters."
            % {'max_length': self.max_length}
        )
