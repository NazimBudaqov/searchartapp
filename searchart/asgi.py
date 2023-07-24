import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from apps.searchartapi.consumers import ProgressConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchart.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # Add your WebSocket routing here
            path('import_progress/', ProgressConsumer.as_asgi()),
        ])
    ),
})


