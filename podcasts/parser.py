import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from django.db import transaction
from .models import Podcast, Episode

class Parser:
    def __init__(self, file=None, path=None, url=None) :
        self.file = file
        self.path = path
        self.response = requests.get(url)
        self.response.raise_for_status()
        self.xml_data = self.response.text.replace("itunes:", "itunes_")
        self.base = ET.fromstring(self.xml_data)

    # def read_rss_file(self):
    #     with open(self.rss_path, "rt", encoding="utf-8") as f:
    #         file = f.read()
    #     return file

    def rss_parser(self):
        base = self.base
        episodes = []

        try:
            poddata = {}

            for item in base.findall(".//item"):
                episode = {
                    "title": item.findtext("title"),
                    "duration": item.findtext("itunes_duration"),
                    "audioUrl": item.find("enclosure").get("url"),
                    "pubDate": item.findtext("pubDate"),
                    "explicit": item.findtext("itunes_explicit"),
                    "imageUrl": item.findtext("itunes_image"),
                    "summary": item.findtext("itunes_summary"),
                    "description": item.findtext("description"),
                }
                explicit_element = item.find("itunes_explicit")

                if explicit_element is not None:
                    episode["explicit"] = explicit_element.text
                else:
                    episode["explicit"] = ""

                subtitle_element = item.find("itunes_subtitle")
                if subtitle_element is not None:
                    episode["subtitle"] = subtitle_element.text
                else:
                    episode["subtitle"] = ""
                episodes.append(episode)

            poddata["title"] = base.findtext("channel/title")
            poddata["description"] = base.findtext("channel/description")
            poddata["subtitle"] = base.findtext("channel/itunes_subtitle")
            poddata["author"] = base.findtext("channel/itunes_author")
            poddata["imageUrl"] = base.findtext("channel/image/url")
            poddata["rssOwner"] = base.findtext("channel/itunes_owner/itunes_name")
            poddata["websiteUrl"] = base.findtext("channel/link")
            poddata["isExplicitContent"] = base.findtext("channel/itunes_explicit")
            poddata["copyright"] = base.findtext("channel/copyright")
            poddata["language"] = base.findtext("channel/language")
            poddata["contentType"] = base.findtext("channel/itunes_type")
            poddata["category"] = [
                category.text
                for category in base.findall("channel/itunes_category/itunes_category")] 
            return {"poddata": poddata, "episodes": episodes}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching RSS feed: {e}")
            return None
        
    def save_podcast_to_db(self, data):
        poddata = data.get("poddata")
        episodes = data.get("episodes")
        with transaction.atomic():
            podcast = Podcast.objects.get_or_create(title=poddata["title"])[0]

            podcast.description = poddata["description"]
            podcast.subtitle = poddata["subtitle"]
            podcast.author = poddata["author"]
            podcast.imageUrl = poddata["imageUrl"]
            podcast.rssOwner = poddata["rssOwner"]
            podcast.websiteUrl = poddata["websiteUrl"]
            podcast.isExplicitContent = poddata["isExplicitContent"]
            podcast.language = poddata["language"]
            podcast.contentType = poddata["contentType"]
            podcast.save()

            for category in poddata["category"] :
                podcast.category.add(category)
            podcast.save()

            episode_titles = Episode.objects.filter(podcast=podcast).values_list("title")

            episode_list = []
            for episode_data in episodes:
                if not episode_data["title"] in episode_titles: 
                    episode = Episode(
                        podcast=podcast,
                        title=episode_data["title"],
                        duration=episode_data["duration"],
                        audioUrl=episode_data["audioUrl"],
                        pubDate= datetime.strptime(episode_data["pubDate"], "%a, %d %b %Y %H:%M:%S %z"),
                        explicit=episode_data["explicit"],
                        imageUrl=episode_data.get("imageUrl", ""),
                        summary=episode_data["summary"],
                        description=episode_data["description"])
                    episode_list.append(episode)
            Episode.objects.bulk_create(episode_list)
            