from channels.db import database_sync_to_async
from django.utils import timezone
from chat.models import Chat, ChatParticipant, Message, Block
from datetime import timedelta
from django.utils import timezone


@database_sync_to_async
def get_chat(chat_id):
    try:
        return Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return None


@database_sync_to_async
def is_member(chat, user):
    return ChatParticipant.objects.filter(chat=chat, user=user).exists()


@database_sync_to_async
def is_blocked(chat, user):
    participants = ChatParticipant.objects.filter(chat=chat)
    return Block.objects.filter(blocked=user, blocker__in=[p.user for p in participants]).exists()


@database_sync_to_async
def create_message(chat_id, sender_id, content, message_type):
    msg = Message.objects.create(
        chat_id=chat_id,
        sender_id=sender_id,
        content=content,
        message_type=message_type,
    )
    return msg.to_json()


@database_sync_to_async
def mark_all_delivered(chat_id, user_id):
    Message.objects.filter(
        chat_id=chat_id,
        status="sent"
    ).exclude(sender_id=user_id).update(status="delivered")


@database_sync_to_async
def mark_all_seen(chat_id, user_id):
    Message.objects.filter(
        chat_id=chat_id,
        status__in=["sent", "delivered"]
    ).exclude(sender_id=user_id).update(status="seen")


@database_sync_to_async
def set_user_presence(chat_id, user_id, is_online):
    ChatParticipant.objects.filter(
        chat_id=chat_id,
        user_id=user_id
    ).update(is_online=is_online, last_seen=timezone.now())



@database_sync_to_async
def update_message(message_id, new_content, user_id):
    message = Message.objects.filter(id=message_id, sender_id=user_id).first()
    
    if not message:
        return None


    if timezone.now() - message.created_at > timedelta(minutes=15):
        return None
    
    message.content = new_content
    message.save()

    return message.to_json()

@database_sync_to_async
def delete_message(message_id, user_id):
    deleted_count, _ = Message.objects.filter(
        id=message_id,
        sender_id=user_id
    ).delete()

    return deleted_count > 0

@database_sync_to_async
def is_online(user_id):
    return (
        ChatParticipant.objects
        .filter(user_id=user_id)
        .values_list("is_online", flat=True)
        .first()
    )

@database_sync_to_async
def get_unread_message(user_id):
    return list(
        Message.objects
        .filter(
            chat__participants__user_id=user_id,  
            status='delivered',
        )
        .exclude(sender_id=user_id)
        .order_by('-created_at')
    )[:30]