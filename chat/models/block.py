from django.db import models
from users.models import User


class Block(models.Model):
     blocker = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blocked_users')
     blocked = models.ForeignKey(User,on_delete=models.CASCADE,related_name='block_by')
     created_at = models.DateTimeField(auto_now_add=True)
     
     class Meta:
         unique_together = ('blocker', 'blocked')