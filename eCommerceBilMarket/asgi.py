from django.urls import re_path
from django.core.asgi import get_asgi_application
import chat.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "https": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            chat.routing.websocket_urlpatterns
        ])
    ),
})