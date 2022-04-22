import json
from abc import ABC, abstractmethod

import requests
import spotipy
from spotipy import SpotifyClientCredentials
from youtube_dl import YoutubeDL
from ytmusicapi import YTMusic

from src.config.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, YOUTUBE_TOKEN


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
        youtube_api_url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key={}"
        response = requests.get(youtube_api_url.format(search_query, YOUTUBE_TOKEN))
        text_attribute = response.text
        json_data = json.loads(text_attribute)
        tail = json_data['items'][0]['id']['videoId']
        url = 'https://www.youtube.com/watch?v=' + tail
        return url

    @classmethod
    def get_by_link(cls, url):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        print(info)
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
            return url
        else:
            # если это плейлист или альбом Spotify
            for track in spotify_link_info['tracks']:
                try:
                    url = YoutubeSource.get_by_search(track['name'])
                    spotify_playlist.append(url)
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
            information = spotify_client.track(_id)

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
                })

            return {
                'type': 'album',
                'name': information['name'],
                'tracks': tracks
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
                    'name': track_name
                })

            return {
                'type': 'playlist',
                'name': information['name'],
                'tracks': tracks
            }
        else:
            return 'Unknown spotify url'
