from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Podcast, Episode
from .serializers import PodcastSerializer, EpisodeSerializer

# Create your views here.

class EpisodeListView():

    def get(self, request):
        queryset = Episode.objects.all()
        serializer_data = EpisodeSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)