import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import asyncio
import json
from datetime import datetime
from mqtt_lib import MQTTv5, MQTTv3
from channels.layers import get_channel_layer
import redis
import xmltodict
from mqtt_client_logger import logger_conf
from sensor_lib import SensorLib

load_dotenv()  

redis_instance = redis.StrictRedis(
    host="redis", port=6379, db=0, charset="utf-8", decode_responses=True)

logger = logger_conf(__name__)

async def mqtt_send(future, channel_layer, channel, event):
    result = await channel_layer.send(channel, event)
    future.set_result(result)

client_1 = {
    "client_name": "client_1",
    "username": os.getenv('CLIENT_1_USERNAME'),
    "password": os.getenv('CLIENT_1_PASSWORD'),
    "host": os.getenv('CLIENT_HOST'),
    "port": int(os.getenv('CLIENT_PORT')),
    "topics_subscription": [
        os.getenv('CLIENT_1_TOPICS')
    ],
    "mqtt_version": 3
}

clients = [
    MQTTv3(client_1)
]

class Server:
    def __init__(self, channel, clients):
        self.channel = channel
        self.mqtt_channel_name = "mqtt"
        self.mqtt_channel_sub = "mqtt_sub"
        self.client_1 = clients[0]

        self.client_1.client.on_message = self._on_message_v3

    def _on_message_v3(self, client, userdata, message):
        try:
            device_id = json.loads(message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']
            attr_value = json.loads(message.payload.decode(
                "utf-8", "ignore"))["uplink_message"]["decoded_payload"]
            time = json.loads(message.payload.decode(
                "utf-8", "ignore"))["received_at"].split(".")[0]

            timestamp = datetime.strptime(
                time, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

            decoded_messages = []

            keys = redis_instance.keys(device_id+"*")

            for key in keys:
                dp = json.loads(redis_instance.get(key))
                if dp["data_point"] in attr_value.keys():
                    dec_msg = {}
                    dec_msg["table_id"] = str(dp["table_id"])
                    dec_msg["timestamp"] = timestamp
                    dec_msg["value"] = attr_value[dp["data_point"]]
                    decoded_messages.append(dec_msg)
                else:
                    print("Parameter does not exist in payload")
            print("new sensor data: ", decoded_messages)
            for key in decoded_messages:
                table = key["table_id"]
                if table is not None:
                    msg = {
                        "topic": message.topic,
                        "payload": key,
                        "qos": message.qos,
                        "host": userdata["host"],
                        "port": userdata["port"],
                    }

                    self._asyncio_send(
                        self.channel, self.mqtt_channel_name, self.mqtt_channel_sub, msg)
                else:
                    print('data logging error for topic {} and this client {}'.format(
                        message.topic, userdata["host"]))
                    logger.error('data logging error for topic {} and this client {}'.format(
                        message.topic, userdata["host"]))

        except:
            print('Data from TTN not valid ...')

    def _asyncio_send(self, channel, mqtt_channel_name, mqtt_channel_sub, msg):
        try:
            future = asyncio.Future()
            asyncio.ensure_future(mqtt_send(future, channel, mqtt_channel_name, {
                                  "type": mqtt_channel_sub, "text": msg}))

        except Exception as e:
            print("Cannot send message ...")
            logger.error("Cannot send message {}".format(msg))
            logger.exception(e)

    async def client_1_start(self):
        self.client_1.client.connect(
            host=self.client_1.host,
            port=self.client_1.port,
            keepalive=60,
            bind_address="",
            bind_port=0,
            clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
            properties=None)

        await asyncio.sleep(5)
        while True:
            self.client_1.client.loop(0.1)
            await asyncio.sleep(0.01)
            if not self.client_1.client.connected_flag:
                self.client_1.client.disconnect()
                await asyncio.sleep(5)
                print("client reconnecting ...")
                logger.error("client reconnecting for {} ... ".format(
                    self.client_1.host))
                try:
                    self.client_1.client.connect(
                        host=self.client_1.host,
                        port=self.client_1.port,
                        keepalive=60,
                        bind_address="",
                        bind_port=0,
                        clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                        properties=None
                    )
                    await asyncio.sleep(5)
                except:
                    print("reconnection failed")
                    logger.error("reconnection for {} failed".format(
                        self.client_1.host))

    def run(self):
        loop = asyncio.get_event_loop()
        self.loop = loop

        print("Event loop for mqtt clients running forever ...")
        logger.info("Event loop for mqtt clients running forever ...")

        asyncio.ensure_future(self.client_1_start())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            print("Mqtt client disconnected ... loop exited")
            logger.debug("Mqtt client disconnected ... loop exited")
            loop.close()

        self.client_1.disconnect()

channel_layer = get_channel_layer()
client_server = Server(channel_layer, clients)
client_server.run()
