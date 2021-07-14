from django.contrib import admin
from .models import User, Album, Song

admin.site.register(Album)
admin.site.register(Song)
