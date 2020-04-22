import discord
from discord.ext import commands

from helpers.checks import is_owner, is_admin
from scraper import run_scraper

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    @commands.check(is_owner)
    async def updatejson(self, ctx):
        run_scraper()
        await ctx.send('Updated JSON data')
    
    @updatejson.error
    async def updatejson_error(self, ctx, error):
        await ctx.send('Oops! Looks like only the owner can run this command.')


def setup(client):
    client.add_cog(Owner(client))
