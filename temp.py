from discord import FFmpegOpusAudio
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os

import util


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')
FFMPEG_OPTIONS = {'before_options': '''-reconnect 1 -reconnect_streamed 1
                  -reconnect_delay_max 5''', 'options': '-vn'}

bot = commands.Bot(command_prefix='-')
queue = []


@bot.command()
async def fetch(ctx, message):
    response = util.search_wiki(message)
    if response:
        await ctx.send(response)


@bot.command()
async def show(ctx, message):
    response = util.find_photo(message)
    if response:
        await ctx.send(response)


@bot.command()
async def summon(ctx):
    voice = get(ctx.guild.voice_channels, name='general')
    await voice.connect()


@bot.command()
async def retrieve(ctx, search_title):
    voice = get(bot.voice_clients, guild=ctx.guild)
    url, song_title, duration = util.ydl_source(search_title)
    source = await FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)

    if voice.is_playing():
        queue.append(source)
        message = "As you wish, the next song is: "

    else:
        voice.play(source,
                   after=lambda x=None:
                   check_reserve(ctx))
        message = "Will now play: "

    await ctx.send(message + song_title)


def check_reserve(ctx):
    if queue:
        voice = get(bot.voice_clients, guild=ctx.guild)
        source = queue.pop(0)
        voice.play(source)


@bot.command()
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()

    check_reserve(ctx)


@bot.command()
async def recommence(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        return


@bot.command()
async def halt(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
    else:
        response = "Haven't played anything yet "
        title, name = util.polite_address(ctx.author)

        response += title + " " + name
        print(response)


@bot.command()
async def cease(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
    else:
        return


@bot.command()
async def depart(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_connected():
        await voice.disconnect()
    else:
        return


bot.run(TOKEN)
