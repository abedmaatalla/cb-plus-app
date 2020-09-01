from channels.routing import ProtocolTypeRouter, URLRouter

from main import routing
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter(
            routing.websocket_urlpatterns
        )
})