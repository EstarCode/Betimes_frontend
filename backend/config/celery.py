"""
Celery configuration for PDF Utility SaaS Platform.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('pdf_utility')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'cleanup-old-files': {
        'task': 'apps.compression.tasks.cleanup_old_files',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
    'cleanup-failed-jobs': {
        'task': 'apps.compression.tasks.cleanup_failed_jobs',
        'schedule': crontab(hour=3, minute=0),  # Run daily at 3 AM
    },
    'cleanup-old-conversion-files': {
        'task': 'apps.conversion.tasks.cleanup_old_conversion_files',
        'schedule': crontab(hour=2, minute=30),  # Run daily at 2:30 AM
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery configuration."""
    print(f'Request: {self.request!r}')
