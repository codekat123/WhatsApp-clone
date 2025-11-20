from django.db import models
from django.contrib.auth import get_user_model
from .chat import Chat

User = get_user_model()


class Message(models.Model):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("seen", "Seen"),
    ]

    content = models.TextField(max_length=500)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="sent")

    class Meta:
        indexes = [
            models.Index(fields=["chat", "created_at"]),
            models.Index(fields=["sender"]),
            models.Index(fields=["status"]),
        ]

    def to_json(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }
