from django.urls import path

from users.views import user_views, hockey_views


urlpatterns = [
    path('create', user_views.create_user_api),
    path('login', user_views.authenticate_user_api),
    path('hockey_player/create', hockey_views.create_hockey_player),
    path('test', hockey_views.get_6_best_players)
]