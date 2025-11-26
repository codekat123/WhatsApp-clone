from ...models import Chat,ChatParticipant
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from  ...serializers import GroupAddMemberSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class GroupAddAdminAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupAddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member_id = serializer.validated_data['user_id']
        group_id = serializer.validated_data['group_id']

        group = get_object_or_404(Chat, id=group_id, is_group=True)
        user = get_object_or_404(User, id=member_id)

        
        if not ChatParticipant.objects.filter(
            chat=group,
            user=request.user,
            is_admin=True
        ).exists():
            return Response(
                {"detail": "Only group admins can promote users."},
                status=status.HTTP_403_FORBIDDEN
            )

        member = ChatParticipant.objects.filter(
            user=user,
            chat=group
        ).first()

        if not member:
            raise ValidationError(
                {"detail": "This user is not in this group."}
            )

        member.is_admin = True
        member.save()

        return Response(
            {"detail": "User has been promoted to admin successfully."},
            status=status.HTTP_200_OK
        )
