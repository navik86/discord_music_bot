from discord import Embed
from discord.ext import commands
from src.media.media_source import YoutubeSource, SpotifySource


@commands.command()
async def track(ctx):
    """Показывает текущий трек в очереди"""
    voice = ctx.guild.voice_client

    if voice is None:
        desc = 'Нет треков для проигрывания, используйте команду !play'
        embed = Embed(title="Текущий трек:", description=desc, color=0x00ff00)
        await ctx.channel.send(embed=embed)
    else:
        track_name = ctx.bot.current_track[0]['title']
        creator_name = ctx.bot.current_track[0]['creator']
        embed = Embed(
            title="Текущий трек: ",
            description=" ",
            color=0x00ff00
        )
        embed.add_field(name=track_name, value=creator_name, inline=False)
        show_queue = ctx.bot.playback_queue.queue
        if len(show_queue) > 0:
            embed.add_field(name="------------------", value="Очередь проигрывания:", inline=False)
            counter = 1
            for i in show_queue:
                embed.add_field(name=f"{counter}. {i[0]['title']}", value=i[0]['creator'], inline=False)
                counter += 1
        await ctx.channel.send(embed=embed)


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

    if query.startswith('https://www.youtu'):
        data = YoutubeSource.get_by_link(query)
        if type(data) is list:
            [queue.put((i, voice_channel)) for i in data]
            await ctx.send("Треки добавлены в очередь")
        else:
            queue.put((data, voice_channel))
            await ctx.send("Трек добавлен в очередь")

    elif query.startswith('https://open.spoti'):
        data = SpotifySource.get_by_link(query)
        if type(data) is list:
            [queue.put((i, voice_channel)) for i in data]
            await ctx.send("Треки добавлены в очередь")
        else:
            queue.put((data, voice_channel))
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