from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from users.models import User
from podcasts.models import Podcast, Episode


# Create your models here.

class Subscribe:
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class Like:
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class Comment:
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user
    

class Playlist:
    title = models.CharField(max_length=40)
    description = models.TextField(blank=False,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user")
    podcasts = models.ManyToManyField(Podcast)
    episodes = models.ManyToManyField(Episode)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title
    

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()