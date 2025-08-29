from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class EmailOrUsernameBackend(BaseBackend):
    """
    Custom authentication backend to allow login using either email or username.
    """
    def authenticate(self, request, username=None, password=None):
        email_validator = EmailValidator()
        user = None

        try:
            email_validator(username)
            user = UserModel.objects.get(email=username)
        except ValidationError:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None
        except UserModel.DoesNotExist:
            return None

        if user is not None and user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        """
        Return user instance by user ID.
        """
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
