import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ba_framework.settings')

app = Celery('ba_framework')

# Load the configuration from the Django settings, using the 'CELERY' namespace.
# This allows us to configure Celery in the Django settings file using a prefix 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Schedule the task to run every 1 minutes
app.conf.beat_schedule = {
    'fetch-data-every-1-minutes': {
        'task': 'agents.tasks.fetch_data_task',
        'schedule': crontab(minute='*/1'),  # Runs every 1 minutes
        'args': (1,),  # Replace with appropriate room_id
    },
}
