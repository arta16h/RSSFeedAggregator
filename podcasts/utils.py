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