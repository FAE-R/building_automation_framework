# Import the ProtocolTypeRouter and ChannelNameRouter classes from the channels.routing module
# ProtocolTypeRouter is used to route different types of connections (e.g., HTTP, WebSocket)
# ChannelNameRouter is used to route messages based on their channel name
from channels.routing import ProtocolTypeRouter, ChannelNameRouter

# Import the MqttConsumer class from the logger.consumers module
# MqttConsumer handles MQTT messages
from logger.consumers import MqttConsumer

# Import the get_asgi_application function from the django.core.asgi module
# get_asgi_application returns an ASGI callable that handles HTTP requests
from django.core.asgi import get_asgi_application

# Define the application as a ProtocolTypeRouter
# This router directs different types of connections to appropriate handlers
application = ProtocolTypeRouter({
    # Route HTTP requests to Django's ASGI application
    "http": get_asgi_application(),
    
    # Route messages sent to channels to the appropriate consumer
    'channel': ChannelNameRouter(
        {
            # Route messages sent to the "mqtt" channel to the MqttConsumer
            "mqtt": MqttConsumer.as_asgi()
        }
    )
})
