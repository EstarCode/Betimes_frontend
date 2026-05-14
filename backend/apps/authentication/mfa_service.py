"""
Multi-Factor Authentication Service
Requirement 13: MFA with TOTP and SMS
Follows OWASP Authentication Guidelines
"""
import pyotp
import qrcode
import io
import base64
import secrets
import logging
from typing import Dict, List, Tuple
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class MFAService:
    """
    Enterprise MFA service with TOTP and SMS support
    Implements OWASP best practices for 2FA
    """
    
    BACKUP_CODE_COUNT = 10
    BACKUP_CODE_LENGTH = 8
    
    def setup_totp(self, user) -> Dict:
        """
        Setup TOTP for user
        
        Args:
            user: User instance
        
        Returns:
            dict: Setup data with secret and QR code
        """
        try:
            # Generate secret
            secret = pyotp.random_base32()
            
            # Create TOTP instance
            totp = pyotp.TOTP(secret)
            
            # Generate provisioning URI
            issuer_name = getattr(settings, 'MFA_ISSUER_NAME', 'Betimes Enterprise')
            provisioning_uri = totp.provisioning_uri(
                name=user.email,
                issuer_name=issuer_name
            )
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Generate backup codes
            backup_codes = self.generate_backup_codes()
            
            # Store temporarily (don't save to user yet)
            cache_key = f"mfa_setup_{user.id}"
            cache.set(cache_key, {
                'secret': secret,
                'backup_codes': backup_codes
            }, timeout=600)  # 10 minutes
            
            logger.info(f"MFA setup initiated for user: {user.email}")
            
            return {
                'success': True,
                'secret': secret,
                'qr_code': f"data:image/png;base64,{qr_code_base64}",
                'provisioning_uri': provisioning_uri,
                'backup_codes': backup_codes
            }
            
        except Exception as e:
            logger.exception(f"MFA setup failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_totp_setup(self, user, token: str) -> bool:
        """
        Verify TOTP token during setup
        
        Args:
            user: User instance
            token: 6-digit TOTP token
        
        Returns:
            bool: Verification success
        """
        try:
            # Get temporary setup data
            cache_key = f"mfa_setup_{user.id}"
            setup_data = cache.get(cache_key)
            
            if not setup_data:
                logger.warning(f"MFA setup data not found for user: {user.email}")
                return False
            
            secret = setup_data['secret']
            backup_codes = setup_data['backup_codes']
            
            # Verify token
            totp = pyotp.TOTP(secret)
            if totp.verify(token, valid_window=1):
                # Save to user
                user.mfa_enabled = True
                user.mfa_secret = secret
                user.backup_codes = backup_codes
                user.save()
                
                # Clear cache
                cache.delete(cache_key)
                
                logger.info(f"MFA enabled for user: {user.email}")
                return True
            
            logger.warning(f"Invalid MFA token during setup for user: {user.email}")
            return False
            
        except Exception as e:
            logger.exception(f"MFA verification failed: {str(e)}")
            return False
    
    def verify_totp(self, user, token: str) -> bool:
        """
        Verify TOTP token for authentication
        
        Args:
            user: User instance
            token: 6-digit TOTP token
        
        Returns:
            bool: Verification success
        """
        try:
            if not user.mfa_enabled or not user.mfa_secret:
                return False
            
            totp = pyotp.TOTP(user.mfa_secret)
            
            # Verify with 1-step window (30 seconds before/after)
            if totp.verify(token, valid_window=1):
                logger.info(f"MFA token verified for user: {user.email}")
                return True
            
            logger.warning(f"Invalid MFA token for user: {user.email}")
            return False
            
        except Exception as e:
            logger.exception(f"MFA token verification failed: {str(e)}")
            return False
    
    def verify_backup_code(self, user, code: str) -> bool:
        """
        Verify and consume backup code
        
        Args:
            user: User instance
            code: Backup code
        
        Returns:
            bool: Verification success
        """
        try:
            if not user.mfa_enabled or not user.backup_codes:
                return False
            
            # Check if code exists
            if code in user.backup_codes:
                # Remove used code
                user.backup_codes.remove(code)
                user.save()
                
                logger.info(f"Backup code used for user: {user.email}")
                return True
            
            logger.warning(f"Invalid backup code for user: {user.email}")
            return False
            
        except Exception as e:
            logger.exception(f"Backup code verification failed: {str(e)}")
            return False
    
    def disable_mfa(self, user) -> bool:
        """
        Disable MFA for user
        
        Args:
            user: User instance
        
        Returns:
            bool: Success status
        """
        try:
            user.mfa_enabled = False
            user.mfa_secret = ''
            user.backup_codes = []
            user.save()
            
            logger.info(f"MFA disabled for user: {user.email}")
            return True
            
        except Exception as e:
            logger.exception(f"MFA disable failed: {str(e)}")
            return False
    
    def generate_backup_codes(self) -> List[str]:
        """
        Generate backup codes
        
        Returns:
            list: List of backup codes
        """
        codes = []
        for _ in range(self.BACKUP_CODE_COUNT):
            code = ''.join(secrets.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') 
                          for _ in range(self.BACKUP_CODE_LENGTH))
            codes.append(code)
        return codes
    
    def regenerate_backup_codes(self, user) -> List[str]:
        """
        Regenerate backup codes for user
        
        Args:
            user: User instance
        
        Returns:
            list: New backup codes
        """
        try:
            new_codes = self.generate_backup_codes()
            user.backup_codes = new_codes
            user.save()
            
            logger.info(f"Backup codes regenerated for user: {user.email}")
            return new_codes
            
        except Exception as e:
            logger.exception(f"Backup code regeneration failed: {str(e)}")
            return []
    
    def send_sms_code(self, user, phone_number: str) -> Tuple[bool, str]:
        """
        Send SMS verification code
        
        Args:
            user: User instance
            phone_number: Phone number to send code to
        
        Returns:
            tuple: (success, message)
        """
        try:
            # Generate 6-digit code
            code = ''.join(secrets.choice('0123456789') for _ in range(6))
            
            # Store code in cache (5 minutes expiry)
            cache_key = f"sms_code_{user.id}"
            cache.set(cache_key, code, timeout=300)
            
            # Send SMS using Twilio (if configured)
            if hasattr(settings, 'TWILIO_ACCOUNT_SID') and settings.TWILIO_ACCOUNT_SID:
                from twilio.rest import Client
                
                client = Client(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )
                
                message = client.messages.create(
                    body=f"Your Betimes verification code is: {code}",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
                
                logger.info(f"SMS code sent to user: {user.email}")
                return True, "SMS code sent successfully"
            else:
                # Development mode - log code
                logger.info(f"SMS code for {user.email}: {code}")
                return True, f"Development mode - Code: {code}"
            
        except Exception as e:
            logger.exception(f"SMS send failed: {str(e)}")
            return False, str(e)
    
    def verify_sms_code(self, user, code: str) -> bool:
        """
        Verify SMS code
        
        Args:
            user: User instance
            code: 6-digit SMS code
        
        Returns:
            bool: Verification success
        """
        try:
            cache_key = f"sms_code_{user.id}"
            stored_code = cache.get(cache_key)
            
            if stored_code and stored_code == code:
                # Clear code after successful verification
                cache.delete(cache_key)
                logger.info(f"SMS code verified for user: {user.email}")
                return True
            
            logger.warning(f"Invalid SMS code for user: {user.email}")
            return False
            
        except Exception as e:
            logger.exception(f"SMS code verification failed: {str(e)}")
            return False
    
    def check_mfa_required(self, user) -> bool:
        """
        Check if MFA is required for user role
        
        Args:
            user: User instance
        
        Returns:
            bool: MFA required
        """
        # MFA required for Super_Admin and Admin roles
        return user.role in ['Super_Admin', 'Admin']
