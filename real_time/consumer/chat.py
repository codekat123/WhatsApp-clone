from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .rate_limit import RateLimiter
from . import db_helpers
from .handlers import (
    handle_create_message,
    handle_delete_message,
    handle_update_message,
    handle_typing,
    handle_seen,
    broadcast_presence as broadcast_presence_handler,
    handle_notifications,
)


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for handling chat functionality.
    
    This consumer handles WebSocket connections for chat rooms and routes
    incoming messages to appropriate handler functions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate_limiter = RateLimiter(limit=15, window=60)
        self.db = db_helpers  

    handlers = {
        "typing": handle_typing,
        "create_message": handle_create_message,
        "delete_message": handle_delete_message,
        "update_message": handle_update_message,
        "seen": handle_seen,
        "notifications": handle_notifications,
    }

    async def connect(self):
        """Handle new WebSocket connection."""
        user = self.scope["user"]
        if not user.is_authenticated:
            return await self.close()

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        chat = await db_helpers.get_chat(self.chat_id)

        if not chat:
            return await self.close()

        if await db_helpers.is_blocked(chat, user):
            return await self.close()

        if not await db_helpers.is_member(chat, user):
            return await self.close()

        self.room_group_name = f"chat_{self.chat_id}"
        self.user = user
        

        await db_helpers.set_user_presence(self.chat_id, user.id, True)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        # Use the presence handler
        await broadcast_presence_handler(self, "online", user)

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if hasattr(self, "chat_id") and hasattr(self, "user"):
            await db_helpers.set_user_presence(self.chat_id, self.user.id, False)
            await broadcast_presence_handler(self, "offline", self.user)

    async def receive(self, text_data=None, bytes_data=None):
        """Receive message from WebSocket and route to appropriate handler."""
        user = self.scope["user"]
        if not user.is_authenticated:
            return

        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, TypeError):
            return

        event_type = data.get("type")
        if not event_type:
            return

        # Route to appropriate handler if exists
        handler = self.handlers.get(event_type)
        if handler:
            await handler(self, data, user)

    # --------------------------------------------------------
    # Outgoing Event Methods
    # --------------------------------------------------------

    async def chat_message(self, event):
        """Send new chat message to WebSocket."""
        await self.send(text_data=json.dumps(event["message"]))

    async def delete_message(self, event):
        """Notify clients about deleted message."""
        await self.send(json.dumps({
            "type": "delete_message",
            "message_id": event["message_id"],
            "success": event["success"],
            "by_user": event["by_user"],
        }))

    async def update_message(self, event):
        """Send updated message to WebSocket."""
        await self.send(json.dumps(event["message"]))

    async def typing_event(self, event):
        """Broadcast typing indicator to chat participants."""
        await self.send(json.dumps({
            "type": "typing",
            "user_id": event["user_id"]
        }))

    async def seen_event(self, event):
        """Notify clients about seen messages."""
        await self.send(json.dumps({
            "type": "seen",
            "user_id": event["user_id"]
        }))

    async def presence_event(self, event):
        """Broadcast user presence status."""
        await self.send(json.dumps({
            "type": "presence",
            "status": event["status"],
            "user_id": event["user_id"]
        }))

    async def notification_event(self, event):
        await self.send(json.dumps({
            "type": "notifications",
            "messages": event["messages"],
            "user_id": event["user_id"]
        }))
