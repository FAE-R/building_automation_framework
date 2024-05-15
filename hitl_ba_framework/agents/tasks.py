from .models import Room
from django.dispatch import receiver
from celery import shared_task
from hitl_ba_framework.celery import app
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from django.utils import timezone
import json
from django_celery_beat.models import PeriodicTask, PeriodicTasks, CrontabSchedule, IntervalSchedule
from django.apps import apps
from celery import shared_task
from django.db.models.signals import post_save, pre_save
from django_celery_results.models import TaskResult


logger = get_task_logger(__name__)
