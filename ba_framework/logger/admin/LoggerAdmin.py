from django.contrib import admin
from django.apps import apps
from logger.models import *
import pandas as pd
import glob
import os
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

# Register your models here.

class MetaDataAdmin(admin.ModelAdmin):
      pass
      


# class DPAdmin(admin.ModelAdmin):
#       pass

# all_files = glob.glob(os.path.join("/home/hitl_ba_framework/data_points/", "*.pkl"))

# data_point_lists = []

# for filename in all_files:
#     data_frame = pd.read_pickle(filename)
#     data_point_lists.append(data_frame)


# df = pd.concat(data_point_lists, ignore_index=True)

# length, columnes = df.shape

# for i in range(length):
#     admin.site.register(apps.get_model("logger", str(df.table_id[i])), MetaDataAdmin)

