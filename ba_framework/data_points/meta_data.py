import pandas as pd
import redis
from logger.models import MetaData
from agents.models import Vicki_Thermostat
import glob
import os
import json


def MetaData_fill():

    redis_instance = redis.StrictRedis(
        host="redis", port=6379, db=0, charset="utf-8", decode_responses=True)

    all_files = glob.glob(os.path.join("./data_points/", "*.pkl"))

    data_point_lists = []

    for filename in all_files:
        data_frame = pd.read_pickle(filename)
        data_point_lists.append(data_frame)

    df = pd.concat(data_point_lists, ignore_index=True)

    length, columnes = df.shape

    for i in range(length):

        ####### save data point name as a dict in redis #####

        key = df.data_point_name[i]

        value = {
            "device_name": df.device_name[i],
            "device_id": df.device_id[i],
            "table_id": df.table_id[i],
            "topic": df.topic[i],
            "data_point_type": df.data_point_type[i],
            "measurement_type": df.measurement_type[i],
            "description": df.description[i]
        }

        value = json.dumps(value)

        redis_instance.set(key, value)
        response = {
            'msg': f"{key} successfully set to {df.table_id[i]}"
        }
        print("Redis: ", response)

        ####### save device id as a dict in redis #####

        key = df.device_id[i]

        redis_instance.set(key, df.device_name[i])

        ####### save meta data in the database (postgresql) #####

        p, created = MetaData.objects.get_or_create(
            device_name=df.device_name[i],
            device_id=df.device_id[i],
            table_id=df.table_id[i],
            topic=df.topic[i],
            data_point_name=df.data_point_name[i],
            data_point_type=df.data_point_type[i],
            measurement_type=df.measurement_type[i],
            description=df.description[i]
        )

        if created:
            print(df.table_id[i],
                  ": table MetaData filled with a new entry ...")
            

    print("Meta data tables ready ...")
