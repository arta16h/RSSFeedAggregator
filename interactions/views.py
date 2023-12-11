from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from users.auth import JwtAuthentication
from podcasts.models import Episode, Podcast
from .models import Bookmark, Viewed, Episode, Subscribe, Playlist
from .serializers import *
from podcasts.serializers import EpisodeSerializer

# Create your views here.

class LikeAPIView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        like_serializer = LikeSerializer(data = request.data)
        like_serializer.is_valid(raise_exception=True)
        user = request.user
        episode_id = request.data.get("episode_id")

        try:
            already_liked = Like.objects.get(user=user, episode=episode_id)
            already_liked.delete()
            return Response({"detail": _("Like removed successfully.")}, status=status.HTTP_200_OK)
        
        except Like.DoesNotExist:

            if like_serializer.validated_data.get("model")=="podcast":
                podcast = Podcast.objects.get(id = like_serializer.validated_data.get("id"))
                if podcast:
                    like = Like(content_object = podcast, account = request.user)
                    like.save()

            elif like_serializer.validated_data.get("model") == "episode":
                episode = Episode.objects.get(id = like_serializer.validated_data.get("id"))
                if episode:
                    like = Like(content_object = episode, account = request.user)
                    like.save()
            return Response(data={"message": "succeeded"}, status=status.HTTP_201_CREATED)
        
    def liked_list(self, request, *args, **kwargs):
        liked = Like.objects.filter(user=request.user).values_list("episode__id", flat=True)
        return Response({"Liked": list(liked)}, status=status.HTTP_200_OK)
    

class CommentAPIView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        comment_serializer = CommentSerializer(data = request.data)
        comment_serializer.is_valid(raise_exception=True)

        if comment_serializer.validated_data.get("model")=="podcast":
            try:
                podcast = Podcast.objects.get(id= comment_serializer.validated_data.get("id"))
            except Podcast.DoesNotExist:
                return Response({"error": _("Podcast not found.")}, status=status.HTTP_404_NOT_FOUND)
            
            if podcast:
                comment = Comment(content_object = podcast, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()

        elif comment_serializer.validated_data.get("model")=="episode":
            try:
                episode = Episode.objects.get(id= comment_serializer.validated_data.get("id"))
            except Episode.DoesNotExist:
                return Response({"error": _("Episode not found.")}, status=status.HTTP_404_NOT_FOUND)
            
            if episode:
                comment = Comment(content_object= episode, account= request.user, text= comment_serializer.validated_data.get("text"))
                comment.save()

        return Response(data={"message":_("succeeded")}, status=status.HTTP_201_CREATED)
    


class PlaylistAPIView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        DATA =  request.data.copy()
        user = request.user
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True ,instance=Playlist.objects.get(id=request.data.get("playlist")))
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()
        return Response(data={"message":_("succeeded")}, status=status.HTTP_201_CREATED)

    def playlist_list(self, request, *args, **kwargs) :
        playlists = Playlist.objects.filter(user = request.user)
        return Response({"playlists", list(playlists)}, status=status.HTTP_200_OK)

class SubscribeView(generics.ListCreateAPIView):
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Subscribe.objects.all()

    def post(self, request, *args, **kwargs):
        podcast = Podcast.objects.get(id= request.data.get("podcast_id"))
        user = request.user

        try:
            already_subscribed = Subscribe.objects.get(user=user, podcast=podcast)
            already_subscribed.delete()
            return Response({"message": _("unsubscribed")}, status=status.HTTP_200_OK)
        
        except Subscribe.DoesNotExist:
            subscribe_data = {"user": user.id, "podcast": podcast.id}
            subscribe_serializer = SubscribeSerializer(data = subscribe_data)
            # serializer = self.get_serializer(data=subscribe_data)
            if subscribe_serializer.is_valid():
                subscribe_serializer.save()
                return Response(subscribe_serializer.data, status=status.HTTP_201_CREATED)
            return Response(subscribe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def subscribed_list(self, request, *args, **kwargs):
        subscried = Subscribe.objects.filter(user=request.user).values_list("podcast__id", flat=True)
        return Response({"Subscribed": list(subscried)}, status=status.HTTP_200_OK)
    

class BookmarkAPIView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        bookmark_serializer = BookmarkSerializer(data = request.data)
        bookmark_serializer.is_valid(raise_exception=True)
        user = request.user
        episode_id = request.data.get("episode_id")

        try:
            already_bookmarked = Bookmark.objects.get(user=user, episode=episode_id)
            already_bookmarked.delete()
            return Response({"detail": _("Bookmark removed successfully.")}, status=status.HTTP_200_OK)
        
        except Bookmark.DoesNotExist:
            episode = Episode.objects.get(id = bookmark_serializer.validated_data.get("episode_id"))
            if episode:
                bookmark = Bookmark(content_object = episode, account = request.user)
                bookmark.save()
            return Response(data={"message": _("succeeded")}, status=status.HTTP_201_CREATED)
        
    def bookmarked_list(self, request, *args, **kwargs):
        bookmarked = Bookmark.objects.filter(user=request.user).values_list("episode__id", flat=True)
        return Response({"Bookmarked": list(bookmarked)}, status=status.HTTP_200_OK)
    

class ViewedEpisodesAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        user = self.request.user
        viewed_episodes = Viewed.objects.filter(user=user).values_list("episode", flat=True)
        queryset = Episode.objects.filter(id__in=viewed_episodes)
        return queryset