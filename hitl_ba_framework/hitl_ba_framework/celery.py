import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hitl_ba_framework.settings')

app = Celery('hitl_ba_framework')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
