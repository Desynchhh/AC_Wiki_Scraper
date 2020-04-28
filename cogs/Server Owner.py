import discord
from discord.ext import commands

import json

from helpers.checks import is_owner
from helpers.serversettings import load_serversettings, update_serversettings

class ServerOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.check(is_owner)
    async def setprefix(self, ctx, *, prefix):
        """Set a custom prefix for the bot on this server.
        Example: >sethemisphere !"""
        serversettings = load_serversettings()
        
        guild_id = str(ctx.guild.id)
        if guild_id in serversettings:
            serversettings[guild_id]['prefix'] = prefix
        else:
            serversettings[guild_id] = {'prefix': prefix}

        update_serversettings(serversettings)
        
        await ctx.send(f'New prefix is `{prefix}`')


    @commands.command()
    @commands.check(is_owner)
    async def sethemisphere(self, ctx, hemisphere:str):
        """Set the default hemisphere for this server.
        By default, the bot will always get statistics from the northern hemisphere. Use this command to change the default to the southern hemisphere.
        Example: >sethemisphere northern"""
        hemisphere = hemisphere.lower()
        if hemisphere == 'northern' or hemisphere == 'southern':
            serversettings = load_serversettings()
            
            guild_id = str(ctx.guild.id)
            if guild_id in serversettings:
                serversettings[guild_id]['hemisphere'] = hemisphere
            else:
                serversettings[guild_id] = {"hemisphere": hemisphere}
            
            update_serversettings(serversettings)
            
            await ctx.send(f'The default hemisphere is now `{hemisphere}`')
        
        else:
            await ctx.send("You can only set the hemisphere to either northern or southern!")


def setup(bot):
    bot.add_cog(ServerOwner(bot))