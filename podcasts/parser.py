import requests
import xml.etree.ElementTree as ET
from django.db import transaction
from .models import Podcast, Episode

class Parser:
    def __init__(self, url) :
        self.response = requests.get(url)
        self.response.raise_for_status()
        self.xml_data = self.response.text
        self.root = ET.fromstring(self.xml_data)

    def rss_parser(self):
        root = self.root
        episodes = []

        try:
            podcast_metadata = {
                "title": "",
                "description": "",
                "author": "",
                "imageUrl": "",
                "rssOwner": "",
                "websiteUrl": "",
                "isExplicitContent": "",
                "copyright": "",
                "language": "",
                "contentType": "",
                "subtitle": "",
                "category": [],
                # "pubDate": "",
                # "keywords": "",
            }

            for item in root.findall(".//item"):
                episode = {
                    "title": item.findtext("title"),
                    "duration": item.findtext("itunes:duration", namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}),
                    "audioUrl": item.find("enclosure").get("url"),
                    "pubDate": item.findtext("pubDate"),
                    "explicit": item.findtext("itunes:explicit",namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}),
                    "imageUrl": item.findtext("itunes:image", namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}),
                    "summary": item.findtext("itunes:summary", namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}),
                    "description": item.findtext(".//content:encoded", namespaces={"content": "http://purl.org/rss/1.0/modules/content/"}),
                }

                explicit_element = item.find("itunes:explicit", namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
                if explicit_element is not None:
                    episode["explicit"] = explicit_element.text
                else:
                    episode["explicit"] = ""

                subtitle_element = item.find("itunes:subtitle", namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
                if subtitle_element is not None:
                    episode["subtitle"] = subtitle_element.text
                else:
                    episode["subtitle"] = ""
                episodes.append(episode)

            podcast_metadata["title"] = root.findtext("channel/title")
            podcast_metadata["description"] = root.findtext("channel/description")
            podcast_metadata["subtitle"] = root.findtext("channel/itunes:subtitle", 
                                                        namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
            podcast_metadata["author"] = root.findtext("channel/itunes:author",
                                                        namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
            podcast_metadata["imageUrl"] = root.findtext("channel/image/url")
            podcast_metadata["rssOwner"] = root.findtext("channel/itunes:owner/itunes:name", 
                                                            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
            podcast_metadata["websiteUrl"] = root.findtext("channel/link")
            podcast_metadata["isExplicitContent"] = root.findtext("channel/itunes:explicit",
                                                                namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
            podcast_metadata["copyright"] = root.findtext("channel/copyright")
            podcast_metadata["language"] = root.findtext("channel/language")
            podcast_metadata["contentType"] = root.findtext("channel/itunes:type",
                                                            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
            podcast_metadata["category"] = [
                category.text
                for category in root.findall("channel/itunes:category/itunes:category",
                                            namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})]
                       
            return {"podcast_metadata": podcast_metadata, "episodes": episodes}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching RSS feed: {e}")
            return None
        
    def save_podcast_to_db(self, data):
        podcast_metadata = data.get("podcast_metadata")
        episodes = data.get("episodes")
        with transaction.atomic():
            podcast, created = Podcast.objects.get_or_create(
                title=podcast_metadata["title"])

            podcast.description = podcast_metadata["description"]
            podcast.category = podcast_metadata["category"]
            podcast.subtitle = podcast_metadata["subtitle"]
            podcast.author = podcast_metadata["author"]
            podcast.imageUrl = podcast_metadata["imageUrl"]
            podcast.rssOwner = podcast_metadata["rssOwner"]
            podcast.websiteUrl = podcast_metadata["websiteUrl"]
            podcast.isExplicitContent = podcast_metadata["isExplicitContent"]
            podcast.language = podcast_metadata["language"]
            podcast.contentType = podcast_metadata["contentType"]
            podcast.save()

            episode_list = []
            for episode_data in episodes:
                if not Episode.objects.filter(podcast=podcast, audioUrl=episode_data["audioUrl"]).exists():
                    episode = Episode(
                        podcast=podcast,
                        title=episode_data["title"],
                        duration=episode_data["duration"],
                        audioUrl=episode_data["audioUrl"],
                        pubDate=episode_data["pubDate"],
                        explicit=episode_data["explicit"] == "yes",
                        imageUrl=episode_data.get("imageUrl", ""),
                        summary=episode_data["summary"],
                        description=episode_data["description"])
                    episode_list.append(episode)
            Episode.objects.bulk_create(episode_list)
