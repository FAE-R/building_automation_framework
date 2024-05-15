from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from logger.consumers import MqttConsumer, DWDConsumer
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'channel': ChannelNameRouter(
        {
            "mqtt": MqttConsumer.as_asgi(),
            "dwd_worker": DWDConsumer.as_asgi()
        }
    )
})
