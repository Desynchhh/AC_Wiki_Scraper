import discord
from discord.ext import commands

import json

from helpers.checks import is_owner
from helpers.serversettings import Serversettings

class ServerOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['setp'])
    @commands.check(is_owner)
    async def setprefix(self, ctx, *, prefix):
        serversettings = Serversettings().load()
        
        guild_id = str(ctx.guild.id)
        if guild_id in serversettings:
            serversettings[guild_id]['prefix'] = prefix
        else:
            serversettings[guild_id] = {'prefix': prefix}

        Serversettings().update(serversettings)
        
        await ctx.send(f'New prefix is `{prefix}`')
    
    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You have to specify a new prefix to use for your server.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("Only the server owner can use that command.")


    @commands.command(aliases=['seth'])
    @commands.check(is_owner)
    async def sethemisphere(self, ctx, hemisphere:str):
        hemisphere = hemisphere.lower()
        valid_hemispheres = Serversettings().get_valid_hemispheres()
        if hemisphere in valid_hemispheres['northern'] or hemisphere in valid_hemispheres['southern']:
            for hs in valid_hemispheres:
                if hemisphere in hs:
                    hemisphere = hs
            serversettings = Serversettings().load()
            
            guild_id = str(ctx.guild.id)
            if guild_id in serversettings:
                serversettings[guild_id]['hemisphere'] = hemisphere
            else:
                serversettings[guild_id] = {"hemisphere": hemisphere}
            
            Serversettings().update(serversettings)
            
            await ctx.send(f'The default hemisphere is now `{hemisphere}`')
        
        else:
            raise Exception('HemisphereDoesNotExist')

    @sethemisphere.error
    async def sethemisphere_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('You have to specify a hemisphere to use as the default hemisphere for your server.')

        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("Only the server owner can use that command.")

        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            if error.original.args[0] == 'HemisphereDoesNotExist':
                await ctx.send('The hemisphere you have chosen does not exist. You can only choose between northern and southern.')

def setup(bot):
    bot.add_cog(ServerOwner(bot))