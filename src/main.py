from src.bot.bot import MusicBot
from src.media.bot_commands import commands_list
# from utils.db_api import connection_db


def main():
    bot = MusicBot([commands_list])
    # connection_db()
    bot.run()


if __name__ == "__main__":
    main()
