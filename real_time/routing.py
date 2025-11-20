from django.urls import path
from .consumer import ChatConsumer

chat_urlpatterns = [
    path("ws/chat/<int:chat_id>/", ChatConsumer.as_asgi()),
]
