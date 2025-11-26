from django.db import models
from users.models import User



class Chat(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='chats_created'
    )

    def __str__(self):
        if self.is_group and self.name:
            return self.name
        return f"Chat {self.pk}"

