from unittest import TestCase, main
from bot.bot import MusicBot
from src.media.bot_commands import commands_list


class MusicBotTestCase(TestCase):

    def test_register_commands(self):
        bot = MusicBot([commands_list])
        self.assertEqual(9, len(bot.commands))

    def test_add_cog(self):
        bot = MusicBot([commands_list])
        self.assertIn('Media', bot.cogs)


if __name__ == '__main__':
    main()