from pathlib import Path

from discord.ext import commands


class MusicBot(commands.Bot):

    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Setup complete.")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def on_ready(self):
        print('Bot is ready!')

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("!")(bot, msg)
