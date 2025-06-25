from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from astek_technical_task.accounts.types import UserInterface

User = get_user_model()


def login_user(*, username: str, password: str) -> dict:
    user = authenticate(username=username, password=password)
    if not user:
        raise ValidationError(_("Invalid username or password"))
    if not user.is_active:
        raise ValidationError(_("User is inactive"))
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def create_user(user_interface: UserInterface) -> User:
    return User.objects.create(
           first_name=user_interface.first_name,
           last_name=user_interface.last_name,
           username=user_interface.username,
           password=user_interface.password,
           email=user_interface.email
    )
