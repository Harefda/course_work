from django.urls import path

from users import views


urlpatterns = [
    path('create', views.create_user_api),
    path('login', views.authenticate_user_api),
]