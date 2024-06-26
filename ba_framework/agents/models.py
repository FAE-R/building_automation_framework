# Importing the models module from Django, which provides the base classes for defining database models.
from django.db import models

# Importing the User model from Django's built-in authentication system to handle user-related data.
from django.contrib.auth.models import User

# Importing the post_save and pre_save signals from Django's models module, which are triggered after or before saving a model instance, respectively.
from django.db.models.signals import post_save, pre_save

# Importing the receiver decorator from Django's dispatch module to connect signal handlers to signals.
from django.dispatch import receiver

# Importing validators from Django's core validators to enforce constraints on model fields.
from django.core.validators import MaxValueValidator, MinValueValidator

# Importing ObjectDoesNotExist exception from Django's core exceptions to handle cases where an object does not exist.
from django.core.exceptions import ObjectDoesNotExist

# Importing utilities from Django's timezone module to work with time zones and date/time fields.
from django.utils import timezone

# Importing timedelta from Python's datetime module to perform date/time manipulations.
from datetime import timedelta

# Importing pytz to handle different time zones.
import pytz

# Importing os to interact with the operating system, such as file and directory management.
import os

# Importing apps from Django to work with Django applications.
from django.apps import apps

# Importing SearchVector from Django's PostgreSQL full-text search support to enable full-text search capabilities.
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


# Signal receiver to create a Profile whenever a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # This function is called whenever a User instance is saved.
    # If the User instance is newly created (created=True),
    # it creates a new Profile instance linked to this User.
    if created:
        Profile.objects.create(user=instance, username=instance.username)


# # Signal receiver to save the Profile whenever the User is saved.
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # This function is called whenever a User instance is saved.
#     # It tries to save the associated Profile instance.
#     # If the Profile instance does not exist (ObjectDoesNotExist),
#     # it creates a new Profile instance linked to this User.
#     try:
#         instance.profile.save()
#     except ObjectDoesNotExist:
#         Profile.objects.create(user=instance, username=instance.username)

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

