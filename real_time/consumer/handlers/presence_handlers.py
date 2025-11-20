async def broadcast_presence(consumer, status, user):
    """Broadcast user presence status to the chat group"""
    await consumer.channel_layer.group_send(
        consumer.room_group_name,
        {
            "type": "presence.event",
            "status": status,
            "user_id": user.id,
        }
    )
