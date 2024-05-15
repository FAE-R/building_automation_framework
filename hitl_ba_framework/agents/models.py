from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.utils import timezone
from datetime import timedelta
import pytz
import os
from django.apps import apps
from django.contrib.postgres.search import SearchVector

class Building(models.Model):
    name = models.CharField(max_length=30, default="UNKNOWN", null=True,)
    location = models.CharField(max_length=30, blank=True, null=True,)

    def __str__(self):
        return self.name + " -- " + self.location


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30, default="UNKNOWN")
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, null=True)
    join_date = models.DateField(null=True, blank=True)
    push_notification_token = models.CharField(max_length=150, blank=True)
    geofencing_active = models.BooleanField(default=False)
    notification_active = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance, username=instance.username)


class Room(models.Model):
    name = models.CharField(
        max_length=30, default="UNKNOWN", null=True, blank=True)
    room_type = models.CharField(max_length=30, null=True, blank=True, choices=(
        ('Office', 'Office'), ('Meeting_Room', 'Meeting_Room'), ('Floor', 'Floor'), ('Bedroom', 'Bedroom'), ('Living_Room', 'Living_Room'), ('Others', 'Others')))
    user_number = models.IntegerField(default=1, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    control_mode = models.CharField(max_length=30, null=True, blank=True, choices=(
        ('Off', 'Off'), ('Manual', 'Manual'), ('Adaptive', 'Adaptive')))
    occupied = models.BooleanField(null=True, blank=True)
    last_change = models.DateTimeField(auto_now=True)
    last_change_by_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    temperature_setpoint = models.FloatField(
        null=True, blank=True, validators=[MaxValueValidator(28), MinValueValidator(12)])
    temperature_setpoint_max = models.FloatField(
        null=True, blank=True, validators=[MaxValueValidator(28), MinValueValidator(12)])
    temperature_setpoint_min = models.FloatField(
        null=True, blank=True, validators=[MaxValueValidator(28), MinValueValidator(12)])
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name + " -- " + self.building.name



@receiver(pre_save, sender=Room)
def on_change(sender, instance: Room, **kwargs):
    if instance.id is None:
        pass
    else:
        previous = Room.objects.get(id=instance.id)

        if instance.control_mode == "Manual" and previous.occupied == instance.occupied:

            table_list = Room_Monitoring_Datapoints.objects.get(
                room=previous)
            if instance.last_change_by_user is not None:
                feedback = Comfort_Feedback.objects.create(
                    room=previous, user=instance.last_change_by_user)
            else:
                feedback = Comfort_Feedback.objects.create(
                        room=previous, user=Profile.objects.get(pk=1))
            if table_list is not None:
                ranges = (timezone.now() -
                          timedelta(hours=1), timezone.now())

                if table_list.temperature != None:
                    table = apps.get_model(
                        'logger', table_list.temperature)
                    value = table.timescale.filter(
                        time__range=ranges).last()
                    if value != None:
                        feedback.temperature = value.value

                if table_list.temperature_out != None:
                    table = apps.get_model(
                        'logger', table_list.temperature_out)
                    value = table.timescale.filter(
                        time__range=ranges).last()
                    if value != None:
                        feedback.temperature_out = value.value

                if table_list.humidity != None:
                    table = apps.get_model(
                        'logger', table_list.humidity)
                    value = table.timescale.filter(
                        time__range=ranges).last()
                    if value != None:
                        feedback.humidity = value.value

                if table_list.co2 != None:
                    table = apps.get_model(
                        'logger', table_list.co2)
                    value = table.timescale.filter(
                        time__range=ranges).last()
                    if value != None:
                        feedback.co2 = value.value

                if table_list.light != None:
                    table = apps.get_model(
                        'logger', table_list.light)
                    value = table.timescale.filter(
                        time__range=ranges).last()
                    if value != None:
                        feedback.light = value.value

                feedback.feedback_setpoint = instance.temperature_setpoint
                feedback.datetime = timezone.now()
                feedback.save()


class Room_Users(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    tracker_table = models.CharField(max_length=100, null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    still_use_room = models.BooleanField(default=True, null=True, blank=True)
    leave_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.room.name + " -- " + self.user.user.username


def agent_directory_path(instance, filename):
    file_path = 'static/agents/roomID_{0}/{1}'.format(instance.room.id, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return file_path

class Room_Monitoring_Datapoints(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    temperature_out = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.CharField(max_length=100, null=True, blank=True)
    humidity = models.CharField(max_length=100, null=True, blank=True)
    co2 = models.CharField(max_length=100, null=True, blank=True)
    motion = models.CharField(max_length=100, null=True, blank=True)
    ir = models.CharField(max_length=100, null=True, blank=True)
    light = models.CharField(max_length=100, null=True, blank=True)
    humidity_out = models.CharField(max_length=100, null=True, blank=True)
    global_radiation = models.CharField(max_length=100, null=True, blank=True)
    doors_open = models.CharField(max_length=150, null=True, blank=True)
    doors_counter = models.CharField(max_length=150, null=True, blank=True)
    windows_open = models.CharField(max_length=450, null=True, blank=True)
    windows_counter = models.CharField(max_length=450, null=True, blank=True)
    co2_threshold_lastday_10min = models.IntegerField(null=False, blank=False, default=50)
    co2_threshold_lastday_20min = models.IntegerField(null=False, blank=False, default=80)
    co2_threshold_week_10min = models.IntegerField(null=False, blank=False, default=50)
    rl_agent_file = models.FileField(upload_to=agent_directory_path, null=True, blank=True)

    def __str__(self):
        return self.room.name


class Vicki_Thermostat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    device_id_ttn = models.CharField(max_length=100, null=True, blank=True)
    ttn_webook_id = models.CharField(max_length=100, null=True, blank=True)
    ttn_app_id = models.CharField(max_length=100, null=True, blank=True)
    ttn_token = models.CharField(max_length=100, null=True, blank=True)
    ttn_m_token = models.CharField(max_length=100, null=True, blank=True)
    target_temperature = models.CharField(max_length=100, null=True, blank=True)
    operational_mode = models.CharField(max_length=100, null=True, blank=True)
    motor_position = models.CharField(max_length=100, null=True, blank=True)
    downlink_motor_position = models.CharField(max_length=100, null=True, blank=True)
    motor_range = models.CharField(max_length=100, null=True, blank=True)
    internal_sensor_temperatur = models.CharField(max_length=100, null=True, blank=True)
    battery_voltage = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.room.name + " -- " + self.serial_number
    

class Scheduler(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=50, null=True, blank=True,
                                   choices=((0, 'Monday'), (1, 'Tuesday'),
                                            (2, 'Wednesday'), (3, 'Thursday'),
                                            (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')))
    hour = models.PositiveSmallIntegerField(null=True, blank=True, 
        validators=[MaxValueValidator(24), MinValueValidator(0)])
    quarter = models.PositiveSmallIntegerField(null=True, blank=True, 
        validators=[MaxValueValidator(4), MinValueValidator(0)])
    occupied_rate = models.FloatField(null=True, blank=True, validators=[
                                      MaxValueValidator(100), MinValueValidator(0)])

    def __str__(self):
        return self.room.name + " -- " + self.day_of_week + " -- " + str(self.hour)


class Comfort_Feedback(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    feedback = models.CharField(max_length=50, null=True, blank=True,
                                choices=((2, 'Comfortable'), (1, 'Cold'),
                                         (0, 'Too Cold'), (3, 'Hot'),
                                         (4, 'Too Hot')))
    feedback_setpoint = models.FloatField(null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    temperature_out = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    co2 = models.FloatField(null=True, blank=True)
    light = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.room.name + " -- " + self.user.username + "--" + str(self.feedback)


class Notification(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True,
                                choices=((0, 'CO2'), (1, 'Comfort_Feedback'),
                                         (2, 'Control')))
    sent = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.room.name + " -- " + self.title


# @receiver(post_save)
# def check_occupancy_by_change(sender, instance, created, **kwargs):
#     list_door_models = ['Tab1_0226_status']
#     door = Room_Monitoring_Datapoints.objects.annotate(search=SearchVector(
#         "door1", "door2", "door3")).filter(search=sender.__name__).last()
#     if door is not None:
#         print("door opened/closed ...", door.room.name)
#         update_0226_status_active.delay("02:26")
