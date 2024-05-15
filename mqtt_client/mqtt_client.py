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

redis_instance = redis.StrictRedis(
    host="redis", port=6379, db=0, charset="utf-8", decode_responses=True)

logger = logger_conf(__name__)


async def mqtt_send(future, channel_layer, channel, event):
    result = await channel_layer.send(channel, event)
    future.set_result(result)


client_1 = {
    "client_name": "client_1",
    "username": "<username>",
    "password": "<password>",
    "host": "eu1.cloud.thethings.network",
    "port": 1883,
    "topics_subscription": [
        "v3/<appID>@ttn/devices/#"
    ],
    "mqtt_version": 3
}


client_2 = {
    "client_name": "client_2",
    "username": "<username>",
    "password": "<password>",
    "host": "eu1.cloud.thethings.network",
    "port": 1883,
    "topics_subscription": [
        "v3/<appID>@ttn/devices/#"
    ],
    "mqtt_version": 3
}

client_3 = {
    "client_name": "client_3",
    "username": "<username>",
    "password": "<password>",
    "host": "eu1.cloud.thethings.network",
    "port": 1883,
    "topics_subscription": [
        "v3/<appID>@ttn/devices/#"
    ],
    "mqtt_version": 3
}


clients = [
    MQTTv3(client_1),
    MQTTv3(client_2),
    MQTTv3(client_3)
]


class Server:
    def __init__(self, channel, clients):
        self.channel = channel
        self.mqtt_channel_name = "mqtt"
        self.mqtt_channel_sub = "mqtt_sub"
        self.client_1 = clients[0]
        self.client_2 = clients[1]
        self.client_3 = clients[2]

        self.client_1.client.on_message = self._on_message_v5
        self.client_2.client.on_message = self._on_message_v3
        self.client_3.client.on_message = self._on_message_v3

    def _on_message_v3(self, client, userdata, message):

        try:
            device_id = json.loads(message.payload.decode(
                "utf-8", "ignore"))['end_device_ids']['device_id']

            device_name = redis_instance.get(device_id)

            sensor_lib = SensorLib(device_name=device_name, message=message)
            data = sensor_lib.parse()

            for key in data["decoded_messages"]:
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
                        message.topic, self.client_2.host))
                    logger.error('data logging error for topic {} and this client {}'.format(
                        message.topic, self.client_2.host))

        except:
            print('Data from TTN not valid ...')

    def _on_message_v5(self, client, userdata, message):

        try:
            if message.topic == "IG/mbus":
                sensor_lib = SensorLib(
                    device_name="PolluTherm", message=message)
                data = sensor_lib.parse()

                for key in data["decoded_messages"]:
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
                        print('data logging error for topic {} and this client {} and this message {}'.format(
                            message.topic, self.client_1.host, key))
                        logger.error('data logging error for topic {} and this client {} and this message {}'.format(
                            message.topic, self.client_1.host, key))
            else:
                payload = {}
                table = json.loads(redis_instance.get(
                    payload["data_point_name"]))["table_id"]
                if table != None:
                    payload["timestamp"] = payload["timestamp"]
                    payload["table_id"] = table
                    payload["value"] = payload["value"]
                    msg = {
                        "topic": message.topic,
                        "payload": payload,
                        "qos": message.qos,
                        "host": userdata["host"],
                        "port": userdata["port"],
                    }

                    self._asyncio_send(
                        self.channel, self.mqtt_channel_name, self.mqtt_channel_sub, msg)
                else:
                    print('data logging error for topic {} and this client {}'.format(
                        message.topic, self.client_1.host))
                    logger.error('data logging error for topic {} and this client {}'.format(
                        message.topic, self.client_1.host))

        except:
            logger.error('Error: data logging error for topic {} and this client {}'.format(
                message.topic, self.client_1.host))

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

    async def client_2_start(self):
        self.client_2.client.connect(host=self.client_2.host,
                                     port=self.client_2.port,
                                     keepalive=60,
                                     bind_address="",
                                     bind_port=0,
                                     clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                                     properties=None)

        await asyncio.sleep(5)
        while True:
            self.client_2.client.loop(0.1)
            await asyncio.sleep(0.01)
            if not self.client_2.client.connected_flag:
                self.client_2.client.disconnect()
                await asyncio.sleep(5)
                print("client reconnecting ...")
                logger.error("client reconnecting for {} ... ".format(
                    self.client_2.host))
                try:
                    self.client_2.client.connect(host=self.client_2.host,
                                                 port=self.client_2.port,
                                                 keepalive=60,
                                                 bind_address="",
                                                 bind_port=0,
                                                 clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                                                 properties=None)
                    await asyncio.sleep(5)
                except:
                    print("reconnection failed")
                    logger.error("reconnection for {} failed".format(
                        self.client_2.host))

    async def client_3_start(self):
        self.client_3.client.connect(host=self.client_3.host,
                                     port=self.client_3.port,
                                     keepalive=60,
                                     bind_address="",
                                     bind_port=0,
                                     clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                                     properties=None)

        await asyncio.sleep(5)
        while True:
            self.client_3.client.loop(0.1)
            await asyncio.sleep(0.01)
            if not self.client_3.client.connected_flag:
                self.client_3.client.disconnect()
                await asyncio.sleep(5)
                print("client reconnecting ...")
                logger.error("client reconnecting for {} ... ".format(
                    self.client_3.host))
                try:
                    self.client_3.client.connect(host=self.client_3.host,
                                                 port=self.client_3.port,
                                                 keepalive=60,
                                                 bind_address="",
                                                 bind_port=0,
                                                 clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                                                 properties=None)
                    await asyncio.sleep(5)
                except:
                    print("reconnection failed")
                    logger.error("reconnection for {} failed".format(
                        self.client_3.host))

    def run(self):
        loop = asyncio.get_event_loop()
        self.loop = loop

        print("Event loop for mqtt clients running forever ...")
        logger.info("Event loop for mqtt clients running forever ...")

        asyncio.ensure_future(self.client_1_start())
        asyncio.ensure_future(self.client_2_start())
        asyncio.ensure_future(self.client_3_start())
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
        self.client_2.disconnect()
        self.client_3.disconnect()


channel_layer = get_channel_layer()
client_server = Server(channel_layer, clients)
client_server.run()
