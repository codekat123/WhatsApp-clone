import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')


django_asgi_app = get_asgi_application()

from real_time.routing import chat_urlpatterns
from real_time.websocket_jwt_middleware import JWTAuthMiddleware  

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(chat_urlpatterns)
    ),
})
