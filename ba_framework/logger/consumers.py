# Importing datetime module for handling date and time.
from datetime import datetime

# Importing timezone utilities from Django to work with time zones.
from django.utils import timezone

# Importing AsyncConsumer from channels.consumer to create an asynchronous consumer.
from channels.consumer import AsyncConsumer

# Importing database_sync_to_async from channels.db to run synchronous database code in an asynchronous context.
from channels.db import database_sync_to_async

# Importing apps from Django to dynamically load models.
from django.apps import apps

# Importing pytz to handle different time zones.
import pytz

# Importing send_mail from Django's core mail module for sending emails.
# Documentation: https://docs.djangoproject.com/en/4.1/topics/email/
from django.core.mail import send_mail


# Defining MqttConsumer class which inherits from AsyncConsumer to handle asynchronous WebSocket connections.
class MqttConsumer(AsyncConsumer):
    # Asynchronous method to handle MQTT subscription events.
    async def mqtt_sub(self, event):
        try:
            # Extracting the payload from the event data.
            payload = event['text']['payload']
            
            # Calling the get_table method to process the payload.
            await self.get_table(payload)
        except Exception as inst:
            # Handling exceptions that occur during the processing of the event.
            print("error during saving data values")
            print("Exception: ", inst)

    # Synchronous method to get the table and save the payload data to the database.
    # This method is wrapped with database_sync_to_async to allow it to be called in an async context.
    @database_sync_to_async
    def get_table(self, payload):
        # Extracting the table ID from the payload.
        table = payload["table_id"]
        try:
            # Dynamically getting the model using the table ID.
            Metric = apps.get_model('logger', table)
            metric = Metric()
            
            # Setting the value of the metric from the payload.
            metric.value = float(payload["value"])
            
            # Parsing and setting the timestamp from the payload.
            time = datetime.strptime(payload["timestamp"], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
            metric.time = time.astimezone(pytz.timezone(timezone.get_current_timezone_name()))
            
            # Saving the metric instance to the database.
            metric.save()
        except Exception as e:
            # Handling exceptions that occur during the saving of data.
            print("Error during saving data!")
            print("Exception:", e)

    # Placeholder for the asynchronous method to handle MQTT publication events.
    async def mqtt_pub(self, event):
        pass
