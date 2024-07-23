from django.utils import timezone
from datetime import timedelta
from django.apps import apps
from .models import Room, Device, Datapoint
import pandas as pd
from pycaret.classification import load_model
import os

# Get the directory of the current file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the model file
model_path = os.path.join(current_directory, 'calibrated_rf_model.pkl')

# Print the current working directory and model path
print("Current working directory:", os.getcwd())
print("Model path:", model_path)

# Load the calibrated model using the correct path
calibrated_rf_model = load_model(model_path)

def fetch_data(room: Room) -> dict:
    print("Fetching data...")
    """
    Fetch data from the database and Redis for the given room for the last hour.
    
    input parameters:
        - room: django room object

    output:
        - dict
        {
            "co2": [],
            "door": [],
            "motion": []
        }
    """

    data = {
        'co2': [],
        'door': [],
        'motion': [],
        'occupancy': []
    }

    if room is not None:
        sensors = {
            'co2': {
                'device_type': 'elsys-ers-co2',
                'datapoint_type': 'co2'
            },
            'door': {
                'device_type': 'tab-elsys-ers',
                'datapoint_type': 'digital'
            },
            'motion': {
                'device_type': 'elsys-ers-co2',
                'datapoint_type': 'motion'
            },
            'occupancy': {
                'device_type': 'elsys-ers-eye',
                'datapoint_type': 'occupancy'
            }
        }
        
        for sensor, info in sensors.items():
            try:
                device = Device.objects.get(room=room, type=info['device_type'])

                print(f"Device for {sensor}: {device}")
                
                dp = Datapoint.objects.get(device=device, type=info['datapoint_type'])

                print(f"Datapoint for {sensor}: {dp}")
                
                table_id = dp.table_id
                
                table = apps.get_model("logger", str(table_id))
                print(f"Table for {sensor}: {table}")
                
                if table is not None:
                    now = timezone.now()
                    one_hour_ago = now - timedelta(hours=1)
                    
                    datapoints = table.objects.filter(time__range=(one_hour_ago, now))
                    print(f"Datapoints for {sensor}: {datapoints}")
                    
                    if sensor == 'co2':
                        df_co2 = pd.DataFrame(list(datapoints.values('time', 'value')))
                        
                        # Feature Engineering
                        df_co2.set_index('time', inplace=True)
                        df_co2 = df_co2.resample('10T').mean().interpolate(method='nearest')  # Resample to 10-minute intervals

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

                        df_co2["co2"] = df_co2["value"]
                        df_co2 = df_co2[['co2', 'co2_10m_dif1', 'co2_10m_dif2', 'co2_10m_dif4', 'co2_10m_dif6', 'co2_10m_mean_last_4']]
                        
                        # Prediction using the calibrated model
                        pred_unseen_rf = calibrated_rf_model.predict(df_co2)
                        data['co2'] = pred_unseen_rf.tolist()
                    else:
                        for point in datapoints:
                            data[sensor].append(point.value)
                
            except Device.DoesNotExist:
                print(f"Device of type '{info['device_type']}' not found in the specified room.")
            except Datapoint.DoesNotExist:
                print(f"Datapoint of type '{info['datapoint_type']}' not found for the specified device.")
            except Exception as e:
                print(f"An error occurred while processing {sensor}: {e}")

    return data
