from rest_framework import serializers
from .models import Podcast, Episode


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