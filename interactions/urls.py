from django.urls import path
from .views import LikeAPIView, CommentAPIView, SubscribeView, PlaylistAPIView


urlpatterns = [
    path("like/", LikeAPIView.as_view(), name="like"),
    path("comment/", CommentAPIView.as_view(), name="comment"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("playlist/", PlaylistAPIView.as_view(), name="playlist"),
]