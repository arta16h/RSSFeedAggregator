from rest_framework import serializers
from .models import Podcast, Episode, Owner, Category

class OwnerSerializer(serializers.Serializer):
    class Meta:
        model = Owner
        fields = [
            "name",
            "email",
            "created_at",
            "updated_at",
        ]


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "created_at",
            "updated_at",
        ]


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = [
            "title",
            "description",
            "category",
            "author",
            "rssOwner",
            "websiteUrl",
            "isExplicitContent",
            "copyright",
            "language",
            "contentType",
            "pubDate",
            "imageUrl",
            "subtitle",
            "keywords",
        ]


class EpisodeSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Episode
        fields = [
            "podcast",
            "title",
            "description",
            "duration",
            "pubDate",
            "explicit",
            "summary",
            "audioUrl",
            "keywords",
        ]