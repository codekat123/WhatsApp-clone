from ..models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['phone_number']

    def validate_phone_number(self, number):
        number_str = str(number)


        digits_only = ''.join(filter(str.isdigit, number_str))
        if not 10 <= len(digits_only) <= 15:
            raise serializers.ValidationError("Invalid phone number length.")


        if digits_only.count(digits_only[0]) == len(digits_only):
            raise serializers.ValidationError("Phone number not allowed.")

        return number