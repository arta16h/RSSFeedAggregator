from django.http import Http404

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
    

class PodcastDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PodcastSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = Podcast.objects.filter(pk=pk)
        if not queryset.exists():
            raise Http404("Podcast not found")
        return queryset.first()