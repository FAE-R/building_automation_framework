from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
import uuid
import json
import redis
from django.apps import apps
from django.core.management import call_command


# Importing SearchVector from Django's PostgreSQL full-text search support to enable full-text search capabilities.
from django.contrib.postgres.search import SearchVector

redis_instance = redis.StrictRedis(
    host="redis", port=6379, db=0, charset="utf-8", decode_responses=True)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30, default="UNKNOWN")
    join_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=30, default="UNKNOWN")
    email = models.EmailField(null=True, blank=True,)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username


class Building(models.Model):
    name = models.CharField(max_length=30, default="UNKNOWN", null=False,)
    building_id = models.CharField(max_length=30, blank=True, null=True,)
    owner =  models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=30, blank=False, null=False,)
    address = models.CharField(max_length=30, blank=True, null=True,)
    city = models.CharField(max_length=30, blank=True, null=True,)
    country = models.CharField(max_length=30, blank=True, null=True,)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name + " -- " + self.location

# Signal receiver to create a Profile whenever a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # This function is called whenever a User instance is saved.
    # If the User instance is newly created (created=True),
    # it creates a new Profile instance linked to this User.
    if created:
        Profile.objects.create(user=instance, username=instance.username)


# Signal receiver to change the Profile whenever the User is saved.
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
    


SENSOR_CHOICES = [
    ("smart_thermostat_vicki", "smart_thermostat_vicki"),
    ("elsys-ers-co2", "elsys-ers-co2"),
    ("tab-elsys-ers", "tab-elsys-ers"),
    ("elsys-ers-eye", "elsys-ers-eye")
]


class Device(models.Model):
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, null=True, blank=True)
    device_id = models.CharField(max_length=30, blank=False, null=False)
    device_appEui = models.CharField(max_length=30, blank=False, null=False)
    device_devEui = models.CharField(max_length=30, blank=False, null=False)
    device_name = models.CharField(max_length=30, blank=True, null=True)
    app_id = models.CharField(max_length=30, blank=False, null=False)
    type = models.CharField(max_length=30, choices=SENSOR_CHOICES, blank=False, null=False,
                            help_text="device type (e.g. sensor, actuator, switch,…)")
    status = models.CharField(max_length=30, blank=True, null=True,
                              help_text="device status (e.g. online, offline, idle)")
    manufacturer = models.CharField(max_length=30, blank=True, null=True)
    topic = models.CharField(max_length=30, blank=True, null=True)
    firmware_version = models.CharField(max_length=30, blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True)
    mod_date = models.DateField(auto_now=True)
    description = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.device_id)

class Datapoint(models.Model):
    datapoint_name = models.CharField(max_length=100, blank=False, null=False)
    #table_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    table_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False, unique=True)
    device_eui = models.CharField(max_length=100, blank=False, null=False)
    device = models.ForeignKey(
        to=Device, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=100, default="float")
    status = models.CharField(max_length=30, blank=True, null=True,
                              help_text="datapoint status (e.g. online, offline, idle)")
    measurement_type = models.CharField(max_length=30, blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True)
    mod_date = models.DateField(auto_now=True)
    description = models.TextField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f"{self.device.type} -- {self.datapoint_name}"


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

@receiver(post_save, sender=Device)
def create_datapoints(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.type == "smart_thermostat_vicki":
                data_point_list = ["batteryVoltage", "childLock", "motorPosition", "motorRange", "sensorTemperature", "targetTemperature", "operationalMode", "manualTargetTemperatureUpdate", "downlinkMotorPosition", "keepAliveTime"]
            elif instance.type == "elsys-ers-co2":
                data_point_list = ["temperature", "humidity",
                                   "co2", "light", "motion", "vdd"]
            elif instance.type == "tab-elsys-ers":
                data_point_list = ["accMotion", "digital", "pulseAbs", "vdd", "x", "y", "z"]
            elif instance.type == "elsys-ers-eye":
                data_point_list = ["occupancy", "humidity", "light", "motion", "temperature", "vdd"]
            else:
                print("device not found in sensor list!")
                pass

            if instance.device_id is not None:
                for dp in data_point_list:
                    dp_obj = Datapoint.objects.create(
                        datapoint_name=instance.device_devEui + '_' + dp, 
                        table_id=str(uuid.uuid4().hex),
                        device=instance, 
                        device_eui=instance.device_devEui, 
                        type=dp
                    )

                    value = {
                        "data_point_name": instance.device_devEui + '_' + dp,
                        "device_name": instance.device_name,
                        "data_point": dp,
                        "device_id": instance.device_devEui,
                        "table_id": dp_obj.table_id,
                        "topic": "v3/"+instance.app_id+"@ttn/devices/#",  
                        "data_point_type": "float",
                        "measurement_type": "float",
                        "description": "this is a ..."
                    }

                    
                    
                    key = value["data_point_name"] # add data point name
                    value = json.dumps(value)
                    redis_instance.set(key, value)
                    response = {
                        'msg': f"{key} successfully set to {instance.device_devEui}"
                    }
                    print("Redis: ", response)

                call_command('makemigrations', 'logger', interactive=False)
                call_command('migrate', interactive=False)


        except ObjectDoesNotExist:
            print(
                f"Error while creating datapoints for device {instance}".format(instance))

    else:

        if instance.device_id is not None:
            dps = Datapoint.objects.filter(
                    device=instance
                )
            for dp in dps:

                value = {
                    "data_point_name": instance.device_devEui + '_' + dp.type,
                    "data_point": dp.type,
                    "device_name": instance.device_name,
                    "device_id": instance.device_devEui,
                    "table_id": dp.table_id,
                    "topic": "v3/"+instance.app_id+"@ttn/devices/#",  
                    "data_point_type": "float",
                    "measurement_type": "float",
                    "description": "this is a ..."
                }

                key = value["data_point_name"]
                value = json.dumps(value)
                redis_instance.set(key, value)
                response = {
                    'msg': f"{key} successfully set to {instance.device_devEui}"
                }
                print("Redis: ", response)