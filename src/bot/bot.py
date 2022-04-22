from discord.ext import commands
from config.config import PREFIX, BOT_TOKEN
import queue

from utils.db_api import connection_db, show_top_5


class MusicBot(commands.Bot):

    def __init__(self, additional_commands=None):
        self.playback_queue = queue.Queue()
        self.current_track = None
        self._cogs = ["src.media.media"]
        super().__init__(
            command_prefix=PREFIX,
            case_insensitive=True,
        )
        self.setup()
        if additional_commands:
            self.register_commands(additional_commands)
        # self.connect_db()

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

    def show_top_5_tracks(self):
        return show_top_5()

    def run(self):
        print("Running src...")
        super().run(BOT_TOKEN, reconnect=True)

    # def connect_db(self):
    #     connection_db()

    async def on_ready(self):

        connection_db()
        print('Bot is ready!')
