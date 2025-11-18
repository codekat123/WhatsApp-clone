from django.db import models 
from django.contrib.auth import get_user_model
from .chat import Chat
User = get_user_model()


class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_participations')
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField()
    last_seen = models.DateTimeField()

    class Meta:
        unique_together = ('chat', 'user')
    
    def save(self, *args, **kwargs):
        if not self.chat.is_group:
            if self.chat.participants.count() >= 2:
                raise ValueError("Private chat cannot have more than two participants.")
        super().save(*args, **kwargs)