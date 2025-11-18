from rest_framework.generics import UpdateAPIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ...models import Chat, ChatParticipant
from ...serializers import ChatSerializer


class GroupUpdateAPIView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_url_kwarg = "group_id"

    def get_object(self):
        group_id = self.kwargs.get(self.lookup_url_kwarg)
        group = get_object_or_404(Chat, id=group_id)

        
        is_admin = ChatParticipant.objects.filter(
            user=self.request.user,
            chat=group,
            is_admin=True
        ).exists()

        if not is_admin:
            raise ValidationError("you are not allowed to update this group")

        return group

    def perform_update(self, serializer):
        
        serializer.save()
