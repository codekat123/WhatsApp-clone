from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import VerifyOTPSerializer
from ..utils import get_session, increment_attempts, clear_session, MAX_VERIFY_ATTEMPTS


User = get_user_model()

class RegisterAPIView(APIView):
     permission_classes = (AllowAny,)

     def post(self,request):
          serializer = VerifyOTPSerializer(request.data)
          serializer.is_valid(raise_exception=True)
          session_id = serializer.validated_data['session_id']
          otp = serializer.validated_data['otp']
      
          session = get_session(session_id)

          if not session:
               return Response({"detail": "Session expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)

          attempts = increment_attempts(session_id)

          if attempts > MAX_VERIFY_ATTEMPTS:
               return Response({"detail": "Too many wrong attempts. Request a new OTP."},
                          status=status.HTTP_403_FORBIDDEN)


          if session.get("otp") != otp:
               return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

          clear_session(session_id)

          phone = session.get("phone")
          user, created = User.objects.get_or_create(
              phone_number=phone,
              defaults={"full_name": "", "is_active": True}
          )
          refresh = RefreshToken.for_user(user)
          return Response({
              "access": str(refresh.access_token),
              "refresh": str(refresh),
              "user": {
                  "id": user.pk,
                  "phone_number": str(user.phone_number),
                  "created": created
              }
          }, status=status.HTTP_200_OK)