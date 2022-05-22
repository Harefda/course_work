from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.errors import ObjectAlreadyExists, ValidationError


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