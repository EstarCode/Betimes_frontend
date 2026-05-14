"""
Celery Tasks for Workflow Management
Requirement 21: Background Task Processing
Requirement 11: Workflow Escalation
"""
from celery import shared_task
import logging
from datetime import timedelta
from django.utils import timezone
from .models import WorkflowInstance
from apps.notifications.models import Notification

logger = logging.getLogger(__name__)


@shared_task
def check_escalations_task():
    """
    Check for workflows that need escalation
    Runs every hour
    Requirement 11: Escalate after 48 hours
    """
    logger.info("Checking for workflow escalations")
    
    cutoff_time = timezone.now() - timedelta(hours=48)
    
    # Find workflows pending for more than 48 hours
    pending_workflows = WorkflowInstance.objects.filter(
        status__in=['pending', 'in_review'],
        updated_at__lt=cutoff_time
    )
    
    escalated_count = 0
    
    for workflow in pending_workflows:
        try:
            # Update workflow status
            workflow.status = 'escalated'
            workflow.save()
            
            # Create notification for escalation
            Notification.objects.create(
                user=workflow.initiated_by,
                type='workflow_escalated',
                channel='email',
                subject=f'Workflow Escalated: {workflow.document.filename}',
                message=f'Your workflow for document "{workflow.document.filename}" has been escalated due to pending approval for more than 48 hours.'
            )
            
            # Notify next level manager (if configured)
            if workflow.template and hasattr(workflow.template, 'escalation_manager'):
                Notification.objects.create(
                    user=workflow.template.escalation_manager,
                    type='workflow_escalation_alert',
                    channel='email',
                    subject=f'Escalation Alert: {workflow.document.filename}',
                    message=f'Workflow for document "{workflow.document.filename}" has been escalated and requires your attention.'
                )
            
            escalated_count += 1
            logger.info(f"Escalated workflow: {workflow.id}")
            
        except Exception as e:
            logger.exception(f"Failed to escalate workflow {workflow.id}: {str(e)}")
    
    logger.info(f"Escalated {escalated_count} workflows")
    return {'escalated_count': escalated_count}


@shared_task
def send_workflow_notification_task(workflow_id, event_type):
    """
    Send workflow event notifications
    
    Args:
        workflow_id: Workflow instance UUID
        event_type: Event type (approved, rejected, escalated, etc.)
    """
    try:
        workflow = WorkflowInstance.objects.get(id=workflow_id)
        
        # Determine recipients based on event type
        recipients = []
        
        if event_type == 'approved':
            recipients.append(workflow.initiated_by)
            message = f'Your workflow for document "{workflow.document.filename}" has been approved.'
        elif event_type == 'rejected':
            recipients.append(workflow.initiated_by)
            message = f'Your workflow for document "{workflow.document.filename}" has been rejected.'
        elif event_type == 'stage_completed':
            recipients.append(workflow.initiated_by)
            message = f'Stage {workflow.current_stage} of your workflow for document "{workflow.document.filename}" has been completed.'
        
        # Create notifications
        for recipient in recipients:
            Notification.objects.create(
                user=recipient,
                type=f'workflow_{event_type}',
                channel='email',
                subject=f'Workflow Update: {workflow.document.filename}',
                message=message
            )
        
        logger.info(f"Sent workflow notifications for {workflow_id}: {event_type}")
        return {'success': True, 'recipients': len(recipients)}
        
    except WorkflowInstance.DoesNotExist:
        logger.error(f"Workflow not found: {workflow_id}")
        return {'success': False, 'error': 'Workflow not found'}
    except Exception as e:
        logger.exception(f"Failed to send workflow notification: {str(e)}")
        return {'success': False, 'error': str(e)}
