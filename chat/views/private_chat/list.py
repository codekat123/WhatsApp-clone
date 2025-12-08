from rest_framework.generics import ListAPIView
from ...models import Chat
from ...serializers import ChatListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max



class ChatListPerUser(ListAPIView):
     serializer_class = ChatListSerializer
     authentication_classes = [JWTAuthentication]
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
        user = self.request.user

        return (
            Chat.objects
            .filter(participants__user=user)
            .annotate(last_message_time=Max('messages__created_at'))
            .order_by('-last_message_time')
        )
