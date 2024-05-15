import paho.mqtt.client as mqtt
from mqtt_client_logger import logger_conf

logger = logger_conf(__name__)


class MQTTv5:
    def __init__(self, client):
        self.host = client["host"]
        self.port = client["port"]
        self.mqtt_version = client["mqtt_version"]
        self.username = client["username"]
        self.password = client["password"]
        self.topics_subscription = client["topics_subscription"]
        
        assert isinstance(self.topics_subscription, list), "Topic subscription must be a list with topic"

        self.client = mqtt.Client(client_id=None, userdata={
                "host": self.host,
                "port": self.port,
            },
            protocol=mqtt.MQTTv5
        )
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.connected_flag = False


    def _on_connect(self, client, userdata, flags, reasonCode, properties=None):
        logger.info('data logging connected for this client {}'.format(self.host))
        self.client.connected_flag = True
        for i in self.topics_subscription:
            self.client.subscribe(topic=i)   

    def _on_disconnect(self, client, userdata, rc):
        print("MQTTv5 client disconnected ...")
        logger.warning('data logging disconnected for this client {}'.format(self.host))
        self.client.connected_flag = False


class MQTTv3:
    def __init__(self, client):
        self.host = client["host"]
        self.port = client["port"]
        self.mqtt_version = client["mqtt_version"]
        self.username = client["username"]
        self.password = client["password"]
        self.topics_subscription = client["topics_subscription"]

        self.client = mqtt.Client(client_id=None, userdata={
            "host": self.host,
            "port": self.port,
        })

        assert isinstance(self.topics_subscription, list), "Topic subscription must be a list with topic"
        self.client.username_pw_set(username=self.username, password=self.password)
        
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.connected_flag = False


    def _on_connect(self, client, userdata, flags, reasonCode, properties=None):
        self.client.connected_flag = True
        logger.info('data logging connected for this client {}'.format(self.host))
        for i in self.topics_subscription:
            self.client.subscribe(topic=i)   

    def _on_disconnect(self, client, userdata, rc):
        print("MQTTv3 client disconnected ...")
        logger.warning('data logging disconnected for this client {}'.format(self.host))
        self.client.connected_flag = False


