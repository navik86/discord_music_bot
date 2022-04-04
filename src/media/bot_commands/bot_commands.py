from discord.ext import commands
from src.media.media_source import YoutubeSource


@commands.command()
async def track(ctx):
    """Показывает текущий трек в очереди"""
    pass


@commands.command()
async def play(ctx, *, query=None):
    """Поиск музыки и добавление в очередь"""
    queue = ctx.bot.playback_queue

    try:
        voice_channel = ctx.author.voice.channel
    except AttributeError:
        await ctx.send("Зайдите в голосовой канал")
        return

    if query is None:
        await ctx.send("После play укажите url или поисковый запрос")
        return

    if query.startswith('http'):
        print("if")
        data = YoutubeSource.get_by_link(query)
        queue.put((data, voice_channel))
        print(queue.qsize())
        await ctx.send("Трек добавлен в очередь")
    else:
        data = YoutubeSource.get_by_search(query)
        queue.put((data, voice_channel))
        await ctx.send("Трек добавлен в очередь")


@commands.command(aliases=['p'])
async def pause(ctx):
    """Ставит музыку на паузу"""
    voice = ctx.guild.voice_client

    if voice.is_playing():
        voice.pause()
    else:
        await ctx.channel(f'{ctx.author.mention}, Музыка не воспроизводится')


@commands.command(aliases=['r'])
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