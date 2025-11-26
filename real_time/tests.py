import pytest
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase, override_settings
from django.utils import timezone
from chat.models import Chat  
from src.asgi import application
from chat.models import ChatParticipant
User = get_user_model()

CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}


@pytest.mark.asyncio
@override_settings(CHANNEL_LAYERS=CHANNEL_LAYERS)
class ChatWebsocketTest(TransactionTestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            phone_number="01009874328",
            full_name="somebody",
        )

     
        self.chat = Chat.objects.create(name="Test Chat")

        self.participant = ChatParticipant.objects.create(user=self.user,chat=self.chat,is_online=True,last_seen=timezone.now())
        

    async def test_connect(self):
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{self.chat.id}/",
        )


        communicator.scope["user"] = self.user

        connected, _ = await communicator.connect()
        assert connected

        await communicator.disconnect()
