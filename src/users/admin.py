from django.contrib import admin

from users.models import User, HockeyPlayer

admin.site.register(User)
admin.site.register(HockeyPlayer)