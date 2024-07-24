from django.utils import timezone
from datetime import timedelta
from django.apps import apps
from .models import Room, Device, Datapoint
import pandas as pd
from pycaret.classification import load_model
import os


# Load the calibrated model using the correct path
calibrated_rf_model = load_model('./agents/calibrated_rf_model')

def v1(room: Room) -> dict:
    print("Fetching data...")
    output = {
        "error": "",
        "last_occupancy": "",
        "result": 0,
        "detected_by": []
    }

    if room is None:
        output["error"] = "Room object is none"
        return output

    # Check room's current occupancy status
    if room.occupied is not None:
        output["last_occupancy"] = int(room.occupied)
        print(f"Room occupied: {room.occupied}")
    else:
        output["last_occupancy"] = -1
        print("Room occupancy unknown")

    sensors = {
        'co2': 'elsys-ers-co2',
        'door': 'tab-elsys-ers',
        'motion': 'elsys-ers-co2',
        'IR': 'elsys-ers-eye'
    }

    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    try:
        for sensor_type, device_type in sensors.items():
            device = Device.objects.filter(room=room, type=device_type).first()
            if device is None:
                print(f"Device of type '{device_type}' not found in the specified room.")
                continue

            datapoints = Datapoint.objects.filter(device=device, type=sensor_type)
            if not datapoints.exists():
                print(f"Datapoint of type '{sensor_type}' not found for the specified device.")
                continue

            datapoint_table = apps.get_model("logger", str(datapoints.first().table_id))

            if sensor_type == 'co2':
                data_points = datapoint_table.objects.filter(time__range=(one_hour_ago, now)).order_by('-time')
                if data_points.count() >= 6:
                    df_co2 = pd.DataFrame(list(data_points.values('time', 'value')))
                    df_co2.set_index('time', inplace=True)
                    df_co2 = df_co2.resample('10T').mean().interpolate(method='nearest')
                    df_co2['co2_10m_mean_last_4'] = df_co2['value'].rolling(window=4).mean()
                    df_co2["co2_10m_dif1"] = df_co2["value"].diff()
                    df_co2["co2_10m_dif2"] = df_co2["value"].diff(periods=2)
                    df_co2["co2_10m_dif4"] = df_co2["value"].diff(periods=4)
                    df_co2["co2_10m_dif6"] = df_co2["value"].diff(periods=6)
                    df_co2['co2_10m_mean_last_4'].fillna(method='ffill', inplace=True)
                    df_co2['co2_10m_dif1'].fillna(method='ffill', inplace=True)
                    df_co2['co2_10m_dif2'].fillna(method='ffill', inplace=True)
                    df_co2['co2_10m_dif4'].fillna(method='ffill', inplace=True)
                    df_co2['co2_10m_dif6'].fillna(method='ffill', inplace=True)
                    df_co2 = df_co2[['co2_10m_dif1', 'co2_10m_dif2', 'co2_10m_dif4', 'co2_10m_dif6', 'co2_10m_mean_last_4']]
                    pred_unseen_rf = calibrated_rf_model.predict(df_co2)
                    if any(pred == 1 for pred in pred_unseen_rf):  
                        output["result"] = 1
                        output["detected_by"].append("CO2")

            else:
                data_points = datapoint_table.objects.filter(time__range=(one_hour_ago, now)).order_by('-time')

                if sensor_type == 'motion' and any(d.value > 0 for d in data_points):
                    output["result"] = 1
                    output["detected_by"].append("motion")

                elif sensor_type == 'IR' and any(d.value > 0 for d in data_points):
                    output["result"] = 1
                    output["detected_by"].append("IR")

                elif sensor_type == 'door' and data_points.count() > 1:
                    if data_points.first().value != data_points.last().value:
                        output["result"] = 1
                        output["detected_by"].append("door")

    except Exception as e:
        output["error"] = f"An error occurred: {e}"
        return output

    # Update room occupancy status
    if output["result"] == 1:
        if room.occupied != True:
            room.occupied = True
            room.save()
    elif output["result"] == 0:
        if room.occupied != False:
            room.occupied = False
            room.save()
    else:
        if room.occupied is not None:
            room.occupied = None
            room.save()

    return output
