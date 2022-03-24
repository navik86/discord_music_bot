import wavelink
from discord.ext import commands


class MediaSource(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='127.0.0.1',
                                            port=2333,
                                            password="youshallnotpass")

@commands.command(name='play')
async def play_command(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc = ctx.voice_client
    await vc.play(search)


def setup(bot):
    bot.add_cog(MediaSource(bot))
