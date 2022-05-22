from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.errors import ObjectAlreadyExists, ValidationError
from users.services import HockeyPlayerToolKit
from users.serializers import HockeyPlayerSerializer
from users.models import HockeyPlayer


@api_view(["POST"])
def create_hockey_player(request):
    data = request.POST or request.data

    try:
        name = data['name'] 
        second_name = data['second_name']
        patronymic = data['patronymic']
        birthday = data['birthday']
        abandoned_pucks = data['abandoned_pucks']
        passes = data['passes']
        penalty_minutes = data['penalty_minutes']
    except KeyError:
        return Response({'error': 'REQUEST_FIELDS_ERROR'}, status=400)

    try:
        hockey_player = HockeyPlayerToolKit.create(
            name=name,
            second_name=second_name,
            patronymic=patronymic,
            birthday=birthday,
            abandoned_pucks=abandoned_pucks,
            passes=passes,
            penalty_minutes=penalty_minutes
        )
    except ObjectAlreadyExists:
        return Response({"error": "HOCKEY_PLAYER_WITH_THIS_NAME_ALREADY_EXISTS"}, status=400)
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)

    serializer = HockeyPlayerSerializer(instance=hockey_player)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def get_6_best_players(request):
    best = HockeyPlayer.objects.order_by('-passes', '-abandoned_pucks')[:6]

    serializer = HockeyPlayerSerializer(instance=best, many=True)
    return Response(serializer.data, status=200)