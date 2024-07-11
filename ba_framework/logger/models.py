from django.db import models
from timescale.db.models.models import TimescaleModel
import redis
import json
# Create your models here.

redis_instance = redis.StrictRedis(
    host="redis", port=6379, db=0, charset="utf-8", decode_responses=True)

keys = redis_instance.keys("eui-*")

for key in keys:
    dp = json.loads(redis_instance.get(key))

    if dp["table_id"] is not None and dp["table_id"] != "":
        try:
            attrs = {
                'value': models.FloatField(),
                '__module__': 'logger.models'
            }
            type(str(dp["table_id"]), (TimescaleModel,), attrs)
        except:
            print("Error during creating table {} for sensor {}".format(dp["table_id"], dp["device_id"]))


