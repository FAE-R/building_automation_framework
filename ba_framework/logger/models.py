from django.db import models
from timescale.db.models.models import TimescaleModel
import pandas as pd
import glob
import os

# Create your models here.

class MetaData(models.Model):
    device_name = models.CharField(max_length=100, default="Unknown")
    device_id = models.CharField(max_length=100, default=0)
    table_id = models.CharField(max_length=100, default="Metric")
    topic = models.CharField(max_length=200, default="Unknown")
    data_point_name = models.TextField(default="Unknown")
    data_point_type = models.CharField(max_length=100, default="float")
    measurement_type = models.CharField(max_length=100, default="Unknown")
    description = models.TextField(default="This is a data point for ...")

    def __str__(self):
        return self.topic + " -- " + self.table_id



all_files = glob.glob(os.path.join("./data_points/" , "*.pkl"))

data_point_lists = []

for filename in all_files:
    data_frame = pd.read_pickle(filename)
    data_point_lists.append(data_frame)


df = pd.concat(data_point_lists, ignore_index=True)


length, columnes = df.shape

for i in range(length):
    attrs = {
        'value': models.FloatField(),
        '__module__': 'logger.models'
    }
    type(str(df.table_id[i]), (TimescaleModel,), attrs)