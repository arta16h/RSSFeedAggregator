from django.db.models import Q
from .parser import *
from .models import Podcast


def count_categories(podcasts):
    categories = {}
    for podcast in podcasts:
        category = podcast.main_fields.category
        categories.setdefault(category, 0)
        categories[category] += 1
    sorted_categories = {k:v for k,v in sorted(categories.items(), key=lambda item:item[1], reverse=True)}
    return sorted_categories


def recommended_podcasts(user):
    all_podcasts = Podcast.objects.all()
    user_podcasts = all_podcasts.filter(subscribe__user=user)
    sorted_categories = count_categories(user_podcasts)
    podcasts = all_podcasts.exclude(Q(subscribe__user=user)).filter(main_fields__category__in=sorted_categories.keys())
    podcasts_ids = list(podcasts.values_list("id", flat=True))
    return podcasts_ids

