import discord
from discord.ext import commands

from helpers.checks import is_owner
from helpers.serversettings import Serversettings
from logger import log_command

class ServerOwner(commands.Cog):
    def __init__(self, bot:discord.ext.commands.Bot):
        self.bot = bot
    
    @commands.command(aliases=['setp'])
    @commands.check(is_owner)
    async def setprefix(self, ctx:discord.ext.commands.Context, *, prefix:str):
        """Used to set a custom prefix for individual servers, in case it has multiple bots using the same prefix.

        :type ctx: discord.ext.commands.Context
        :type prefix: str
        """
        await log_command(ctx, "setprefix", prefix)
        serversettings = Serversettings().load()
        
        guild_id = str(ctx.guild.id)
        if guild_id in serversettings:
            serversettings[guild_id]['prefix'] = prefix
        else:
            serversettings[guild_id] = {'prefix': prefix}

        Serversettings().update(serversettings)
        
        await ctx.send(f'New prefix is `{prefix}`')
    
    @setprefix.error
    async def setprefix_error(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors for the 'sethemisphere' method. Sends out an informing message to the relevant discord channel.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You have to specify a new prefix to use for your server.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("Only the server owner can use that command.")


    @commands.command(aliases=['seth'])
    @commands.check(is_owner)
    async def sethemisphere(self, ctx:discord.ext.commands.Context, hemisphere:str):
        """Used to set the default hemisphere for individual servers, in case the majority of server members live on one hemisphere.

        :type ctx: discord.ext.commands.Context
        :type hemisphere: str
        :raises Exception: HemisphereDoesNotExist. The method could not find the given hemisphere in the serversettings JSON file.
        """
        await log_command(ctx, "sethemisphere", hemisphere)
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
            raise Exception('HemisphereDoesNotExist', hemisphere)

    @sethemisphere.error
    async def sethemisphere_error(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors for the 'sethemisphere' method. Sends out an informing message to the relevant discord channel.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('You have to specify a hemisphere to use as the default hemisphere for your server.')

        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("Only the server owner can use that command.")

        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            if error.original.args[0] == 'HemisphereDoesNotExist':
                await ctx.send('The hemisphere you have chosen does not exist. You can only choose between northern and southern.')

def setup(bot:discord.ext.commands.Bot):
    bot.add_cog(ServerOwner(bot))