# Import the os module for interacting with the operating system
import os
# Import the Celery class from the celery module for creating Celery applications
from celery import Celery
# Import the crontab schedule class from the celery.schedules module for scheduling tasks
from celery.schedules import crontab
# Import the timedelta class from the datetime module for creating time intervals
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ba_framework.settings')

# Instantiate a Celery application with the name 'ba_framework'.
app = Celery('ba_framework')

# Load the configuration from the Django settings, using the 'CELERY' namespace.
# This allows us to configure Celery in the Django settings file using a prefix 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all installed apps. Celery will look for a 'tasks.py' file in each application.
app.autodiscover_tasks()
