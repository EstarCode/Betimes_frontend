"""
Celery Tasks for Notifications
Requirement 21: Background Task Processing
Requirement 18: Notification System
"""
from celery import shared_task
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Notification

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_notification_task(self, notification_id):
    """
    Send email notification
    
    Args:
        notification_id: Notification UUID
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        
        logger.info(f"Sending email notification to {notification.user.email}")
        
        send_mail(
            subject=notification.subject,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
            fail_silently=False,
        )
        
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        
        logger.info(f"Email notification sent successfully to {notification.user.email}")
        return {'success': True, 'notification_id': str(notification_id)}
        
    except Notification.DoesNotExist:
        logger.error(f"Notification not found: {notification_id}")
        return {'success': False, 'error': 'Notification not found'}
    except Exception as e:
        logger.exception(f"Email notification failed: {str(e)}")
        
        # Update notification status
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.status = 'failed'
            notification.save()
        except:
            pass
        
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task(bind=True, max_retries=3)
def send_sms_notification_task(self, notification_id, phone_number):
    """
    Send SMS notification
    
    Args:
        notification_id: Notification UUID
        phone_number: Recipient phone number
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        
        logger.info(f"Sending SMS notification to {phone_number}")
        
        # Send SMS using Twilio (if configured)
        if hasattr(settings, 'TWILIO_ACCOUNT_SID') and settings.TWILIO_ACCOUNT_SID:
            from twilio.rest import Client
            
            client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
            
            message = client.messages.create(
                body=notification.message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            
            notification.status = 'sent'
            notification.sent_at = timezone.now()
            notification.save()
            
            logger.info(f"SMS notification sent successfully to {phone_number}")
            return {'success': True, 'notification_id': str(notification_id)}
        else:
            logger.warning("Twilio not configured - SMS not sent")
            return {'success': False, 'error': 'SMS service not configured'}
        
    except Notification.DoesNotExist:
        logger.error(f"Notification not found: {notification_id}")
        return {'success': False, 'error': 'Notification not found'}
    except Exception as e:
        logger.exception(f"SMS notification failed: {str(e)}")
        
        # Update notification status
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.status = 'failed'
            notification.save()
        except:
            pass
        
        raise self.retry(exc=e, countdown=2 ** self.request.retries)


@shared_task
def batch_send_notifications_task(notification_ids):
    """
    Batch send multiple notifications
    
    Args:
        notification_ids: List of notification UUIDs
    """
    logger.info(f"Batch sending {len(notification_ids)} notifications")
    
    results = []
    for notification_id in notification_ids:
        try:
            notification = Notification.objects.get(id=notification_id)
            
            if notification.channel == 'email':
                result = send_email_notification_task.delay(notification_id)
            elif notification.channel == 'sms':
                # Assuming phone number is stored in user profile
                phone_number = getattr(notification.user, 'phone_number', None)
                if phone_number:
                    result = send_sms_notification_task.delay(notification_id, phone_number)
                else:
                    logger.warning(f"No phone number for user: {notification.user.email}")
                    continue
            
            results.append({'notification_id': str(notification_id), 'status': 'queued'})
            
        except Exception as e:
            logger.exception(f"Failed to queue notification {notification_id}: {str(e)}")
            results.append({'notification_id': str(notification_id), 'status': 'failed', 'error': str(e)})
    
    return results


@shared_task
def cleanup_old_notifications_task():
    """
    Clean up old read notifications (older than 30 days)
    Runs daily at 2 AM
    """
    from datetime import timedelta
    
    logger.info("Starting notification cleanup task")
    
    cutoff_date = timezone.now() - timedelta(days=30)
    
    deleted_count, _ = Notification.objects.filter(
        read_at__isnull=False,
        read_at__lt=cutoff_date
    ).delete()
    
    logger.info(f"Cleaned up {deleted_count} old notifications")
    return {'deleted_count': deleted_count}
