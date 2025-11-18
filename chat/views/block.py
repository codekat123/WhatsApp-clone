from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Block
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class BlockUserAPIView(APIView):
    def post(self, request, user_id):
        blocked = get_object_or_404(User, id=user_id)

        if blocked == request.user:
            return Response({"detail": "You can't block yourself."}, status=400)

        Block.objects.get_or_create(
            blocker=request.user,
            blocked=blocked
        )
        return Response({"detail": "User blocked successfully."}, status=201)

class UnblockUserAPIView(APIView):
    def delete(self, request, user_id):
        blocked = get_object_or_404(User, id=user_id)
        Block.objects.filter(
            blocker=request.user,
            blocked=blocked
        ).delete()
        return Response({"detail": "User unblocked successfully."}, status=200)
