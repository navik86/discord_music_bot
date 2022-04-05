from discord.ext import commands
from src.config import config
import queue

from src.media.bot_commands import commands_list


class MusicBot(commands.Bot):

    def __init__(self):
        self.playback_queue = queue.Queue()
        self.current_track = None
        self._cogs = ["src.media.media"]
        self.additional_commands = [commands_list]
        # self.additional_events = [events_list]
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

        # for item in self.additional_events:
        #     for j in item:
        #         self.add_listener(j)

        print("Setup complete.")

    def run(self):
        self.setup()
        print("Running src...")
        super().run(config.BOT_TOKEN, reconnect=True)

    async def on_ready(self):
        print('Bot is ready!')


