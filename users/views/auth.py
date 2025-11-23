from ..utils import create_session_for_phone
from ..serializers import SendOTPSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny



def send_sms(phone: str, otp: str):
    """
    Replace with your SMS provider (Twilio, Vonage, etc).
    In production call this as a Celery task (non-blocking).
    """
    print(f"[DEBUG] send OTP {otp} to {phone}")


class SendOTPView(APIView):
    permission_classes = (AllowAny,)


    def post(self, request):
          serializer = SendOTPSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          phone_number = str(serializer.validated_data.get('phone_number'))

          try:
               session = create_session_for_phone(phone_number)
          except RuntimeError as e:
               return Response({"detail": str(e)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
          
          send_sms(phone_number,session)

          return Response({
            "detail": "OTP sent",
            "session_id": session["session_id"],
            "expires_in": session["expires_in"],
        }, status=status.HTTP_200_OK)