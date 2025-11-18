from rest_framework.generics import DestroyAPIView
from ...models import Chat, ChatParticipant
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

class GroupDestroyAPIView(DestroyAPIView):
    queryset = Chat.objects.all()

    def get_object(self):
        group_id = self.kwargs['group_id']

        
        group = get_object_or_404(Chat, id=group_id, is_group=True)


        is_admin = ChatParticipant.objects.filter(
            user=self.request.user,
            chat=group,
            is_admin=True
        ).exists()

        if not is_admin:
            raise ValidationError("You are not allowed to delete this group.")

        return group

          
