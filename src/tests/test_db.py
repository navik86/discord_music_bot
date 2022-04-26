import unittest
from unittest.mock import patch, MagicMock

from utils.db_api import check_track, connection_db


class DatabaseTest(unittest.TestCase):

    @patch('utils.db_api.connect')
    def test_check_track(self, connect_mock):

        con_mock = MagicMock()

        con_mock.execute.return_value.fetchone.return_value = ('Smells Like Teen Spirit')

        connection = MagicMock()
        connection.cursor.return_value.__enter__.return_value = con_mock

        connect_mock.return_value = connection

        connection_db()
        self.assertEqual(True, check_track('Smells Like Teen Spirit'))