from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.utils import UserErrorMessages
from app.errors import ObjectAlreadyExists, ValidationError
from users.services import (
    UserToolKit,
    UserCreator
)


@api_view(["POST"])
def create_user_api(request, *args, **kwargs):
    data = request.POST or request.data

    try:
        username = data['username']
        first_name = data['first_name']
        second_name = data['second_name']
        password = data['password']
    except KeyError:
        return Response({'error': UserErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    try:
        user = UserToolKit.create_user(
            username,
            first_name,
            second_name,
            password
        )
    except ValidationError as exc:
        return Response({'error': str(exc)}, status=400)
    except Val:
        return Response({'error': UserErrorMessages.NON_UNIQUE_EMAIL_ERROR.value}, status=400)

    serializer = UserSerializer(instance=user)
    return Response(serializer.data, status=201)