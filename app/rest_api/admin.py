from django.contrib import admin
from django.contrib.admin.models import LogEntry
from rest_api.models import User, Image

admin.site.register(User)


admin.site.register(Image)