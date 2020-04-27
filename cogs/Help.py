import discord
from discord.ext import commands

from helpers.checks import is_owner

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            pass
    
    @help.command()
    async def fish(self, ctx):
        pass

    
    @help.command()
    async def bug(self, ctx):
        pass


    @help.command()
    async def prevmonth(self, ctx):
        pass


    @help.command()
    async def thismonth(self, ctx):
        pass


    @help.command()
    async def nextmonth(self, ctx):
        pass


    @help.command()
    @commands.check(is_owner)
    async def setprefix(self, ctx):
        pass


    @help.command()
    @commands.check(is_owner)
    async def sethemisphere(self, ctx):
        pass

    
def setup(client):
    client.add_cog(Help(client))