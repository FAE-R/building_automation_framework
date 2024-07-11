from .models import Room
from django.dispatch import receiver
from celery import shared_task
from ba_framework.celery import app
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from django_celery_beat.models import PeriodicTask, PeriodicTasks, CrontabSchedule, IntervalSchedule
from django.apps import apps
from celery import shared_task
from django_celery_results.models import TaskResult


from .functions.occupancy_detection_task import Occupancy_Detection

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
