from discord.ext import commands

import util


class Wiki(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fetch(self, ctx, message):
        response = util.search_wiki(message)
        if response:
            await ctx.send(response)

    @commands.command()
    async def show(self, ctx, message):
        response = util.find_photo(message)
        if response:
            await ctx.send(response)


def setup(bot):
    bot.add_cog(Wiki(bot))
