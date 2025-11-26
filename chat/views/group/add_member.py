from ...models import Chat,ChatParticipant
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from  ...serializers import GroupAddMemberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone

User = get_user_model()

class GroupAddMemberAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupAddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_id = serializer.validated_data["group_id"]
        member_id = serializer.validated_data["user_id"]

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
            user=member,
            defaults={"is_online": False,"last_seen":timezone.now()}
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
