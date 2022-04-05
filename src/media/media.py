import discord
from discord.ext import commands
from src.media.bot_commands.bot_commands import play, skip


class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.vc = ''
        self.is_playing = False

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if self.is_playing is True:
            return
        if (ctx.command == play or ctx.command == skip) and self.bot.playback_queue.qsize() > 0:
            await self.playback()

    async def playback(self):
        if self.bot.playback_queue.qsize() > 0:
            self.is_playing = True
            self.bot.current_track = self.bot.playback_queue.get()
            url = self.bot.current_track[0]['source']
            voice_channel = self.bot.current_track[1]

            if self.vc == "" or not self.vc.is_connected() or self.vc is None:
                self.vc = await voice_channel.connect()
            else:
                await self.vc.move_to(voice_channel)

            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    def play_next(self):
        if self.bot.playback_queue.qsize() > 0:
            self.is_playing = True
            item = self.bot.playback_queue.get()
            url = item[0]['source']
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False


def setup(bot):
    bot.add_cog(Media(bot))