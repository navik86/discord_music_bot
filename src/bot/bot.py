from discord.ext import commands
from config import config
import queue


class MusicBot(commands.Bot):

    def __init__(self, additional_commands=None):
        self.playback_queue = queue.Queue()
        self.current_track = None
        self._cogs = ["src.media.media"]
        super().__init__(
            command_prefix=config.PREFIX,
            case_insensitive=True,
        )
        self.setup()
        if additional_commands:
            self.register_commands(additional_commands)

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(cog)
            print(f"Loaded {cog}")

        print("Setup complete.")

    def register_commands(self, additional_commands):

        for item in additional_commands:
            for j in item:
                self.add_command(j)

    def run(self):
        print("Running src...")
        super().run(config.BOT_TOKEN, reconnect=True)

    async def on_ready(self):
        print('Bot is ready!')


