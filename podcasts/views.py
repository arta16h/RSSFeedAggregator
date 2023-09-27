from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Podcast, Episode
from .serializers import PodcastSerializer, EpisodeSerializer

# Create your views here.

class EpisodeListView():
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        queryset = Episode.objects.all()
        return queryset
    

class PodcastListView(generics.ListCreateAPIView):
    serializer_class = PodcastSerializer

    def get_queryset(self):
        queryset = Podcast.objects.all()
        return queryset