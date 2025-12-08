from rest_framework import serializers
from ..models import Chat
from .message import MessageSerializer
from users.serializers import ProfileSerializer
from ..models import Message
class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['name', 'messages', 'created_at','id']



class ChatListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['name', 'last_message', 'user']

    def get_last_message(self, obj):
        message = obj.messages.order_by('-created_at').first()
        if message:
            return MessageSerializer(message).data
        return None

    def get_user(self, obj):
        
        other_participant = obj.participants.exclude(
            user=self.context['request'].user
        ).first()

        if other_participant:
            
            return ProfileSerializer(other_participant.user).data

        return None

