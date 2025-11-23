from ..db_helpers import get_unread_messages

async def handle_notifications(consumer, data, user):
    unread = await get_unread_messages(user.id)

    await consumer.channel_layer.group_send(
        consumer.room_group_name,
        {
            "type": "notification.event",
            "messages": [msg.to_json() for msg in unread],
            "user_id": user.id
        }
    )
