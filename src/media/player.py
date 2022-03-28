from discord.ext import commands
from .media_source import YoutubeSource
from .music_queue import MUSIC_QUEUE


@commands.command()
async def play(ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Connect to a voice channel!")
    else:
        yts = YoutubeSource()
        song = yts.get_by_search(query)
        if type(song) == type(True):
            await ctx.send("Could not download the song")
        else:
            await ctx.send("Song added to the queue")
            MUSIC_QUEUE.append([song, voice_channel])


@commands.command()
async def pause(ctx):
    pass


@commands.command()
async def stop(ctx):
    pass


@commands.command()
async def leave(ctx):
    pass


PLAY_COMMANDS = [
    play,
    pause,
    stop,
    leave,
]

