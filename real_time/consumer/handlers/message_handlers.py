import json

async def handle_create_message(consumer, data, user):
    """Handle message creation"""
    allowed, consumer.msg_timestamps = consumer.rate_limit(consumer.msg_timestamps)
    if not allowed:
        return await consumer.send(json.dumps({"error": "Slow down"}))

    content = data.get("content", "").strip()
    message_type = data.get("message_type", "text")

    if not content:
        return

    msg_data = await consumer.db.create_message(
        chat_id=consumer.chat_id,
        sender_id=user.id,
        content=content,
        message_type=message_type
    )

    await consumer.channel_layer.group_send(
        consumer.room_group_name,
        {"type": "chat.message", "message": msg_data},
    )

async def handle_delete_message(consumer, data, user):
    """Handle message deletion"""
    message_id = data.get("message_id")
    is_done = await consumer.db.delete_message(message_id, user.id)

    await consumer.channel_layer.group_send(
        consumer.room_group_name,
        {
            "type": "delete.message",
            "message_id": message_id,
            "success": is_done,
            "by_user": user.id
        }
    )

async def handle_update_message(consumer, data, user):
    """Handle message updates"""
    message_id = data["message_id"]
    new_content = data["new_content"]

    message_data = await consumer.db.update_message(
        message_id,
        new_content,
        user.id
    )

    await consumer.channel_layer.group_send(
        consumer.room_group_name,
        {"type": "update.message", "message": message_data}
    )
