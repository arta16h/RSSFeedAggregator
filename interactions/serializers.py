from rest_framework.serializers import ModelSerializer
from .models import Like, Comment, Subscribe, Playlist, Bookmark


class SubscribeSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = [
            "user",
            "podcast",
            "created_at",
            "updated_at",
        ]

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = [
            "user",
            "episode",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "user",
            "episode",
            "content",
            "created_at",
            "updated_at",
        ]


class PlaylistSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            "title",
            "description",
            "user",
            "podcasts",
            "episodes",
            "created_at",
            "updated_at",
        ]
        
    def update(self, instance, validated_data):
        for podcast in validated_data.get("podcasts"):
            instance.podcasts.add(podcast)
        for episode in validated_data.get("episodes"):
            instance.episodes.add(episode)
        instance.save()
        return instance
    

class BookmarkSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            "user",
            "episode",
        ]