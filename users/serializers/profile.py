from rest_framework import serializers
from django.core.files.images import get_image_dimensions
from PIL import Image
from ..models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['about', 'phone_number', 'full_name', 'image']
        read_only_fields = ['phone_number']

    def validate_image(self, image):
        
        max_size = 3 * 1024 * 1024
        if image.size > max_size:
            raise serializers.ValidationError("Image is too large. Max size is 3MB.")

        valid_formats = ['JPEG', 'JPG', 'PNG', 'WEBP']
        try:
            img = Image.open(image)
            format = img.format.upper()
            if format not in valid_formats:
                raise serializers.ValidationError("Unsupported image format.")
        except Exception:
            raise serializers.ValidationError("Corrupted or invalid image file.")


        width, height = get_image_dimensions(image)
        if width > 3000 or height > 3000:
            raise serializers.ValidationError("Image dimensions are too large.")


        if width < 200 or height < 200:
            raise serializers.ValidationError("Image is too small. Minimum size is 200x200.")

        return image
