import asyncio
from channels.layers import get_channel_layer
from mqtt_client_logger import logger_conf
from mergeData import merge
from wetterdienst.provider.dwd.observation import (
    DwdObservationParameter
)


logger = logger_conf(__name__)


async def send_channel(future, channel_layer, channel, event):
    result = await channel_layer.send(channel, event)
    future.set_result(result)


class Server:
    def __init__(self, channel):
        self.channel = channel
        self.mqtt_channel_name = "dwd_worker"
        self.mqtt_channel_sub = "dwd_worker_sub"

    def _asyncio_send(self, channel, mqtt_channel_name, mqtt_channel_sub, msg):
        try:
            future = asyncio.Future()
            asyncio.ensure_future(send_channel(future, channel, mqtt_channel_name, {
                                  "type": mqtt_channel_sub, "text": msg}))

        except Exception as e:
            print("Cannot send message ...")
            logger.error("Cannot send message {}".format(msg))
            logger.exception(e)

    async def client_start(self):
        while True:
            parameters = [
                DwdObservationParameter.MINUTE_10.TEMPERATURE_AIR_MIN_200,
            ]

            try:
                data = merge(parameters)
                index_list = data.index.tolist()
                value_list = data.values.tolist()

                for i in range(len(index_list)):
                    msg = {
                        "table_id": "weather_temperature",
                        "timestamp": index_list[i].strftime("%Y-%m-%dT%H:%M:%S"),
                        "value": value_list[i]
                    }
                    self._asyncio_send(self.channel, self.mqtt_channel_name,
                                       self.mqtt_channel_sub, msg)

                await asyncio.sleep(0.1)
            except Exception as e:
                print("DWD temp: Cannot send message ...")
                logger.error("DWD temp: Cannot send message {}".format(msg))
                logger.exception(e)

            parameters = [
                DwdObservationParameter.MINUTE_10.HUMIDITY,
            ]

            try:
                data = merge(parameters)
                index_list = data.index.tolist()
                value_list = data.values.tolist()

                for i in range(len(index_list)):
                    msg = {
                        "table_id": "weather_humidity",
                        "timestamp": index_list[i].strftime("%Y-%m-%dT%H:%M:%S"),
                        "value": value_list[i]
                    }
                    self._asyncio_send(self.channel, self.mqtt_channel_name,
                                       self.mqtt_channel_sub, msg)
                await asyncio.sleep(0.1)
            except Exception as e:
                print("DWD humidity: Cannot send message ...")
                logger.error(
                    "DWD humidity: Cannot send message {}".format(msg))
                logger.exception(e)

            parameters = [
                DwdObservationParameter.MINUTE_10.RADIATION_GLOBAL,
            ]

            try:
                data = merge(parameters)
                index_list = data.index.tolist()
                value_list = data.values.tolist()

                for i in range(len(index_list)):
                    msg = {
                        "table_id": "weather_g_radiation",
                        "timestamp": index_list[i].strftime("%Y-%m-%dT%H:%M:%S"),
                        "value": value_list[i]
                    }
                    self._asyncio_send(self.channel, self.mqtt_channel_name,
                                       self.mqtt_channel_sub, msg)
                await asyncio.sleep(0.1)
            except Exception as e:
                print("DWD g_radiation: Cannot send message ...")
                logger.error(
                    "DWD g_radiation: Cannot send message {}".format(msg))
                logger.exception(e)

            await asyncio.sleep(60*30)

    def run(self):
        loop = asyncio.get_event_loop()
        self.loop = loop

        print("Event loop for mqtt clients running forever ...")
        logger.info("Event loop for mqtt clients running forever ...")

        asyncio.ensure_future(self.client_start())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            print("DWD client disconnected ... loop exited")
            logger.debug("DWD client disconnected ... loop exited")
            loop.close()


channel_layer = get_channel_layer()
client_server = Server(channel_layer)
client_server.run()
