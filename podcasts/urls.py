from django.urls import path
from .views import PodcastListView, PodcastDetailView, EpisodeListView, EpisodeDetailView, PodcastRecommendationAPIView

urlpatterns = [
    path("podcasts/", PodcastListView.as_view(), name="podcast-list-create"),
    path("podcasts/<int:pk>/", PodcastDetailView.as_view(), name="podcast-detail"),
    path("podcasts/<int:pk>/episodes/", EpisodeListView.as_view(), name="podcast-episodes-list-create"),
    path("episodes/<int:pk>/", EpisodeDetailView.as_view(), name="episode-detail"),
    path("recommends/", PodcastRecommendationAPIView.as_view(), name="recommends"),
]