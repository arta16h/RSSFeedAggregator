from django.contrib import admin
from .models import Owner, Category, Episode, Podcast

# Register your models here.

admin.site.register(Owner)
admin.site.register(Category)
admin.site.register(Episode)
admin.site.register(Podcast)