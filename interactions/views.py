from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.auth import JwtAuthentication
from podcasts.models import Episode, Podcast
from .serializers import *

# Create your views here.

class LikeAPIView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def create(self, request):
        like_serializer = LikeSerializer(data = request.data)
        like_serializer.is_valid(raise_exception=True)
        user = request.user
        episode_id = request.data.get("episode_id")

        try:
            existing_like = Like.objects.get(user=user, episode=episode_id)
            existing_like.delete()
            return Response({"detail": "Like removed successfully."}, status=status.HTTP_200_OK)
        
        except Like.DoesNotExist:

            if like_serializer.validated_data.get("model")=="podcast":
                podcast = Podcast.objects.get(id = like_serializer.validated_data.get("model_id"))
                if podcast:
                    like = Like(content_object = podcast, account = request.user)
                    like.save()

            elif like_serializer.validated_data.get("model") == "episode":
                episode = Episode.objects.get(id = like_serializer.validated_data.get("model_id"))
                if episode:
                    like = Like(content_object = episode, account = request.user)
                    like.save()

            return Response(data={"message": "succeeded"}, status=status.HTTP_201_CREATED)
        
    def liked_list(self, request, *args, **kwargs):
        liked = Like.objects.filter(user=request.user)
        return Response({"Liked": list(liked)}, status=status.HTTP_200_OK)
    

class CommentAPIView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        comment_serializer = CommentSerializer(data = request.data)
        comment_serializer.is_valid(raise_exception=True)

        if comment_serializer.validated_data.get("model")=="podcast":
            try:
                podcast = Podcast.objects.get(id= comment_serializer.validated_data.get("model_id"))
            except Podcast.DoesNotExist:
                return Response({"error": "Podcast not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if podcast:
                comment = Comment(content_object = podcast, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()

        elif comment_serializer.validated_data.get("model")=="episode":
            try:
                episode = Episode.objects.get(id= comment_serializer.validated_data.get("model_id"))
            except Episode.DoesNotExist:
                return Response({"error": "Episode not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if episode:
                comment = Comment(content_object= episode, account= request.user, text= comment_serializer.validated_data.get("text"))
                comment.save()

        return Response(data={"message":"succeeded"}, status=status.HTTP_201_CREATED)
    


class PlaylistAPIView(APIView):
    authentication_classes = [JwtAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        DATA =  request.data.copy()
        DATA["account"] = request.user
        DATA.pop("playlist")
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True ,instance=Playlist.objects.get(id=request.data.get("playlist")))
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()
        return Response(data={"message":"succeeded"}, status=status.HTTP_201_CREATED)
    

class SubscribeView(generics.ListCreateAPIView):
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        subscribe_serializer = SubscribeSerializer(data = request.data)
        podcast = Podcast.objects.get(id= subscribe_serializer.validated_data.get("model_id"))
        user = request.user

        try:
            already_subscribed = Subscribe.objects.get(user=user, podcast=podcast)
            already_subscribed.delete()
            return Response({"message": "unsubscribed"}, status=status.HTTP_200_OK)
        
        except Subscribe.DoesNotExist:
            subscribe_data = {"user": user.id, "podcast": podcast}
            serializer = self.get_serializer(data=subscribe_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

