from discord.ext import commands
from src.media.media_source import YoutubeSource


@commands.command()
async def track(ctx):
    """Показывает текущий трек в очереди"""
    pass


@commands.command()
async def play(ctx, args):
    """Поиск музыки и добавление в очередь"""
    voice_channel = ctx.author.voice.channel
    data = YoutubeSource.get_by_link(args)
    queue = ctx.bot.playback_queue
    queue.put((data, voice_channel))


@commands.command()
async def pause(ctx):
    """Ставит музыку на паузу"""
    voice = ctx.guild.voice_client

    if voice.is_playing():
        voice.pause()
    else:
        await ctx.channel(f'{ctx.author.mention}, Музыка не воспроизводится')


@commands.command()
async def resume(ctx):
    """Продолжить воспроизведение музыки"""
    voice = ctx.guild.voice_client

    if voice.is_paused():
        voice.resume()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, Музыка уже играет')


@commands.command()
async def stop(ctx):
    """Прекращает воспроизведение музыки"""
    voice = ctx.guild.voice_client
    voice.stop()


@commands.command()
async def skip(ctx):
    """Пропустить песню"""
    voice = ctx.guild.voice_client
    if voice is not None:
        voice.stop()


@commands.command()
async def leave(ctx):
    """Командует выйти из войса"""
    voice = ctx.guild.voice_client

    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, бот уже отключен от войса')