from django.db import models
from django.contrib.auth import get_user_model
from .chat import Chat

User = get_user_model()


class Message(models.Model):
     content = models.TextField(max_length=500)
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
     chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
     created_at = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
