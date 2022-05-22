from django.urls import path

from users.views import user_views


urlpatterns = [
    path('create', user_views.create_user_api),
    path('login', user_views.authenticate_user_api),
]