async def handle_typing(consumer, data, user):
    """Handle typing indicators"""
    await consumer.channel_layer.group_send(
        consumer.room_group_name,
        {"type": "typing.event", "user_id": user.id},
    )
