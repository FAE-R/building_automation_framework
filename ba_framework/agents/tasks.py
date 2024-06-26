# Importing the Room model from the current package's models module.
from .models import Room

# Importing the receiver decorator from Django's dispatch module to connect signals to functions.
from django.dispatch import receiver

# Importing shared_task decorator from Celery to define tasks that can be executed asynchronously.
from celery import shared_task

# Importing the Celery application instance from the project-specific Celery configuration module.
from ba_framework.celery import app

# Importing get_task_logger from Celery to create loggers for tasks.
from celery.utils.log import get_task_logger

# Importing crontab schedule constructor from Celery for defining periodic tasks with cron-like schedules.
from celery.schedules import crontab

# Importing timezone utilities from Django to handle date and time in a timezone-aware manner.
from django.utils import timezone

# Importing the json module for parsing and creating JSON data.
import json

# Importing models from django_celery_beat for managing periodic tasks.
from django_celery_beat.models import PeriodicTask, PeriodicTasks, CrontabSchedule, IntervalSchedule

# Importing apps module from Django to work with Django applications.
from django.apps import apps

# Importing shared_task again from Celery (this is a duplicate import, and can be removed).
from celery import shared_task

# Importing post_save and pre_save signals from Django's models module to trigger actions after or before saving a model instance.
from django.db.models.signals import post_save, pre_save

# Importing TaskResult model from django_celery_results to store the results of Celery tasks.
from django_celery_results.models import TaskResult


from .functions.occupancy_detection_task import Occupancy_Detection

# Creating a logger for tasks in this module, which allows logging messages within tasks.
logger = get_task_logger(__name__)


@shared_task(bind=True, name="update_occupancy")
def update_occupancy(self, room_name, *args, **kwargs):

    room = Room.objects.get(name=room_name)

    if room is not None:
        current_state = 0

        last_task_result = TaskResult.objects.filter(periodic_task_name=TaskResult.objects.get(task_id=self.request.id).periodic_task_name).last()

        if last_task_result is not None:
            if last_task_result.status == "SUCCESS":
                current_state = int(last_task_result.result)
            else:
                current_state = 0
        else:
            current_state = 0 

        result = Occupancy_Detection(room=room, current_state=current_state)
        if result is not None:
            return result

    else:
        return "Room object is None"
