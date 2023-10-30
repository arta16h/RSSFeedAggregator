from django.http import Http404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.utils import JwtHelper
from .models import Podcast, Episode
from config.publisher_pod import Publisher
from .serializers import PodcastSerializer, EpisodeSerializer
from .utils import like_based_recomended_podcasts, subscription_based_recommended_podcasts

# Create your views here.

publisher = Publisher()

class EpisodeListView(generics.ListCreateAPIView):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        queryset = Episode.objects.all()
        publisher.publish("Listing all Episodes...", queue="podcast-update")
        # logger.info("listing all episodes!")
        return queryset
    

class PodcastListView(APIView):
    
    def get(self, request) :
        queryset = Podcast.objects.all()
        serializer = PodcastSerializer(queryset, many=True)
        publisher.publish("Listing all Podcasts...", queue="podcast-update")
        # logger.info("listing all podcasts!")
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PodcastDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PodcastSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = Podcast.objects.filter(pk=pk)

        if not queryset.exists():
            publisher.error_publish("Podcast does Not Exist!", queue="podcast-update")
            # logger.error("Podcast does not exist!")
            raise Http404("Podcast not found")
        
        publisher.publish("Podcast Detail is Shown.", queue="podcast-update")
        # logger.info("Podcast details is shown!")
        return queryset.first()
    

class EpisodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EpisodeSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = Episode.objects.filter(pk=pk)

        if not queryset.exists():
            publisher.error_publish("Episode does Not Exist!", queue="podcast-update")
            # logger.error("Episode does not exist!")
            raise Http404("Podcast episode not found!")
        
        publisher.publish("Episode Detail is Shown.", queue="podcast-update")
        # logger.info("Episode detail is shown!")
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
            publisher.error_publish("Method Not Found!", queue="podcast-update")
            # logger.error("Method not found!")
            return Response({"details":"Recommendation method not found"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        function = self.recommendations_methods[method]
        publisher.publish("Showing Recommendations Based on Your Method...", queue="podcast-update")
        # logger.info("Showing recomendations based on your method!")
        return Response(function(user))
    
