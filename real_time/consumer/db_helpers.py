from channels.db import database_sync_to_async
from django.utils import timezone
from chat.models import Chat, ChatParticipant, Message, Block
from datetime import timedelta
from django.utils import timezone
from chat.utils import EncryptionService
import logging


logger = logging.getLogger(__name__)


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
def create_message(chat_id, sender_id, content, status,is_encrypted=False):
    msg = Message.objects.create(
        chat_id=chat_id,
        sender_id=sender_id,
        content=content,
        status=status,
        is_encrypted=is_encrypted,
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
def get_unread_messages(user_id, limit=30):
    """
    Retrieve unread messages for a user.
    
    Args:
        user_id: ID of the user
        limit: Maximum number of messages to return (default: 30)
        
    Returns:
        list: List of message dictionaries with decrypted content
    """
    try:
        messages = (
            Message.objects
            .filter(
                chat__participants__user_id=user_id,
                status='delivered'
            )
            .exclude(sender_id=user_id)
            .select_related('sender', 'chat')  # Optimize DB queries
            .order_by('-created_at')[:limit]
        )

        # Convert to list of dictionaries with decrypted content
        return [{
            'id': msg.id,
            'content': msg.decrypt_content() if msg.is_encrypted else msg.content,
            'sender_id': msg.sender.id,
            'chat_id': msg.chat.id,
            'created_at': msg.created_at.isoformat(),
            'is_encrypted': msg.is_encrypted,
            'status': msg.status
        } for msg in messages]
        
    except Exception as e:
        logger.error(f"Error fetching unread messages for user {user_id}: {str(e)}")
        return []