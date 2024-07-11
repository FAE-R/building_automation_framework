# Import the ProtocolTypeRouter and ChannelNameRouter classes from the channels.routing module
# ProtocolTypeRouter is used to route different types of connections (e.g., HTTP, WebSocket)
# ChannelNameRouter is used to route messages based on their channel name
from channels.routing import ProtocolTypeRouter, ChannelNameRouter

# Import the MqttConsumer class from the logger.consumers module
# MqttConsumer handles MQTT messages
from logger.consumers import MqttConsumer
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'channel': ChannelNameRouter(
        {
            "mqtt": MqttConsumer.as_asgi()
        }
    )
})
