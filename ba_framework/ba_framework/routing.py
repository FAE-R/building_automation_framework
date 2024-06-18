from channels.routing import ProtocolTypeRouter, ChannelNameRouter
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
