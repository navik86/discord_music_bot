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
        return url

    @classmethod
    def get_by_link(cls, url):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        return {'source': info['formats'][0]['url'], 'title': info['title'], 'creator': info['creator']}


class SpotifySource(MediaSource):

    @classmethod
    def get_by_search(cls, search_query):
        pass

    @classmethod
    def get_by_link(cls, url):
        spotify_playlist = []

        try:
            spotify_link_info = cls.get_info_from_spotify_link(url)
        except spotipy.SpotifyException:
            return "Что то пошло не так"

        if spotify_link_info['type'] == 'track':
            url = YoutubeSource.get_by_search(spotify_link_info['name'])
            return YoutubeSource.get_by_link(url)
        else:
            # если это плейлист или альбом Spotify
            for track in spotify_link_info['tracks']:
                try:
                    url = YoutubeSource.get_by_search(track['name'])
                    info = YoutubeSource.get_by_link(url)
                    spotify_playlist.append(info)
                except IndexError:
                    return "Один из треков не найден"

            # если не все треки найдены, возврат
            if len(spotify_playlist) == 0:
                return
            return spotify_playlist

    @classmethod
    def get_info_from_spotify_link(cls, url):

        try:
            link_type = url.split('/')[3]
            _id = url.split('/')[4]
            if '?' in _id:
                _id = _id[:_id.index('?')]
        except IndexError:
            return 'Unknown spotify url'

        # получение информации о треке в зависимости от типа ссылки
        if link_type == 'track':
            cls.get_info_from_spotify_link_track(_id)

        elif link_type == 'album':
            cls.get_info_from_spotify_link_album(_id)

        elif link_type == 'playlist':
            cls.get_info_from_spotify_link_playlist(_id)
        else:
            return 'Unknown spotify url'

    @classmethod
    def get_info_from_spotify_link_track(cls, _id):
        information = spotify_client.track(_id)
        print(information)
        track_name = ''
        for artist in information['artists']:
            if information['artists'].index(artist) == 0:
                track_name += artist['name']
            else:
                track_name += ', ' + artist['name']
        track_name += ' - ' + information['name']

        return {
            'type': 'track',
            'name': track_name
        }

    @classmethod
    def get_info_from_spotify_link_album(cls, _id):
        information = spotify_client.album(_id)
        print(information)
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
            })

        return {
            'type': 'album',
            'name': information['name'],
            'tracks': tracks
        }

    @classmethod
    def get_info_from_spotify_link_playlist(cls, _id):
        information = spotify_client.playlist(_id)
        print(information)
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
                'name': track_name
            })

        return {
            'type': 'playlist',
            'name': information['name'],
            'tracks': tracks
        }