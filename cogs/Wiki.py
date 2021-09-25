from discord.ext import commands

import util


class Wiki(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    brief_inform = '''Takes the word and looks up the news on it, remember
                      to wrap the search item in quotation marks " " '''
    brief_fetch = '''Takes the word and looks up information associated with
                     the search item, remember to wrap the song in quotation
                     marks " " '''
    brief_show = '''Takes the word and looks up the photo associated with the
                    search item, remember to wrap the song
                    in quotation marks " " '''

    @commands.command(brief=brief_fetch, description=brief_fetch)
    async def fetch(self, ctx, message):
        response = util.search_wiki(message)
        if response:
            await ctx.send(response)

    @commands.command(brief=brief_show, description=brief_show)
    async def show(self, ctx, message):
        photos, response = util.find_photo(message)

        await ctx.send(response)

        if photos:
            for photo in photos:
                await ctx.send(photo)

    @commands.command(brief=brief_inform, description=brief_inform)
    async def inform(self, ctx, message):
        results = util.search_news(message)

        if results:
            for articles in results:
                title = "**" + articles['title'] + "**" + "\n"
                summary = articles['summary'] + "\n"
                media = articles['media'] + "\n"
                rights = "published by: " + articles['rights'] + "\n"
                date = "published: " + articles['published_date']

                await ctx.send(title + summary + media + rights + date)

        else:
            await ctx.send("No good current information on that")


def setup(bot):
    bot.add_cog(Wiki(bot))
