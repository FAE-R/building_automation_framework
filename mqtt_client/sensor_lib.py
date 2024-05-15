import redis
import json
from datetime import datetime
from mqtt_client_logger import logger_conf
from datetime import datetime, timedelta
import pytz
import xmltodict

logger = logger_conf(__name__)


redis_instance = redis.StrictRedis(
    host="redis", port=6379, db=0, charset="utf-8", decode_responses=True)


class SensorLib:
    def __init__(self, device_name, message):
        self.device_name = device_name
        self.message = message

    def parse(self):
        """
        payload_message:
            data = {
                "decoded_messages": [
                    {
                        "decoded_msg": {
                            "value": <current measurment>,
                            "timestamp": <UTC timestamp in this format "'%Y-%m-%dT%H:%M:%S'">,
                            "table_id": <table_id>
                        }
                    },
                    {
                        ...
                    }
                ]
            } 
        """
        data = {}
        decoded_messages = []

        if self.device_name == "enginko-mcf-lw12ter":

            device_id = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            # timestamp = pytz.timezone("Europe/Berlin").localize(datetime.strptime(attr_value.pop(
            #     'date'), '%m/%d/%Y, %H:%M:%S')).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S')
            # timestamp1 = pytz.timezone("Europe/Berlin").localize(datetime.strptime(attr_value.pop(
            #     'date_1'), '%m/%d/%Y, %H:%M:%S')).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S')
            # timestamp2 = pytz.timezone("Europe/Berlin").localize(datetime.strptime(attr_value.pop(
            #     'date_2'), '%m/%d/%Y, %H:%M:%S')).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S')

            time_dt = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
            timestamp2 = time_dt.strftime('%Y-%m-%dT%H:%M:%S')
            timestamp1 = (time_dt - timedelta(minutes=10)
                          ).strftime('%Y-%m-%dT%H:%M:%S')
            timestamp = (time_dt - timedelta(minutes=20)
                         ).strftime('%Y-%m-%dT%H:%M:%S')

            ### battery ###
            dec_msg = {}
            data_point_name = device_id + "_battery"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp2
            dec_msg["value"] = attr_value["battery"]
            decoded_messages.append(dec_msg)

            ### humidity ###
            dec_msg = {}
            data_point_name = device_id + "_humidity"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["humidity"]
            decoded_messages.append(dec_msg)

            ### humidity_1 ###
            dec_msg = {}
            data_point_name = device_id + "_humidity"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["humidity_1"]
            decoded_messages.append(dec_msg)

            ### humidity_2 ###
            dec_msg = {}
            data_point_name = device_id + "_humidity"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp2
            dec_msg["value"] = attr_value["humidity_2"]
            decoded_messages.append(dec_msg)

            ### temperature ###
            dec_msg = {}
            data_point_name = device_id + "_temperature"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["temperature"]
            decoded_messages.append(dec_msg)

            ### temperature_1 ###
            dec_msg = {}
            data_point_name = device_id + "_temperature"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["temperature_1"]
            decoded_messages.append(dec_msg)

            ### temperature_2 ###
            dec_msg = {}
            data_point_name = device_id + "_temperature"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp2
            dec_msg["value"] = attr_value["temperature_2"]
            decoded_messages.append(dec_msg)

            ### pressure ###
            dec_msg = {}
            data_point_name = device_id + "_pressure"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["pressure"]
            decoded_messages.append(dec_msg)

            ### pressure_1 ###
            dec_msg = {}
            data_point_name = device_id + "_pressure"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["pressure_1"]
            decoded_messages.append(dec_msg)

            ### pressure_2 ###
            dec_msg = {}
            data_point_name = device_id + "_pressure"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp2
            dec_msg["value"] = attr_value["pressure_2"]
            decoded_messages.append(dec_msg)

            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "enginko-mcf-lw12co2":

            device_id = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            # timestamp = pytz.timezone("Europe/Berlin").localize(datetime.strptime(attr_value.pop(
            #     'date'), '%m/%d/%Y, %H:%M:%S')).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S')
            # timestamp1 = pytz.timezone("Europe/Berlin").localize(datetime.strptime(attr_value.pop(
            #     'date_1'), '%m/%d/%Y, %H:%M:%S')).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S')

            time_dt = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
            timestamp1 = time_dt.strftime('%Y-%m-%dT%H:%M:%S')
            timestamp = (time_dt - timedelta(minutes=10)
                         ).strftime('%Y-%m-%dT%H:%M:%S')

            ### battery ###
            dec_msg = {}
            data_point_name = device_id + "_battery"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["battery"]
            decoded_messages.append(dec_msg)

            ### co2 ###
            dec_msg = {}
            data_point_name = device_id + "_co2"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["co2"]
            decoded_messages.append(dec_msg)

            ### co2_1 ###
            dec_msg = {}
            data_point_name = device_id + "_co2"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["co2_1"]
            decoded_messages.append(dec_msg)

            ### humidity ###
            dec_msg = {}
            data_point_name = device_id + "_humidity"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["humidity"]
            decoded_messages.append(dec_msg)

            ### humidity_1 ###
            dec_msg = {}
            data_point_name = device_id + "_humidity"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["humidity_1"]
            decoded_messages.append(dec_msg)

            ### lux ###
            dec_msg = {}
            data_point_name = device_id + "_lux"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["lux"]
            decoded_messages.append(dec_msg)

            ### lux_1 ###
            dec_msg = {}
            data_point_name = device_id + "_lux"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["lux_1"]
            decoded_messages.append(dec_msg)

            ### pressure ###
            dec_msg = {}
            data_point_name = device_id + "_pressure"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["pressure"]
            decoded_messages.append(dec_msg)

            ### pressure_1 ###
            dec_msg = {}
            data_point_name = device_id + "_pressure"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["pressure_1"]
            decoded_messages.append(dec_msg)

            ### temperature ###
            dec_msg = {}
            data_point_name = device_id + "_temperature"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["temperature"]
            decoded_messages.append(dec_msg)

            ### temperature_1 ###
            dec_msg = {}
            data_point_name = device_id + "_temperature"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["temperature_1"]
            decoded_messages.append(dec_msg)

            ### voc ###
            dec_msg = {}
            data_point_name = device_id + "_voc"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["voc"]
            decoded_messages.append(dec_msg)

            ### voc_1 ###
            dec_msg = {}
            data_point_name = device_id + "_voc"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp1
            dec_msg["value"] = attr_value["voc_1"]
            decoded_messages.append(dec_msg)

            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "tab-browan-tbdw100":

            device_id = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            timestamp = datetime.strptime(
                time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

            ### status ###
            dec_msg = {}
            data_point_name = device_id + "_status"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["status"]
            decoded_messages.append(dec_msg)
            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "tab-milesight-ws301":

            device_id = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            timestamp = datetime.strptime(
                time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

            ### status ###
            dec_msg = {}
            data_point_name = device_id + "_status"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            if attr_value["state"] == "close":
                dec_msg["value"] = 0
            elif attr_value["state"] == "open":
                dec_msg["value"] = 1
            else:
                dec_msg["value"] = 999
            decoded_messages.append(dec_msg)
            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "tab-dragino-lds02":

            device_id = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            timestamp = datetime.strptime(
                time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

            ### status ###
            dec_msg = {}
            data_point_name = device_id + "_status"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["status"]
            decoded_messages.append(dec_msg)
            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "innotas_hkv":

            device_id = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            timestamp = datetime.strptime(
                time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

            ### 2h value ###
            dec_msg = {}
            data_point_name = device_id + "_value"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["value"]
            decoded_messages.append(dec_msg)

            ### daily value ###
            if attr_value["day_value"] != "":
                dec_msg = {}
                data_point_name = device_id + "_day_value"
                dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                    "table_id"]
                dec_msg["timestamp"] = timestamp
                dec_msg["value"] = attr_value["day_value"]
                decoded_messages.append(dec_msg)

            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "shellytrv":
            device_id = self.message['fw_info']['device']

            timestamp = datetime.utcfromtimestamp(
                int(self.message['unixtime'])).strftime("%Y-%m-%dT%H:%M:%S")

            ### pos ###
            dec_msg = {}
            data_point_name = device_id + "_pos"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = self.message['thermostats'][0]['pos']
            decoded_messages.append(dec_msg)

            ### target_t ###
            dec_msg = {}
            data_point_name = device_id + "_target_t"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = self.message['thermostats'][0]['target_t']['value']
            decoded_messages.append(dec_msg)

            ### tmp ###
            dec_msg = {}
            data_point_name = device_id + "_tmp_value"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = self.message['thermostats'][0]['tmp']['value']
            decoded_messages.append(dec_msg)

            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "PolluTherm":
            device_id = "WMZ"

            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

            try:
                message_ = json.loads((json.dumps(xmltodict.parse(
                    self.message.payload.decode("iso-8859-1").split("data")[1][3:-4]))))["MBusData"]
            except:
                c = """aneous value</Function>
                        <StorageNumber>0</StorageNumber>
                        <Unit>Temperature Difference (m deg C)</Unit>
                        <Value>99999</Value>
                        <Timestamp>2023-08-07T10:10:10Z</Timestamp>
                    </DataRecord>
                </MBusData>
                '}]"""
                text = self.message.payload.decode("iso-8859-1") + c
                message_ = json.loads((json.dumps(xmltodict.parse(
                    text.split("data")[1][3:-4]))))["MBusData"]

            # SlaveInformation = message["SlaveInformation"]

            DataRecord = message_["DataRecord"]
            for i in DataRecord:
                dec_msg = {}
                if i["Unit"] == "Energy (10 kWh)":
                    ### total heat consumption [kW] ###
                    dec_msg = {}
                    dec_msg["table_id"] = "TotalHeatConsumption"
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = 10*float(i["Value"])
                    decoded_messages.append(dec_msg)

                if i["Unit"] == "Volume (1e-2  m^3)":
                    ### TotalWaterVolumeFlow [m3] ###
                    dec_msg = {}
                    dec_msg["table_id"] = "TotalWaterVolumeFlow"
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = float(i["Value"])/100
                    decoded_messages.append(dec_msg)

                if i["Unit"] == "Volume flow (1e-2  m^3/h)":
                    ### current water flow [m3/h] ###
                    dec_msg = {}
                    dec_msg["table_id"] = "VolumeFlow"
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = float(i["Value"])/100
                    decoded_messages.append(dec_msg)

                if i["Unit"] == "Power (10 W)":
                    ### current heat power [w] ###
                    dec_msg = {}
                    dec_msg["table_id"] = "TotalHeatPower"
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = 10*float(i["Value"])
                    decoded_messages.append(dec_msg)

                if i["Unit"] == "Flow temperature (1e-1 deg C)":
                    ### current heat power [°C] ###
                    dec_msg = {}
                    dec_msg["table_id"] = "FlowTemperature"
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = float(i["Value"])/10
                    decoded_messages.append(dec_msg)
                if i["Unit"] == "Return temperature (1e-1 deg C)":
                    ### current heat power [°C] ###
                    dec_msg = {}
                    dec_msg["table_id"] = "ReturnTemperature"
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = float(i["Value"])/10
                    decoded_messages.append(dec_msg)
                if i["Unit"] == "Temperature Difference (m deg C)":
                    ### current heat power [°C] ###
                    dec_msg = {}
                    dec_msg["table_id"] = "DiffTemperature"
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = float(i["Value"])/1000
                    decoded_messages.append(dec_msg)

            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "elsys-ers-co2-lite":

            device_id = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(self.message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            timestamp = datetime.strptime(
                time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

            ### co2 ###
            dec_msg = {}
            data_point_name = device_id + "_co2"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["co2"]
            decoded_messages.append(dec_msg)

            ### humidity ###
            dec_msg = {}
            data_point_name = device_id + "_humidity"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["humidity"]
            decoded_messages.append(dec_msg)

            ### light ###
            dec_msg = {}
            data_point_name = device_id + "_light"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["light"]
            decoded_messages.append(dec_msg)

            ### motion ###
            dec_msg = {}
            data_point_name = device_id + "_motion"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["motion"]
            decoded_messages.append(dec_msg)

            ### temperature ###
            dec_msg = {}
            data_point_name = device_id + "_temperature"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["temperature"]
            decoded_messages.append(dec_msg)

            ### vdd ###
            dec_msg = {}
            data_point_name = device_id + "_vdd"
            dec_msg["table_id"] = json.loads(redis_instance.get(data_point_name))[
                "table_id"]
            dec_msg["timestamp"] = timestamp
            dec_msg["value"] = attr_value["vdd"]
            decoded_messages.append(dec_msg)

            data["decoded_messages"] = decoded_messages
            return data

        elif self.device_name == "elsys-ers-eye":
            try:
                device_id = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))['end_device_ids']['device_id']
                attr_value = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
                time = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["received_at"].split(".")[0]

                timestamp = datetime.strptime(
                    time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

                param_names = ["occupancy", "humidity",
                               "light", "motion", "temperature", "vdd"]

                for param in param_names:
                    if param in attr_value:  # check if the parameter exists in the payload
                        dec_msg = {}
                        data_point_name = device_id + "_" + param
                        dec_msg["table_id"] = json.loads(
                            redis_instance.get(data_point_name))["table_id"]
                        dec_msg["timestamp"] = timestamp
                        dec_msg["value"] = attr_value[param]
                        decoded_messages.append(dec_msg)

                data["decoded_messages"] = decoded_messages
                return data
            except Exception as e:
                print(f"An error occurred: {e}")

        elif self.device_name == "tab-elsys-ers":
            try:
                device_id = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))['end_device_ids']['device_id']
                attr_value = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
                time = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["received_at"].split(".")[0]

                timestamp = datetime.strptime(
                    time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

                param_names = ["accMotion", "digital",
                               "pulseAbs", "vdd", "x", "y", "z"]

                for param in param_names:
                    if param in attr_value:  # check if the parameter exists in the payload
                        dec_msg = {}
                        data_point_name = device_id + "_" + param
                        dec_msg["table_id"] = json.loads(
                            redis_instance.get(data_point_name))["table_id"]
                        dec_msg["timestamp"] = timestamp

                        # If the parameter is "digital", reverse its value
                        if param == "digital":
                            dec_msg["value"] = 1 if attr_value[param] == 0 else 0
                        else:
                            dec_msg["value"] = attr_value[param]

                        decoded_messages.append(dec_msg)

                data["decoded_messages"] = decoded_messages
                return data
            except Exception as e:
                print(f"An error occurred: {e}")

        elif self.device_name == "thermostat-lorawan-vicky":

            try:
                device_id = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))['end_device_ids']['device_id']
                attr_value = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
                time = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["received_at"].split(".")[0]

                timestamp = datetime.strptime(
                    time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

                param_names = ["batteryVoltage","childLock","motorPosition", "motorRange", "sensorTemperature", "targetTemperature", "operationalMode"]

                for param in param_names:
                    if param in attr_value:  # check if the parameter exists in the payload
                        dec_msg = {}
                        data_point_name = device_id + "_" + param
                        dec_msg["table_id"] = json.loads(
                            redis_instance.get(data_point_name))["table_id"]
                        dec_msg["timestamp"] = timestamp
                        dec_msg["value"] = attr_value[param]
                        decoded_messages.append(dec_msg)

                data["decoded_messages"] = decoded_messages
                return data
            except Exception as e:
                print(f"An error occurred: {e}")

        elif self.device_name == "room-button":
            try:
                device_id = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))['end_device_ids']['device_id']
                attr_value = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
                time = json.loads(self.message.payload.decode(
                    "utf-8", "ignore"))["received_at"].split(".")[0]

                timestamp = datetime.strptime(
                    time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

                param_names = ["buttons", "buttons_first",
                               "count", "type", "uah"]

                for param in param_names:
                    if param in attr_value:  # check if the parameter exists in the payload
                        dec_msg = {}
                        data_point_name = device_id + "_" + param
                        dec_msg["table_id"] = json.loads(
                            redis_instance.get(data_point_name))["table_id"]
                        dec_msg["timestamp"] = timestamp
                        dec_msg["value"] = attr_value[param]
                        decoded_messages.append(dec_msg)
                    else:
                        print(f"Parameter {param} does not exist in payload")

                data["decoded_messages"] = decoded_messages
                return data
            except Exception as e:
                print(f"An error occurred: {e}")
