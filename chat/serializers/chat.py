from rest_framework import serializers
from ..models import Chat
from .message import MessageSerializer

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['name', 'messages', 'create_at']
