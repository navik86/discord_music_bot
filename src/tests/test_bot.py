from unittest import TestCase
from bot.bot import MusicBot
from src.media.bot_commands import commands_list


class MusicBotTestCase(TestCase):

    def test_register_commands(self):
        bot = MusicBot([commands_list])
        self.assertEqual(8, len(bot.commands))
