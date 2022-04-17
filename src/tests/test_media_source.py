from unittest import TestCase
from media.media_source import SpotifySource, YoutubeSource


class MediaSourceTestCase(TestCase):

    def test_get_by_link(self):
        url = 'https://www.youtube.com/watch?v=_FrOQC-zEog'
        expected_result = {
            'source': 'https://www.youtube.com/wa',
            'title': 'Pink Floyd - Comfortably numb',
            'creator': 'Pink Floyd'}
        result = YoutubeSource.get_by_link(url)
        self.assertEqual(expected_result['title'], result['title'])

    def test_get_info_from_spotify_link(self):
        test_cases = [
            {
                'arguments': 'https://open.spotify.com/track/2lzLPRS5gmpUX9gZjPxidy?si=137ec770855f4924',
                'expected_result': {'type': 'track', 'name': 'Imanbek, Goodboys - Goodbye'}
            },
            {
                'arguments': 'https://open.spotify.com/playlist/175UbpiDbRSKD3Thd9Nn5d?si=cc94c10c47d34ff5',
                'expected_result': {
                                    'type': 'playlist',
                                    'name': 'TestPlaylist',
                                    'tracks': [
                                        {'type': 'track', 'name': 'Nirvana - Smells Like Teen Spirit'},
                                        {'type': 'track', 'name': 'Nirvana - Something In The Way'},
                                        {'type': 'track', 'name': 'Nirvana - Come As You Are'}
                                    ]
                                 }
            },
            {
                'arguments': 'https://open.spotify.com/album/3HbSqZwfzLchCol9LCWKNP?si=NXVD2Up3STa85Hk5VtkLMw',
                'expected_result': {
                    'type': 'album', 'name': 'Марабу',
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
            },
            {
                'arguments': 'https://open.spotify.com/song/2lzLPRS5gZjPxidy?si=137ec770855f4924',
                'expected_result': 'Unknown spotify url'
            },
        ]
        for test_case in test_cases:
            result = SpotifySource.get_info_from_spotify_link(test_case['arguments'])
            self.assertEqual(test_case['expected_result'], result)