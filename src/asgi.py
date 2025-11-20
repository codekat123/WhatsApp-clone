import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from real_time.routing import chat_urlpatterns
from notifications.routing import notification_urlpatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(chat_urlpatterns,notification_urlpatterns),
})

