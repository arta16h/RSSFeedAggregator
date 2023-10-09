import logging
from django.http import Http404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.utils import JwtHelper
from .models import Podcast, Episode
from .serializers import PodcastSerializer, EpisodeSerializer
from .utils import like_based_recomended_podcasts, subscription_based_recommended_podcasts

# Create your views here.

logger = logging.getLogger('django_API')

class EpisodeListView(generics.ListCreateAPIView):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        queryset = Episode.objects.all()
        logger.info("listing all episodes!")
        return queryset
    

class PodcastListView(APIView):
    
    def get(self, request) :
        queryset = Podcast.objects.all()
        serializer = PodcastSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    

class PodcastDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PodcastSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = Podcast.objects.filter(pk=pk)
        if not queryset.exists():
            raise Http404("Podcast not found")
        return queryset.first()
    

class EpisodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EpisodeSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = Episode.objects.filter(pk=pk)
        if not queryset.exists():
            raise Http404("Podcast episode not found")
        return queryset.first()
    

class PodcastRecommendationAPIView(APIView):
    authentication_classes = (JwtHelper,)
    permission_classes = (IsAuthenticated,)

    recommendations_methods = {
        "likes": like_based_recomended_podcasts,
        "subscriptions": subscription_based_recommended_podcasts,
    }

    def get(self, request, method):
        if method not in self.recommendations_methods:
            return Response({"details":"Recommendation method not found"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        function = self.recommendations_methods[method]
        return Response(function(user))
    
