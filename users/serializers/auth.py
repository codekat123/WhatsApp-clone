from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class SendOTPSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region="EG")  

class VerifyOTPSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    otp = serializers.CharField(min_length=6, max_length=6)
