import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from real_time.routing import chat_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat_urlpatterns)
    )
})
