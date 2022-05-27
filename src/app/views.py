from django.shortcuts import render, redirect

from users.models import HockeyPlayer


def main_page(request):
    hockey_players = HockeyPlayer.objects.all()
    return render(request, "table.html", {"players": hockey_players})

def login_page(request):
    return render(request, "login.html")

def signin_page(request):
    return render(request, "signin.html")