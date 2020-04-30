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
    

    @commands.command()
    @commands.check(is_bot_owner)
    async def servers(self, ctx):
        print(self.bot.guilds)
        await ctx.send('Checked my servers.')
    

    @commands.command()
    @commands.check(is_bot_owner)
    async def reloadcogs(self, ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
        await ctx.send('Reloaded cogs!')


def setup(bot):
    bot.add_cog(BotOwner(bot))
