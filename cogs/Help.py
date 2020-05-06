import discord
from discord.ext import commands

from helpers.checks import is_owner
from helpers.serversettings import Serversettings

class Help(commands.Cog):
    def __init__(self, bot:discord.ext.commands.Bot):
        self.bot = bot
        self.embed_colour = 0xF9D048
    
    @commands.group()
    async def help(self, ctx:discord.ext.commands.Context):
        """Group for all help commands for the bot.
        Sends out a general help message with a list of all commands if no command is specified.
        Sends out 'owner only' commands if it is invoked by the server owner.

        :type ctx: discord.ext.commands.Context
        """
        if ctx.invoked_subcommand is None:
            prefix = Serversettings().get_prefix(ctx.guild.id)
            
            e = discord.Embed(title=f'{self.bot.user.name} Help Command', colour=self.embed_colour, description="When looking up specific commands, arguments in <tags> are required, and arguments in [brackets] are optional.")
            e.add_field(name='General Commands',value=
                f"{prefix}help [command] - Shows this message. You can also get more detailed help on each command.\n"
                f"{prefix}fish <name> - Shows information on a specified fish.\n"
                f"{prefix}bug <name> - Shows information on a specified bug.\n"
                f"{prefix}prevmonth <critter type> [hemisphere] - Shows all fish/bugs you could catch last month.\n"
                f"{prefix}thismonth <critter type> [hemisphere] - Shows all fish/bugs you can catch this month.\n"
                f"{prefix}nextmonth <critter type> [hemisphere] - Shows all fish/bugs you can catch next month.\n",
            inline=False)

            if is_owner(ctx):
                e.add_field(name='Owner Commands', value=
                    f"{prefix}sethemisphere <hemisphere> - Sets the default hemisphere for your server when running commands.\n"
                    f"{prefix}setprefix <prefix> - Sets a custom prefix for this bot on your server.",
                inline=False)
            
            e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=e)
        
    @help.command(aliases=['help'])
    async def _help(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the help command. Helps users understand the help command.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        e = discord.Embed(title=f"**{prefix}help [command]**", colour=self.embed_colour)
        e.add_field(name="Shows a help message. You can also get more detailed help on each command.", value=
            "**command**: The command you want more detailed help with.\n"
            f"**Example**: {prefix}help thismonth", 
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
    

    @help.command(aliases=['f'])
    async def fish(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the fish command. Helps users understand the fish command.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        e = discord.Embed(title=f'**{prefix}fish <name>**', colour=self.embed_colour)
        e.add_field(name=f'Shows information on the given fish.', value=
            "You need to type the fish's name **exactly** how it's spelled in the game for the command to work (case insensitive).\n"
            "**name**: Name of the fish you wish to know about.\n"
            f"**Example**: {prefix}fish pop-eyed goldfish\n"
            "**Aliases**: fish, f",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    
    @help.command(aliases=['b'])
    async def bug(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the bug command. Helps users understand the bug command.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        e = discord.Embed(title=f'**{prefix}bug <name>**', colour=self.embed_colour)
        e.add_field(name='Shows information on a specified bug.', value=
            "You need to type the bug's name **exactly** how it's spelled in the game for the command to work (case insensitive).\n"
            "**name**: Name of the bug you wish to know about.\n"
            f"**Example**: {prefix}bug common butterfly\n"
            "**Aliases**: bug, b",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command(aliases=['pm', 'lastmonth', 'lm'])
    async def prevmonth(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the prevmonth command. Helps users understand the prevmonth command.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        hemisphere = Serversettings().get_hemisphere(ctx.guild.id)
        e = discord.Embed(title=f'**{prefix}prevmonth <critter type> [hemisphere]**', colour=self.embed_colour)
        e.add_field(name='Shows all critters you could catch last month.',value=
            "**critter type**: The type of critter you wish you could have caught (fish or bugs).\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}prevmonth fish southern\n"
            "**Aliases**: prevmonth, lastmonth, pm, lm",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command(aliases=['tm'])
    async def thismonth(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the thismonth command. Helps users understand the thismonth command.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        hemisphere = Serversettings().get_hemisphere(ctx.guild.id)
        e = discord.Embed(title=f'**{prefix}thismonth <critter type> [hemisphere]**', colour=self.embed_colour)
        e.add_field(name='Shows all critters you can catch this month.',value=
            "**critter type**: The type of critter you want to catch (fish or bugs).\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}thismonth bugs southern\n"
            "**Aliases**: thismonth, tm",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command(aliases=['nm'])
    async def nextmonth(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the nextmonth command. Helps users understand the nextmonth command.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        hemisphere = Serversettings().get_hemisphere(ctx.guild.id)
        e = discord.Embed(title=f'**{prefix}nextmonth <critter type> [hemisphere]**', colour=self.embed_colour)
        e.add_field(name='Shows all critters you can catch next month.',value=
            "**critter type**: The type of critter you want to catch (fish or bugs).\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}nextmonth bugs northern\n"
            "**Aliases**: nextmonth, nm",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command(aliases=['setp'])
    @commands.check(is_owner)
    async def setprefix(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the setprefix command. Helps users understand the setprefix command.
        Can only be invoked by the server owner.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        e = discord.Embed(title=f'**{prefix}setprefix <new prefix>**', colour=self.embed_colour)
        e.add_field(name='Sets a custom prefix for this bot on your server.',value=
            "**new prefix**: The prefix you want to use for this bot on this server. It can be anything you want!.\n"
            f"**Example**: {prefix}setprefix !\n"
            "**Aliases**: setprefix, setp",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command(aliases=['seth'])
    @commands.check(is_owner)
    async def sethemisphere(self, ctx:discord.ext.commands.Context):
        """A detailed help command for the sethemisphere command. Helps users understand the sethemisphere command.
        Can only be invoked by the server owner.

        :type ctx: discord.ext.commands.Context
        """
        prefix = Serversettings().get_prefix(ctx.guild.id)
        hemisphere = Serversettings().get_hemisphere(ctx.guild.id)
        e = discord.Embed(title=f'**{prefix}sethemisphere <hemisphere>**', colour=self.embed_colour)
        e.add_field(name='Sets the default hemisphere for your server when running commands.',value=
            "**hemisphere**: The main hemisphere you want to be used on this server (has to be either 'northern' or 'southern').\n"
            f"**Example**: {prefix}sethemisphere northern\n"
            "**Aliases**: sethemisphere, seth",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    
def setup(bot:discord.ext.commands.Bot):
    bot.add_cog(Help(bot))