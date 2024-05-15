from django.contrib import admin
from agents.models import *




# Register your models here.

admin.site.register(Profile)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Room_Users)
admin.site.register(Room_Monitoring_Datapoints)
admin.site.register(Comfort_Feedback)
admin.site.register(Scheduler)
admin.site.register(Notification)
admin.site.register(Vicki_Thermostat)