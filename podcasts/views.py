from django.http import Http404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from users.auth import JwtAuthentication
from .models import Podcast, Episode
from .tasks import save_single_podcast
from config.publisher import Publisher
from .serializers import PodcastSerializer, EpisodeSerializer
from .utils import recommended_podcasts

# Create your views here.

publisher = Publisher()

class EpisodeListView(generics.ListCreateAPIView):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        queryset = Episode.objects.all()
        publisher.publish("Listing all Episodes...", queue="podcast-update")
        return queryset
    

class PodcastListView(APIView):
    
    def get(self, request) :
        queryset = Podcast.objects.all()
        serializer = PodcastSerializer(queryset, many=True)
        publisher.publish("Listing all Podcasts...", queue="podcast-update")
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PodcastDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PodcastSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = Podcast.objects.filter(pk=pk)

        if not queryset.exists():
            publisher.error_publish("Podcast does Not Exist!", queue="podcast-update")
            raise Http404("Podcast not found")
        
        publisher.publish("Podcast Detail is Shown.", queue="podcast-update")
        return queryset.first()
    

class EpisodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EpisodeSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        queryset = Episode.objects.filter(pk=pk)

        if not queryset.exists():
            publisher.error_publish("Episode does Not Exist!", queue="podcast-update")
            raise Http404("Podcast episode not found!")
        
        publisher.publish("Episode Detail is Shown.", queue="podcast-update")
        return queryset.first()
    

class PodcastRecommendationAPIView(APIView):
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        function = self.recommended_podcasts
        publisher.publish("Showing Recommendations ...", queue="podcast-update")
        return Response(function(user))
    

class AddPodcastView(APIView):
    authentication_classes = [JwtAuthentication,]
    permission_classes=[IsAuthenticated,]

    def post(self, request):
        data = request.data['url']
        if not data:
            raise Response({'message':str(_('URL is invalid!'))}, status=status.HTTP_400_BAD_REQUEST)
        save_single_podcast.delay(data)
        return Response({"message":str(_("Rss file save in database successfully."))}, status.HTTP_201_CREATED)