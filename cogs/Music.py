from discord import FFmpegOpusAudio
from discord.ext import commands
from discord.utils import get

import util


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_depart = 'Oscar leaves the voice chat'
    brief_summon = 'Oscar is summoned to the voice chat'
    brief_retrieve = '''Takes the song and plays it, remember to wrap the song
                        in quotation marks " " '''
    brief_next = 'Plays the next song'
    brief_halt = 'Pauses the current song'
    brief_recommence = 'Resumes the song if it is paused'
    brief_cease = 'Stops the playlist'
    brief_obliterate = 'Removes a song from the playlist'

    queue = {}

    FFMPEG_OPTIONS = {'before_options': '''-reconnect 1 -reconnect_streamed 1
                  -reconnect_delay_max 5''', 'options': '-vn'}

    @commands.command(brief=brief_summon)
    async def summon(self, ctx):
        voice = get(ctx.guild.voice_channels, name='general')
        await voice.connect()

    @commands.command(brief=brief_retrieve, description=brief_retrieve)
    async def retrieve(self, ctx, search_title):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        url, song_title, duration = util.ydl_source(search_title)
        source = await FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)

        if voice.is_playing():
            self.queue[song_title] = source
            print(song_title)
            message = "As you wish, the next song is: "
        else:
            voice.play(source,
                       after=lambda x=None: self.check_reserve(ctx))
            message = "Will now play: "

        await ctx.send(message + song_title)

    def check_reserve(self, ctx):
        if self.queue:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            source = self.queue[next(iter(self.queue))]
            voice.play(source)

    @commands.command(brief=brief_next)
    async def next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()

        self.check_reserve(ctx)

    @commands.command(brief=brief_obliterate)
    async def obliterate(self, ctx, message):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        url, song_title, duration = util.ydl_source(message)

        if voice.is_playing():
            if song_title in self.queue.keys():
                self.queue.pop(song_title)
                await ctx.send("I will obliterate " + song_title + " at once")
        else:
            await ctx.send("I cannot find that in the reserves")

    @commands.command(brief=brief_recommence)
    async def recommence(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            return

    @commands.command(brief=brief_halt)
    async def halt(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            return

    @commands.command(brief=brief_cease)
    async def cease(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
        else:
            return

    @commands.command(brief=brief_depart)
    async def depart(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_connected():
            await voice.disconnect()
        else:
            return


def setup(bot):
    bot.add_cog(Music(bot))
