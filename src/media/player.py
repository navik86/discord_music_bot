import discord
from discord.ext import commands
from .media_source import YoutubeSource
from .music_queue import MUSIC_QUEUE


@commands.command(pass_context=True)
async def join(ctx):
    """Командует присоединиться к войсу"""
    channel = ctx.message.author.voice.channel
    voice = ctx.guild.voice_client

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@commands.command()
async def show_queue(ctx):
    pass


@commands.command()
async def play(ctx, *args):
    """Поиск музыки и добавление в очередь"""
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Connect to a voice channel!")
    else:
        yts = YoutubeSource()
        song = yts.get_by_search(query)
        if type(song) != type(True):
            await ctx.send("Could not download the song")
        else:
            await ctx.send("Song added to the queue")
            MUSIC_QUEUE.append([song, voice_channel])


@commands.command()
async def pause(ctx):
    """Ставит музыку на паузу"""
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
    else:
        await ctx.channel(f'{ctx.author.mention}, Музыка не воспроизводится')


@commands.command()
async def stop(ctx):
    """Прекращает воспроизведение музыки"""
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)  # получаем текущее соединение
    voice.stop()


@commands.command()
async def skip(ctx):
    pass


@commands.command()
async def leave(ctx):
    """Командует выйти из войса"""
    voice = discord.utils.get(ctx.bot.voice_clients, quild=ctx.guild)

    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, бот уже отключен от войса')


PLAY_COMMANDS = [
    join,
    play,
    pause,
    stop,
    leave,
]

