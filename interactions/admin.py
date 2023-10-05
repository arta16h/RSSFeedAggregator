from django.contrib import admin
from .models import Like, Subscribe, Playlist, Comment, Bookmark

# Register your models here.

admin.site.register(Like)
admin.site.register(Subscribe)
admin.site.register(Playlist)
admin.site.register(Comment)
admin.site.register(Bookmark)