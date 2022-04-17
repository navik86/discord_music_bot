from src.bot.bot import MusicBot
from src.media.bot_commands import commands_list


def main():
    bot = MusicBot([commands_list])
    print(bot.commands)
    bot.run()


if __name__ == "__main__":
    main()
