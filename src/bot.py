from discord.ext import commands

from src.config import config
from media.player import PLAY_COMMANDS


class MusicBot(commands.Bot):

    def __init__(self):
        self._cogs = ["src.media.media"]
        self.additional_commands = [PLAY_COMMANDS]
        super().__init__(
            command_prefix=config.PREFIX,
            case_insensitive=True,
        )

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(cog)
            print(f"Loaded {cog}")

        for item in self.additional_commands:
            for j in item:
                self.add_command(j)

        print("Setup complete.")

    def run(self):
        self.setup()
        print("Running src...")
        super().run(config.BOT_TOKEN, reconnect=True)

    async def on_ready(self):
        print('Bot is ready!')


