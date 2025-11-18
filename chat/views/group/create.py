from rest_framework.generics import CreateAPIView
from ...models import Chat,ChatParticipant
from django.contrib.auth import get_user_model
from  ...serializers import ChatSerializer



User = get_user_model()

class GroupChatCreateAPIView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        chat = serializer.save(
            created_by=self.request.user,
            is_group=True
        )

        ChatParticipant.objects.create(
            chat=chat,
            user=self.request.user,
            is_admin=True
        )
