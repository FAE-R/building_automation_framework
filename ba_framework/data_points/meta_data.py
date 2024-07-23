import redis
from agents.models import Datapoint
import json
from django.core.management import call_command


def MetaData_fill():

    redis_instance = redis.StrictRedis(
        host="redis", port=6379, db=0, charset="utf-8", decode_responses=True)

    ####### get data from database (postgresql) #####

    DPs = Datapoint.objects.all()

    ####### save data point name as a dict in redis #####

    for dp in DPs:


        value = {
            "data_point_name": dp.device.device_devEui + '_' + dp.type,
            "data_point": dp.type,
            "device_name": dp.device.device_name,
            "device_id": dp.device.device_devEui,
            "table_id": dp.table_id,
            "topic": "v3/"+ dp.device.app_id+"@ttn/devices/#",  
            "data_point_type": "float",
            "measurement_type": "float",
            "description": "this is a ..."
        }


        ####### save device id as a dict in redis #####


        key = value["data_point_name"] # add data point name
        value = json.dumps(value)
        redis_instance.set(key, value)
        response = {
            'msg': f"{key} successfully set to {dp.device.device_devEui}"
        }
        print("Redis: ", response)

        print(dp.table_id, ": table MetaData filled with a new entry ...")


    call_command('makemigrations', 'logger', interactive=False)
    call_command('migrate', interactive=False)
            

    print("Meta data tables ready ...")
