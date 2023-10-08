from django.db import models
from users.models import User

# Create your models here.

class Owner(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class Podcast(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category)
    author = models.CharField(max_length=50, null=True)
    rssOwner = models.CharField(max_length=50, null=True, blank=True)
    websiteUrl = models.URLField(max_length=255, null=True, blank=True)
    isExplicitContent = models.CharField(max_length=5, default="no")
    copyright = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    contentType = models.CharField(max_length=10, null=True, blank=True)
    pubDate = models.DateTimeField(auto_now_add=True)
    imageUrl = models.URLField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    duration = models.CharField(max_length=25)
    pubDate = models.DateTimeField()
    explicit = models.CharField(max_length=5, default="no")
    summary = models.TextField(null=True, blank=True)
    audioUrl = models.URLField(max_length=300)
    # keywords = models.TextField(null=True, blank=True)
    imageUrl = models.URLField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.title
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    def __str__(self):
        return f"{self.user | self.message}"