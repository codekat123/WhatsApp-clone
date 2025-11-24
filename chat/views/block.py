from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Block
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()


class ToggleBlockAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)

        if target == request.user:
            return Response({"detail": "You can't block yourself."}, status=400)

        block_obj, created = Block.objects.get_or_create(
            blocker=request.user,
            blocked=target
        )

        if not created:
            block_obj.delete()
            return Response({"detail": "User unblocked."}, status=200)

        return Response({"detail": "User blocked."}, status=201)

