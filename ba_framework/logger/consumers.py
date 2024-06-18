from datetime import datetime
from django.utils import timezone
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.apps import apps
import pytz
# https://docs.djangoproject.com/en/4.1/topics/email/
from django.core.mail import send_mail


class MqttConsumer(AsyncConsumer):
    async def mqtt_sub(self, event):
        try:
            payload = event['text']['payload']
            await self.get_table(payload)
        except Exception as inst:
            print("error during saving data values")
            print("Exception: ", inst)

    @database_sync_to_async
    def get_table(self, payload):
        table = payload["table_id"]
        try:
            Metric = apps.get_model('logger', table)
            metric = Metric()
            metric.value = float(payload["value"])
            time = datetime.strptime(
                payload["timestamp"], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
            metric.time = time.astimezone(pytz.timezone(
                timezone.get_current_timezone_name()))
            metric.save()
        except Exception as e:
            print("Error during saving data!")
            print("Exception:", e)

    async def mqtt_pub(self, event):
        pass


