import discord
from discord.ext import commands

from helpers.checks import is_bot_owner
from scraper import run_scraper

class BotOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.check(is_bot_owner)
    async def updatejson(self, ctx):
        run_scraper()
        await ctx.send('Updated JSON data')


def setup(bot):
    bot.add_cog(BotOwner(bot))
