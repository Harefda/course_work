from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.utils import UserErrorMessages
from app.errors import ObjectAlreadyExists, ValidationError
from users.services import UserToolKit


@api_view(["POST"])
def create_user_api(request):
    data = request.POST or request.data

    try:
        username = data['username']
        password = data['password']
    except KeyError:
        return Response({'error': UserErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    try:
        user = UserToolKit.create_user(
            username,
            password
        )
    except ValidationError as exc:
        return Response({'error': str(exc)}, status=400)
    except ObjectAlreadyExists:
        return Response({'error': UserErrorMessages.NON_UNIQUE_EMAIL_ERROR.value}, status=400)

    serializer = UserSerializer(instance=user)
    return Response(serializer.data, status=201)

@api_view(["POST"])
def authenticate_user_api(request):
    data = request.POST or request.data

    username = data.get('username')
    password = data.get('password')

    try:
        user, token = UserToolKit.authenticate_user(
            username,
            password,
        )
    except ValidationError as exc:
        return Response({'error': str(exc)}, status=400)

    serializer = UserSerializer(instance=user)
    return Response(serializer.data, status=200)