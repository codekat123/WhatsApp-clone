from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, full_name, password, **extra_fields)
