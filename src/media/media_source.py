from abc import ABC, abstractmethod
from youtube_dl import YoutubeDL


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
}


class MediaSource(ABC):

    @abstractmethod
    def get_by_search(self, text):
        pass

    @abstractmethod
    def get_by_link(self, link):
        pass


class YoutubeSource(MediaSource):

    @classmethod
    def get_by_search(cls, item):
        pass

    @classmethod
    def get_by_link(cls, url):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        return {'source': info['formats'][0]['url'], 'title': info['title']}


class SpotifySource(MediaSource):
    pass