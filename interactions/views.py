from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.auth import JwtAuthentication
from podcasts.models import Episode, Podcast
from .serializers import *

# Create your views here.

class LikeView(APIView):
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

            return Response(data={"message": "succeded"}, status=status.HTTP_201_CREATED)
        
    def liked_list(self, request, *args, **kwargs):
        liked = Like.objects.filter(user=request.user)
        return Response({"Liked": list(liked)}, status=status.HTTP_200_OK)