from discord import FFmpegOpusAudio
from discord.ext import commands
from discord.utils import get

import util


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    queue = []

    FFMPEG_OPTIONS = {'before_options': '''-reconnect 1 -reconnect_streamed 1
                  -reconnect_delay_max 5''', 'options': '-vn'}

    @commands.command()
    async def summon(self, ctx):
        voice = get(ctx.guild.voice_channels, name='general')
        await voice.connect()

    @commands.command()
    async def retrieve(self, ctx, search_title):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        url, song_title, duration = util.ydl_source(search_title)
        source = await FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)

        if voice.is_playing():
            self.queue.append(source)
            message = "As you wish, the next song is: "

        else:
            voice.play(source,
                       after=lambda x=None: self.check_reserve(ctx))
            message = "Will now play: "

        await ctx.send(message + song_title)

    def check_reserve(self, ctx):
        if self.queue:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            source = self.queue.pop(0)
            voice.play(source)

    @commands.command()
    async def next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()

        self.check_reserve(ctx)

    @commands.command()
    async def recommence(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            return

    @commands.command()
    async def cease(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
        else:
            return

    @commands.command()
    async def depart(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_connected():
            await voice.disconnect()
        else:
            return


def setup(bot):
    bot.add_cog(Music(bot))
