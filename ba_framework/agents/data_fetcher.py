from django.utils import timezone
from datetime import timedelta
from django.apps import apps
from .models import Room, Device, Datapoint

def fetch_data(room: Room) -> dict:
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

    # Initialize the data dictionary
    data = {
        'co2': [],
        'door': [],
        'motion': []
    }

    if room is not None:
        try:
            device = Device.objects.get(room=room, type="elsys-ers-co2")
            
            dp = Datapoint.objects.get(device=device, type="co2")
            
            table_id = dp.table_id
            
            table = apps.get_model("logger", str(table_id))
            
            if table is not None:
                now = timezone.now()
                one_hour_ago = now - timedelta(hours=1)
                
                datapoints = table.objects.filter(time__range=(one_hour_ago, now))
                
                for point in datapoints:
                    data['co2'].append(point.value)  
                
        except Device.DoesNotExist:
            print("Device of type 'elsys-ers-co2' not found in the specified room.")
        except Datapoint.DoesNotExist:
            print("Datapoint of type 'co2' not found for the specified device.")
        except Exception as e:
            print(f"An error occurred: {e}")

    return data
