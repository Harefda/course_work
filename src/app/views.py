from django.shortcuts import render, redirect


def main_page(request):
    return render(request, "main.html")

def login_page(request):
    return render(request, "login.html")

def signin_page(request):
    return render(request, "signin.html")