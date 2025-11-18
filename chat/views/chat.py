from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.db import models, transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from ..models import Chat, ChatParticipant, Message, Block
from ..serializers import MessageSerializer

User = get_user_model()


class PrivateChat(APIView):
    def get(self, request, user_id):
        current_user = request.user
        receiver = get_object_or_404(User, id=user_id)

        if current_user.id == receiver.id:
            raise PermissionDenied("You cannot create a private chat with yourself.")


        if Block.objects.filter(
            models.Q(blocked=current_user, blocker=receiver) |
            models.Q(blocked=receiver, blocker=current_user)
        ).exists():
            raise PermissionDenied("You cannot message this user because one of you blocked the other.")


        chat = (
            Chat.objects
            .filter(is_group=False)
            .filter(participants__user__in=[current_user, receiver])
            .annotate(count=Count("participants"))
            .filter(count=2)
            .first()
        )

        
        if not chat:
            with transaction.atomic():
                chat = (
                    Chat.objects
                    .create(is_group=False, created_by=current_user)
                )
                ChatParticipant.objects.bulk_create([
                    ChatParticipant(chat=chat, user=current_user),
                    ChatParticipant(chat=chat, user=receiver)
                ])

        
        messages = (
            Message.objects
            .filter(chat=chat)
            .order_by("-created_at")[:30]
        )

        serializer = MessageSerializer(messages, many=True)
        return Response({"messages": serializer.data}, status=status.HTTP_200_OK)
