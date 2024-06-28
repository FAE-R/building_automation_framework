import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ba_framework.settings')

app = Celery('ba_framework')

# Load the configuration from the Django settings, using the 'CELERY' namespace.
# This allows us to configure Celery in the Django settings file using a prefix 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
