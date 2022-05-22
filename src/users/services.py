from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import authenticate

from users.models import User
from users.utils import UserErrorMessages
from app.errors import (
    ValidationError,
    ObjectAlreadyExists
)


class UserCreator:
    def __init__(self, username, password):
        self.username = str(username).lower()
        self.password = password

    def __call__(self, raise_exception=True):
        if self.allowed_to_create(raise_exception):
            user = self.create()
            user.save()
            return user
        else:
            return None

    def create(self):
        return User.objects.create_user(
            email=self.username,
            password=self.password,
        )

    def allowed_to_create(self, raise_exception=True):
        try:
            if User.objects.filter(email=self.username).exists():
                raise ObjectAlreadyExists
        except ObjectAlreadyExists as exc:
            if raise_exception:
                raise exc
            else:
                return False

        return True

class UserToolKit:
    @classmethod
    def create_user(cls, username, password):
        user = UserCreator(password=password, username=username)()
        return user

    @classmethod
    def authenticate_user(cls, email, password):
        user = authenticate(email=email, password=password)
        if not user:
            qs = User.objects.filter(email=email)
            if qs.exists() and not qs.first().is_active:
                raise ValidationError(UserErrorMessages.DISABLED_USER_ERROR.value)
            raise ValidationError(UserErrorMessages.CREDENTIALS_ERROR.value)

        return user, Token.objects.get_or_create(user=user)[0]