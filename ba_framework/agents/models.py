from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta
import pytz
import os
from django.apps import apps
# Importing SearchVector from Django's PostgreSQL full-text search support to enable full-text search capabilities.
from django.contrib.postgres.search import SearchVector


class Building(models.Model):
    name = models.CharField(max_length=30, default="UNKNOWN", null=True,)
    location = models.CharField(max_length=30, blank=True, null=True,)

    def __str__(self):
        return self.name + " -- " + self.location
    
# class Vicki_Thermostat(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     serial_number = models.CharField(max_length=100, null=True, blank=True)
#     device_id_ttn = models.CharField(max_length=100, null=True, blank=True)
#     ttn_webook_id = models.CharField(max_length=100, null=True, blank=True)
#     ttn_app_id = models.CharField(max_length=100, null=True, blank=True)
#     ttn_token = models.CharField(max_length=100, null=True, blank=True)
#     ttn_m_token = models.CharField(max_length=100, null=True, blank=True)
#     target_temperature = models.CharField(max_length=100, null=True, blank=True)
#     operational_mode = models.CharField(max_length=100, null=True, blank=True)
#     motor_position = models.CharField(max_length=100, null=True, blank=True)
#     downlink_motor_position = models.CharField(max_length=100, null=True, blank=True)
#     motor_range = models.CharField(max_length=100, null=True, blank=True)
#     internal_sensor_temperatur = models.CharField(max_length=100, null=True, blank=True)
#     battery_voltage = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.room.name + " -- " + self.serial_number




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


# Signal receiver to create a Profile whenever a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # This function is called whenever a User instance is saved.
    # If the User instance is newly created (created=True),
    # it creates a new Profile instance linked to this User.
    if created:
        Profile.objects.create(user=instance, username=instance.username)


# Signal receiver to save the Profile whenever the User is saved.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This function is called whenever a User instance is saved.
    # It tries to save the associated Profile instance.
    # If the Profile instance does not exist (ObjectDoesNotExist),
    # it creates a new Profile instance linked to this User.
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance, username=instance.username)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     try:
#         instance.profile.save()
#     except ObjectDoesNotExist:
#         Profile.objects.create(user=instance, username=instance.username)


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

class Sensor(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, unique=True)  # Assuming device ID should be unique
    table_id = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    data_point_name = models.CharField(max_length=100)
    data_point_type = models.CharField(max_length=100)
    measurement_type = models.CharField(max_length=100)
    description = models.TextField()  # Use TextField if descriptions can be long

    def __str__(self):
        return f"{self.device_name} ({self.device_id})"
    
class Room_Monitoring_Sensors(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.device_name} ({self.sensor.device_id}) - {self.value} ({self.timestamp})"