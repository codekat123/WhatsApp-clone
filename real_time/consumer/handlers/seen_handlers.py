async def handle_seen(consumer, data, user):
    """Handle message seen status"""
    await consumer.db.mark_all_seen(consumer.chat_id, user.id)
    await consumer.channel_layer.group_send(
        consumer.room_group_name,
        {"type": "seen.event", "user_id": user.id},
    )
