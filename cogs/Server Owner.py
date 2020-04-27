import discord
from discord.ext import commands

import json

from helpers.checks import is_owner

serversettings_path = 'serversettings.json'

class ServerOwner(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.check(is_owner)
    async def setprefix(self, ctx, *, prefix):
        """Set a custom prefix for the bot on this server.
        Example: >sethemisphere !"""
        with open(serversettings_path, 'r') as f:
            serversettings = json.load(f)
        
        guild_id = str(ctx.guild.id)
        if guild_id in serversettings:
            serversettings[guild_id]['prefix'] = prefix
        else:
            serversettings[guild_id] = {'prefix': prefix}

        with open(serversettings_path, 'w') as f:
            json.dump(serversettings, f)
        
        await ctx.send(f'New prefix is `{prefix}`')


    @commands.command()
    @commands.check(is_owner)
    async def sethemisphere(self, ctx, hemisphere:str):
        """Set the default hemisphere for this server.
        By default, the bot will always get statistics from the northern hemisphere. Use this command to change the default to the southern hemisphere.
        Example: >sethemisphere northern"""
        hemisphere = hemisphere.lower()
        if hemisphere == 'northern' or hemisphere == 'southern':
            with open(serversettings_path, 'r') as f:
                serversettings = json.load(f)
            
            guild_id = str(ctx.guild.id)
            if guild_id in serversettings:
                serversettings[guild_id]['hemisphere'] = hemisphere
            else:
                serversettings[guild_id] = {"hemisphere": hemisphere}
            
            with open(serversettings_path, 'w') as f:
                json.dump(serversettings, f)
            
            await ctx.send(f'The default hemisphere is now `{hemisphere}`')
        
        else:
            await ctx.send("You can only set the hemisphere to either northern or southern!")


def setup(client):
    client.add_cog(ServerOwner(client))