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

    FFMPEG_OPTIONS = {'before_options': '''-reconnect 1 -reconnect_streamed 1
                  -reconnect_delay_max 5''', 'options': '-vn'}

    queue = {}

    @commands.command(brief=brief_summon)
    async def summon(self, ctx):
        voice = get(ctx.guild.voice_channels, name='general')
        await voice.connect()

    # This is the play command
    @commands.command(brief=brief_retrieve, description=brief_retrieve)
    async def retrieve(self, ctx, search_title):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        # Takes the url, song title and the duration from the ydl and
        # transforms it into a ffmpegopus object
        url, song_title, duration = util.ydl_source(search_title)
        source = await FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)

        # The condtions list to check if the audio is to be added to the
        # playlist or to be played immediately

        title, name = util.polite_address(ctx.message.author)

        conditions = [voice.is_playing(),
                      voice.is_paused()]

        if any(conditions):
            if song_title in self.queue.keys():
                song_title += "* "
            self.queue[song_title] = source
            message = f"As you wish, {title} {name} the next song is: "
        else:
            voice.play(source, after=lambda x=None: self.check_reserve(ctx))
            message = f" As requested by {title} {name} I will now play: "

        await ctx.send(f"{message} {song_title}")

    # The check_reserve checks if there are songs in the playlist and plays it
    # if there are,until it finishes
    def check_reserve(self, ctx):
        if self.queue:
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            # Takes the next song in the playlist and then removes it
            # from the plylist
            source = self.queue.pop(next(iter(self.queue)))
            voice.play(source, after=lambda x=None: self.check_reserve(ctx))

    # Takes the next song in the playlist and plays it
    @commands.command(brief=brief_next)
    async def next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()

        self.check_reserve(ctx)

    # Removes the song from the playlist
    @commands.command(brief=brief_obliterate)
    async def obliterate(self, ctx, message):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        url, song_title, duration = util.ydl_source(message)

        conditions = [voice.is_playing(),
                      voice.is_paused()]

        title, name = util.polite_address(ctx.message.author)

        if any(conditions):
            await ctx.send("Looking......")
            # Uses the song titles extracted from ydl and then
            # check it from the playlist if it's present
            # removes the matching song from the playlist
            keyremove = [key for key, val in self.queue.items()
                         if song_title in key]

            if keyremove:
                self.queue.pop(keyremove[0])

            await ctx.send(f"Of course {title}")
            await ctx.send(f"I will obliterate {song_title} at once")
        else:
            await ctx.send(f"Apologies {title} {name}")
            await ctx.send(f"I cannot find {song_title} in the reserves")

    # Resumes the playlist if it has been paused
    @commands.command(brief=brief_recommence)
    async def recommence(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_paused():
            voice.resume()
        else:
            return

    # Pauses the playlist
    @commands.command(brief=brief_halt)
    async def halt(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
        else:
            return

    # Stops the playlist
    @commands.command(brief=brief_cease)
    async def cease(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
        else:
            return

    # Tells the bot to leave the voice chat
    @commands.command(brief=brief_depart)
    async def depart(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_connected():
            await voice.disconnect()
        else:
            return


def setup(bot):
    bot.add_cog(Music(bot))
