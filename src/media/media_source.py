from abc import ABC, abstractmethod
from youtube_dl import YoutubeDL


class MediaSource(ABC):

    @abstractmethod
    def get_by_search(self, text):
        pass

    @abstractmethod
    def get_by_link(self, link):
        pass


# Find source
# Return source
class YoutubeSource(MediaSource):

    def __init__(self):
        self.YDL_OPTIONS = {
            'format': 'bestaudio',
            'noplaylist': 'True'
        }

    def get_by_search(self, item):

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def get_by_link(self, url):
        pass


class SpotifySource(MediaSource):
    pass