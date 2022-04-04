from abc import ABC, abstractmethod
import spotipy
from spotipy import SpotifyClientCredentials
from youtube_dl import YoutubeDL
from ytmusicapi import YTMusic


from src.config.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

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

spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))


class MediaSource(ABC):

    @abstractmethod
    def get_by_search(self, search_query):
        pass

    @abstractmethod
    def get_by_link(self, url):
        pass


class YoutubeSource(MediaSource):

    @classmethod
    def get_by_search(cls, search_query):
        ytm_client = YTMusic()
        url = 'https://www.youtube.com/watch?v=' + ytm_client.search(query=search_query, filter='songs')[0]['videoId']
        return cls.get_by_link(url)

    @classmethod
    def get_by_link(cls, url):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        return {'source': info['formats'][0]['url'], 'title': info['title']}


class SpotifySource(MediaSource):

    @classmethod
    def get_by_search(cls, search_query):
        pass

    @classmethod
    def get_by_link(cls, url):

        try:
            link_type = url.split('/')[3]
            _id = url.split('/')[4]
            if '?' in _id:
                _id = _id[:_id.index('?')]
        except IndexError:
            return 'Unknown spotify url'

        if link_type == 'track':
            information = spotify_client.track(_id)

            track_name = ''
            for artist in information['artists']:
                if information['artists'].index(artist) == 0:
                    track_name += artist['name']
                else:
                    track_name += ', ' + artist['name']
            track_name += ' - ' + information['name']

            return {
                'source': information['external_urls']['spotify'],
                'title': track_name
            }
        elif link_type == 'album':
            information = spotify_client.album(_id)

            tracks = []
            for track in information['tracks']['items']:
                track_name = ''
                for artist in track['artists']:
                    if track['artists'].index(artist) == 0:
                        track_name += artist['name']
                    else:
                        track_name += ', ' + artist['name']
                track_name += ' - ' + track['name']
                tracks.append({
                    'type': 'track',
                    'name': track_name,
                    'link': track['external_urls']['spotify']
                })

            return {
                'source': information['external_urls']['spotify'],
                'title': information['name']
            }
        elif link_type == 'playlist':
            information = spotify_client.playlist(_id)

            tracks = []
            for track in information['tracks']['items']:
                track_name = ''
                for artist in track['track']['artists']:
                    if track['track']['artists'].index(artist) == 0:
                        track_name += artist['name']
                    else:
                        track_name += ', ' + artist['name']
                track_name += ' - ' + track['track']['name']
                tracks.append({
                    'type': 'track',
                    'name': track_name,
                    'link': track['track']['external_urls']['spotify']
                })

            return {
                'source': information['external_urls']['spotify'],
                'title': information['name']
            }
        else:
            return 'Unknown spotify url'