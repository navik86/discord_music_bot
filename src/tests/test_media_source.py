import ast
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from media.media_source import SpotifySource, YoutubeSource


class MediaSourceTestCase(TestCase):

    @patch('media.media_source.YTMusic')
    def test_get_by_search(self, mock_ytm_client):

        with open('ytm_client_search_example', 'r') as f:
            body = f.read()

        list_info = ast.literal_eval(body)

        temp_mock = mock_ytm_client()
        temp_mock.search.return_value = list_info

        expected_url = 'https://www.youtube.com/watch?v=ljUtuoFt-8c'

        self.assertEqual(
            expected_url,
            YoutubeSource.get_by_search('Smells Like Teen Spirit')
        )

    @patch('media.media_source.YoutubeDL')
    def test_get_by_link(self, mock_youtube_dl):

        with open('youtube_dl_example', 'r') as f:
            body = f.read()

        dict_info = ast.literal_eval(body)

        context_manager = mock_youtube_dl()
        ydl = context_manager.__enter__()
        ydl.extract_info.return_value = dict_info

        expected_result = {
            'source': 'https://rr4---sn-coct-hn9e.googlevideo.com/videoplayback?expire=1650938722&ei=Av9mYpvhJMXm7gP5pL3YBw&ip=178.172.134.197&id=o-APN2qplzLvPAnPD5-2XiC5KHdV8YB3uvCEIPwt5pNhq0&itag=249&source=youtube&requiressl=yes&mh=jF&mm=31%2C29&mn=sn-coct-hn9e%2Csn-8ph2xajvh-n8vs&ms=au%2Crdu&mv=m&mvi=4&pl=24&pcm2=no&gcr=by&initcwndbps=817500&spc=4ocVCyI1tediMz2p_I1qjaEOvXB-&vprv=1&mime=audio%2Fwebm&ns=Hq5MOIctluL600lMnAGn338G&gir=yes&clen=1789063&dur=301.941&lmt=1574994272020984&mt=1650916851&fvip=6&keepalive=yes&fexp=24001373%2C24007246&c=WEB&txp=5531432&n=sp9RWH9eR0SjTzTdv&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cpcm2%2Cgcr%2Cspc%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhANqbLCxHPWAQh9u3ra2aSuZi7hIKCHJi_Wfivu743hzOAiBtTmTKuLIWWNxfKFiMunp_5imU9oydW0Ca20XhQEJZNw%3D%3D&sig=AOq0QJ8wRQIgJOVNEnjTUcmurEFNjxkgt0orsEJ-MctNy2M7tEif16UCIQD8KnMgaI3Ee0EKde1iglx7Xg3OBjpciE1BA3q7ICoyMw==',
            'title': 'Smells Like Teen Spirit',
            'creator': 'Nirvana',
        }

        self.assertEqual(
            expected_result,
            YoutubeSource.get_by_link('https://www.youtube.com/watch?v=ljUtuoFt-8c')
        )

    @patch('media.media_source.spotify_client')
    def test_get_info_from_spotify_link_track(self, mock_spotify_client):

        with open('spotify_client_track_example', 'r') as f:
            body = f.read()

        dict_info = ast.literal_eval(body)
        mock_spotify_client.track.return_value = dict_info

        expected_result = {'type': 'track', 'name': 'Imanbek, Goodboys - Goodbye'}

        self.assertEqual(
            expected_result,
            SpotifySource.get_info_from_spotify_link_track('si=137ec770855f4924')
        )

    @patch('media.media_source.spotify_client')
    def test_get_info_from_spotify_link_playlist(self, mock_spotify_client):

        with open('spotify_client_playlist_example', 'r') as f:
            body = f.read()

        dict_info = ast.literal_eval(body)
        mock_spotify_client.playlist.return_value = dict_info

        expected_result = {
                            'type': 'playlist',
                            'name': 'TestPlaylist',
                            'tracks': [
                                {'type': 'track', 'name': 'Nirvana - Smells Like Teen Spirit'},
                                {'type': 'track', 'name': 'Nirvana - Something In The Way'},
                                {'type': 'track', 'name': 'Nirvana - Come As You Are'}
                            ]
                         }

        self.assertEqual(
            expected_result,
            SpotifySource.get_info_from_spotify_link_playlist('si=cc94c10c47d34ff5')
        )

    @patch('media.media_source.spotify_client')
    def test_get_info_from_spotify_link_album(self, mock_spotify_client):

        with open('spotify__client_album_example', 'r') as f:
            body = f.read()

        dict_info = ast.literal_eval(body)
        mock_spotify_client.album.return_value = dict_info

        expected_result = {
                        'type': 'album',
                        'name': 'Марабу',
                        'tracks': [
                                {'type': 'track', 'name': 'ATL - Удобрением'},
                                {'type': 'track', 'name': 'ATL - Марабу'},
                                {'type': 'track', 'name': 'ATL - Искра'},
                                {'type': 'track', 'name': 'ATL - Ареола'},
                                {'type': 'track', 'name': 'ATL - Крокодил'},
                                {'type': 'track', 'name': 'ATL - Пчёлки'},
                                {'type': 'track', 'name': 'ATL - Паранойя'},
                                {'type': 'track', 'name': 'ATL - Пилюли'},
                                {'type': 'track', 'name': 'ATL - Демоны'},
                                {'type': 'track', 'name': 'ATL - Подснежник'}
                            ]
                        }

        self.assertEqual(
            expected_result,
            SpotifySource.get_info_from_spotify_link_album('si=86N_INzOSguIpkgzu-1KaQ')
        )


if __name__ == '__main__':
    main()
