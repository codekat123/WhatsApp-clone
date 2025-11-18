from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .rate_limit import allowed_to_send
from . import db_helpers


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

        self.msg_timestamps = []

        await db_helpers.set_user_presence(self.chat_id, user.id, True)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.broadcast_presence("online")


    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await db_helpers.set_user_presence(self.chat_id, self.user.id, False)

        await self.broadcast_presence("offline")

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope["user"]
        if not user.is_authenticated:
            return

        try:
            data = json.loads(text_data)
        except:
            return

        event_type = data.get("type")

        if event_type == "typing":
            return await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "typing.event", "user_id": user.id},
            )

        if event_type == "create_message":

            allowed, self.msg_timestamps = allowed_to_send(self.msg_timestamps)
            if not allowed:
                return await self.send(json.dumps({"error": "Slow down"}))

            content = data.get("content", "").strip()
            message_type = data.get("message_type", "text")

            if not content:
                return


            msg_data = await db_helpers.create_message(
                chat_id=self.chat_id,
                sender_id=user.id,
                content=content,
                message_type=message_type
            )

            # broadcast to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.message", "message": msg_data},
            )

        if event_type == "seen":
            await db_helpers.mark_all_seen(self.chat_id, user.id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "seen.event", "user_id": user.id},
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def typing_event(self, event):
        await self.send(json.dumps({"type": "typing", "user_id": event["user_id"]}))

    async def seen_event(self, event):
        await self.send(json.dumps({"type": "seen", "user_id": event["user_id"]}))

    async def presence_event(self, event):
        await self.send(json.dumps({
            "type": "presence",
            "status": event["status"],
            "user_id": event["user_id"]
        }))

    async def broadcast_presence(self, status):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "presence.event",
                "status": status,
                "user_id": self.user.id,
            }
        )
