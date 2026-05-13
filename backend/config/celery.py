"""
Celery configuration for background task processing
Handles async processing of file operations, notifications, and cleanup tasks
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('betimes')

# Load configuration from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Configure task queues
app.conf.task_routes = {
    'apps.conversion.tasks.*': {'queue': 'conversion'},
    'apps.compression.tasks.*': {'queue': 'compression'},
    'apps.notifications.tasks.*': {'queue': 'notifications'},
    'apps.*.tasks.cleanup_*': {'queue': 'cleanup'},
}

# Configure task priorities
app.conf.task_default_priority = 5
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True

# Configure retry behavior
app.conf.task_default_retry_delay = 60  # 1 minute
app.conf.task_max_retries = 3

# Configure periodic tasks
app.conf.beat_schedule = {
    'cleanup-temp-files': {
        'task': 'apps.uploads.tasks.cleanup_temp_files',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'cleanup-failed-jobs': {
        'task': 'apps.processing.tasks.cleanup_failed_jobs',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    'cleanup-completed-jobs': {
        'task': 'apps.processing.tasks.cleanup_completed_jobs',
        'schedule': crontab(hour=4, minute=0),  # Daily at 4 AM
    },
    'collect-system-metrics': {
        'task': 'apps.dashboard.tasks.collect_system_metrics',
        'schedule': 30.0,  # Every 30 seconds
    },
    'check-workflow-escalations': {
        'task': 'apps.workflows.tasks.check_escalations',
        'schedule': 3600.0,  # Every hour
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
