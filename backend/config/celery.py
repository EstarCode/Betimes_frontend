"""
Celery Configuration
Requirement 21: Background Task Processing with priorities and auto-scaling
"""
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('betimes_enterprise')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Task routing - separate queues for different job types
app.conf.task_routes = {
    'apps.conversion.tasks.*': {'queue': 'conversion'},
    'apps.compression.tasks.*': {'queue': 'compression'},
    'apps.notifications.tasks.*': {'queue': 'notifications'},
    'apps.workflows.tasks.*': {'queue': 'workflows'},
}

# Task priorities
app.conf.task_default_priority = 5
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True

# Retry configuration with exponential backoff
app.conf.task_autoretry_for = (Exception,)
app.conf.task_retry_backoff = True
app.conf.task_retry_backoff_max = 600  # 10 minutes max
app.conf.task_retry_jitter = True

# Beat schedule for periodic tasks
app.conf.beat_schedule = {
    # Clean up expired temporary files daily at 2 AM
    'cleanup-temp-files': {
        'task': 'apps.uploads.tasks.cleanup_temp_files_task',
        'schedule': crontab(hour=2, minute=0),
    },
    # Clean up old notifications daily at 2 AM
    'cleanup-old-notifications': {
        'task': 'apps.notifications.tasks.cleanup_old_notifications_task',
        'schedule': crontab(hour=2, minute=0),
    },
    # Check for workflow escalations every hour
    'check-workflow-escalations': {
        'task': 'apps.workflows.tasks.check_escalations_task',
        'schedule': crontab(minute=0),  # Every hour
    },
    # Update system metrics every 5 minutes
    'update-system-metrics': {
        'task': 'apps.dashboard.tasks.update_metrics_task',
        'schedule': crontab(minute='*/5'),
    },
}

# Worker configuration
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_max_tasks_per_child = 1000

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
