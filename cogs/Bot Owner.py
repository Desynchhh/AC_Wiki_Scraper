import discord
from discord.ext import commands

from helpers.checks import is_bot_owner
from scraper import run_scraper

class BotOwner(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    @commands.check(is_bot_owner)
    async def updatejson(self, ctx):
        run_scraper()
        await ctx.send('Updated JSON data')
    
    @updatejson.error
    async def updatejson_error(self, ctx, error):
        await ctx.send('Oops! Looks like only the bot owner can run this command.')


def setup(client):
    client.add_cog(BotOwner(client))
