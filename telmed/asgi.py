import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import telmed.routing 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telmed.settings')  # Replace with your project name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            telmed.routing.websocket_urlpatterns
        )
    ),
})
