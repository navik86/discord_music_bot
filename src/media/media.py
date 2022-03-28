import discord
from discord.ext import commands
from .music_queue import MUSIC_QUEUE


class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.vc = ''
        self.is_playing = False

    async def play_back_handler(self):
        if len(MUSIC_QUEUE) > 0:
            self.is_playing = True

            m_url = MUSIC_QUEUE[0][0]['source']

            if self.vc == "" or not self.vc.is_connected() or self.vc is None:
                self.vc = await MUSIC_QUEUE[0][1].connect()
            else:
                await self.vc.move_to(MUSIC_QUEUE[0][1])

            print(MUSIC_QUEUE)

            MUSIC_QUEUE.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False


def setup(bot):
    bot.add_cog(Media(bot))