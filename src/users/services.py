from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import authenticate

from users.models import User, HockeyPlayer
from users.utils import UserErrorMessages
from app.errors import ValidationError, ObjectAlreadyExists


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
        return UserCreator(password=password, username=username)()

    @classmethod
    def authenticate_user(cls, email, password):
        user = authenticate(email=email, password=password)
        if not user:
            qs = User.objects.filter(email=email)
            if qs.exists() and not qs.first().is_active:
                raise ValidationError(UserErrorMessages.DISABLED_USER_ERROR.value)
            raise ValidationError(UserErrorMessages.CREDENTIALS_ERROR.value)

        return user, Token.objects.get_or_create(user=user)[0]


class HockeyPlayerCreator:
    def __init__(
        self,
        name,
        second_name,
        patronymic,
        birthday,
        abandoned_pucks,
        passes,
        penalty_minutes,
    ):
        self.name = name
        self.second_name = second_name
        self.patronymic = patronymic
        self.birthday = birthday
        self.abandoned_pucks = abandoned_pucks
        self.passes = passes
        self.penalty_minutes = penalty_minutes

    def __call__(self):
        if self.allowed_to_create():
            hockey_player = self.create()
            hockey_player.save()
            return hockey_player
        else:
            return None

    def create(self):
        return HockeyPlayer.objects.create(
            name=self.name,
            second_name=self.second_name,
            patronymic=self.patronymic,
            birthday=self.birthday,
            abandoned_pucks=self.abandoned_pucks,
            passes=self.passes,
            penalty_minutes=self.penalty_minutes,
        )

    def allowed_to_create(self):
        if HockeyPlayer.objects.filter(name=self.name).exists():
            raise ObjectAlreadyExists

        return True


class HockeyPlayerToolKit:
    @classmethod
    def create(
        cls,
        name,
        second_name,
        patronymic,
        birthday,
        abandoned_pucks,
        passes,
        penalty_minutes,
    ):
        return HockeyPlayerCreator(
            name=name,
            second_name=second_name,
            patronymic=patronymic,
            birthday=birthday,
            abandoned_pucks=abandoned_pucks,
            passes=passes,
            penalty_minutes=penalty_minutes,
        )()


# def get_6_best_hockey_players(*args, **kwargs):
#     return HockeyPlayer.objects.filter('+passes', '+abandoned_pucks')
