from ...models import Chat,ChatParticipant
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from  ...serializers import GroupAddMemberSerializer


User = get_user_model()

class GroupAddMemberAPIView(APIView):


    def post(self, request):
        serializer = GroupAddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_id = serializer.validated_data["group_id"]
        member_id = serializer.validated_data["member_id"]

        group = get_object_or_404(Chat, id=group_id, is_group=True)
        member = get_object_or_404(User, id=member_id)

        
        if not ChatParticipant.objects.filter(
            chat=group,
            user=request.user,
            is_admin=True
        ).exists():
            return Response(
                {"detail": "Only group admins can add new members."},
                status=status.HTTP_403_FORBIDDEN
            )

        participant, created = ChatParticipant.objects.get_or_create(
            chat=group,
            user=member
        )

        if not created:
            return Response(
                {"detail": "User is already in the group."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Member added successfully."},
            status=status.HTTP_201_CREATED
        )
