from django.db import models
from django.contrib.auth import get_user_model
from chat.utils import EncryptionService
from django.conf import settings
import json
import logging


User = get_user_model()
logger = logging.getLogger(__name__)



class Message(models.Model):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("seen", "Seen"),
    ]

    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="sent")
    is_encrypted = models.BooleanField(default=False)
    encryption_version = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["chat", "created_at"]),
            models.Index(fields=["sender"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_encrypted"]),
        ]

    def encrypt_content(self, content: str) -> str:
        """Encrypt message content"""
        try:
            if not settings.ENABLE_MESSAGE_ENCRYPTION:
                return content
                
            enc = EncryptionService()
            self.is_encrypted = True
            self.encryption_version = "1.0"
            return enc.encrypt(content)
        except Exception as e:
            logger.error(f"Content encryption failed: {str(e)}")
            raise ValueError("Failed to encrypt message content")

    def decrypt_content(self) -> str:
        """Decrypt message content"""
        try:
            if not self.is_encrypted:
                return self.content
                
            enc = EncryptionService()
            return enc.decrypt(self.content)
        except Exception as e:
            logger.error(f"Content decryption failed: {str(e)}")
            return "[Encrypted content cannot be decrypted]"

    def to_json(self):
        """Convert message to JSON with decrypted content"""
        try:
            content = self.decrypt_content() if self.is_encrypted else self.content
            return {
                "id": self.id,
                "chat_id": self.chat_id,
                "sender_id": self.sender_id,
                "content": content,
                "created_at": self.created_at.isoformat(),
                "is_encrypted": self.is_encrypted,
                "status": self.status,
            }
        except Exception as e:
            logger.error(f"Error converting message to JSON: {str(e)}")
            return {
                "id": self.id,
                "error": "Could not process message content"
            }