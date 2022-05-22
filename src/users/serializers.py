from rest_framework import serializers

from users.models import User, HockeyPlayer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class HockeyPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HockeyPlayer
        fields = [
            "name",
            "second_name",
            "patronymic",
            "birthday",
            "abandoned_pucks",
            "passes",
            "penalty_minutes",
        ]
