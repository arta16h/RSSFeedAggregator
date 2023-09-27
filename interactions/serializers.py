from rest_framework.serializers import ModelSerializer
from .models import Like, Comment, Subscribe, Playlist


class SubscribeSerializer(ModelSerializer):
    class META:
        model = Subscribe
        fields = [
            "user",
            "podcast",
            "created_at",
            "updated_at",
        ]

class LikeSerializer(ModelSerializer):
    class META:
        model = Like
        fields = [
            "user",
            "episode",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(ModelSerializer):
    class META:
        model = Comment
        fields = [
            "user",
            "episode",
            "content",
            "created_at",
            "updated_at",
        ]


class PlaylistSerializer(ModelSerializer):
    class META:
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