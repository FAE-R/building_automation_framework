from agents.models import *
from logger.models import *
from django.apps import apps
from django.utils import timezone
from datetime import timedelta, datetime, date
import holidays

                            






# def Occupancy_Detection(room: object, current_state: int) -> dict:
#     """
#     check real time room occupancy

#     input parameters:
#         - room:             django room object
#         - current_state:    last occupancy status

#     room measurement:
#         - table_list.motion: list of all PIR sensors (Elsys CO2 & Elsys eye) in a room (comma separated)
#             - measured every 10 min.
#             - if == 0 -> no occupancy detected
#             - if > 0 -> occupancy detected or number of detection during last interval

#         - table_list.doors_counter: list of all door change status counters (Elsys EMS doors -> pulse abs) in a room (comma separated)
#             - measured every 10 min.
#             - Cumulative door status change counters (only close to open will be counted) 

#         - table_list.windows_counter: list of all window change status counters (Elsys EMS doors -> pulse abs) in a room (comma separated)
#             - measured every 10 min.
#             - cumulative door status change counters (only close to open will be counted)

#         - table_list.doors_open: list of all door tab sensors (Elsys EMS doors -> digital) in a room (comma separated)
#             - measured every 10 min. and after every status change
#             - if == 1 --> door is open
#             - if == 0 --> door is closed

#         - table_list.windows_open: list of all window tab sensors (Elsys EMS doors -> digital) in a room (comma separated)
#             - measured every 10 min. and after every status change
#             - if == 1 --> window is open
#             - if == 0 --> window is closed

#         - table_list.co2: CO2 sensor (Elsys CO2) in a room (comma separated)
#             - measured in ppm every 10 min.

#     output:
#         - dict
#         {
#             "error":"",
#             "last_occupancy":"",
#             "result":"",
#             "detected_by":["","",...]
#         }
#     """
#     output = {}


#     if room != None:
#         if room.occupied is not None:
#             if room.occupied:
#                 output["last_occupancy"] = 1
#                 print("Room occupied")
#             else:
#                 output["last_occupancy"] = 0
#                 print("Room not occupied")
#         else:
#             output["last_occupancy"] = -1
#             print("Room occupancy unkown")

#         table_list = Room_Monitoring_Sensors.objects.get(room=room)

#         ranges = (timezone.now() - timedelta(minutes=15), timezone.now())
#         ranges_door = (timezone.now() - timedelta(minutes=20), timezone.now())
#         ranges_co2 = (timezone.now() - timedelta(minutes=40), timezone.now())


#         if table_list is not None:
#             output["result"] = 0
#             detected_by = []

#             if table_list.motion != None:
#                 table_lists = table_list.motion.split(",")
#                 for table in table_lists:
#                     table = apps.get_model(
#                         'logger', table)
#                     value = table.timescale.filter(
#                         time__range=ranges).order_by('-id')
#                     if value.exists():
#                         for i in value:
#                             if i.value > 0:
#                                 output["result"] = 1
#                                 detected_by.append("motion")

#             if table_list.ir != None:
#                 table_lists = table_list.ir.split(",")
#                 for table in table_lists:
#                     table = apps.get_model(
#                         'logger', table)
#                     value = table.timescale.filter(
#                         time__range=ranges).order_by('-id')
#                     if value.exists():
#                         for i in value:
#                             if i.value > 0:
#                                 output["result"] = 1
#                                 detected_by.append("IR")

#             if table_list.co2 != None and Room_Monitoring_Datapoints.co2_threshold_lastday_10min != None:
#                 table = apps.get_model('logger', table_list.co2)
#                 value = table.timescale.filter(time__range=ranges_co2).order_by('-id')
#                 if value.exists():
#                     if len(value) >= 3:
#                         if value[0].value - value[1].value >= float(table_list.co2_threshold_lastday_10min) and value[1].value - value[2].value >= float(table_list.co2_threshold_lastday_10min):
#                             output["result"] = 1
#                             detected_by.append("CO2")
                        
#             if table_list.doors_counter != None:
#                 table_lists = table_list.doors_counter.split(",")
#                 for table in table_lists:
#                     table = apps.get_model(
#                         'logger', table)
#                     value = table.timescale.filter(
#                         time__range=ranges_door).order_by('-id')
#                     if value.exists():
#                         if len(value) >= 2:
#                             if value[0].value != value[len(value) - 1].value: # value[0] is the last value in the db
#                                 output["result"] = 1
#                                 detected_by.append("doors_counter")

#             if table_list.windows_counter != None:
#                 table_lists = table_list.windows_counter.split(",")
#                 for table in table_lists:
#                     table = apps.get_model(
#                         'logger', table)
#                     value = table.timescale.filter(
#                         time__range=ranges_door).order_by('-id')
#                     if value.exists():
#                         if len(value) >= 2:
#                             if value[0].value != value[len(value) - 1].value: # value[0] is the last value in the db
#                                 output["result"] = 1
#                                 detected_by.append("windows_counter")

#             if table_list.doors_open != None:
#                 table_lists = table_list.doors_open.split(",")
#                 for table in table_lists:
#                     table = apps.get_model(
#                         'logger', table)
#                     value = table.timescale.filter(
#                         time__range=ranges, value=1)
#                     if value.exists():
#                         output["result"] = 1
#                         detected_by.append("doors_open")

#             if table_list.windows_open != None:
#                     table_lists = table_list.windows_open.split(",")
#                     for table in table_lists:
#                         table = apps.get_model(
#                             'logger', table)
#                         value = table.timescale.filter(
#                             time__range=ranges, value=1)
#                         if value.exists():
#                             output["result"] = 1
#                             detected_by.append("windows_open")

#             if output["result"] == 1:
#                 if room.occupied != True:
#                     room.occupied = True
#                     room.save()
#                 output["detected_by"] = detected_by
#             elif output["result"] == 0:
#                 if room.occupied != False:
#                     room.occupied = False
#                     room.save()
#             else:
#                 if room.occupied is not None:
#                     room.occupied = None
#                     room.save()
            
#             return output
#         else:
#             output["error"] = "Room moitoring data point is none"
#             return output
#     else:
#         output["error"] = "Room object is none"
#         return output


