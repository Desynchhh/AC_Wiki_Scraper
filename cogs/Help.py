import discord
from discord.ext import commands

from datetime import datetime

from helpers.checks import is_owner
from helpers.serversettings import get_prefix, get_hemisphere

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_colour = 0xF9D048
    
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            prefix = get_prefix(ctx)
            
            e = discord.Embed(title=f'{self.bot.user.name} Help Command', colour=self.embed_colour, description="When looking up specific commands, arguments in (parentheses) are required, and arguments in [brackets] are optional.")
            e.add_field(name='General Commands',value=
                f"{prefix}help - Shows this message. You can also get more detailed help on each command.\n"
                f"{prefix}fish - Shows information on a specified fish.\n"
                f"{prefix}bug - Shows information on a specified bug.\n"
                f"{prefix}prevmonth - Shows all critters you could catch last month.\n"
                f"{prefix}thismonth - Shows all critters you can catch this month.\n"
                f"{prefix}nextmonth - Shows all critters you can catch next month.\n",
            inline=False)

            if is_owner(ctx):
                e.add_field(name='Owner Commands', value=
                    f"{prefix}sethemisphere - Sets the default hemisphere for your server when running commands.\n"
                    f"{prefix}setprefix - Sets a custom prefix for this bot on your server.",
                inline=False)
            
            e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=e)
    

    @help.command()
    async def fish(self, ctx):
        prefix = get_prefix(ctx)
        hemisphere = get_hemisphere(ctx)
        e = discord.Embed(title=f'**{prefix}fish (name) [hemisphere]**', colour=self.embed_colour)
        e.add_field(name=f'Shows information on the given fish.', value=
            "You need to type the fish's name **without** spaces or symbols (such as dashes) for the command to work.\n"
            "**name**: Name of the fish you wish to know about.\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}fish popeyedgoldfish southern", 
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    
    @help.command()
    async def bug(self, ctx):
        prefix = get_prefix(ctx)
        hemisphere = get_hemisphere(ctx)
        e = discord.Embed(title=f'**{prefix}bug (name) [hemisphere]**', colour=self.embed_colour)
        e.add_field(name='Shows information on a specified bug.', value=
            "You need to type the bug's name **without** spaces or symbols (such as dashes) for the command to work.\n"
            "**name**: Name of the bug you wish to know about.\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}bug commonbutterfly northern",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command()
    async def prevmonth(self, ctx):
        prefix = get_prefix(ctx)
        hemisphere = get_hemisphere(ctx)
        e = discord.Embed(title=f'**{prefix}prevmonth (critter type) [hemisphere]**', colour=self.embed_colour)
        e.add_field(name='Shows all critters you could catch last month.',value=
            "**critter type**: The type of critter you wish you could have caught (fish or bugs).\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}prevmonth bugs southern",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command()
    async def thismonth(self, ctx):
        prefix = get_prefix(ctx)
        hemisphere = get_hemisphere(ctx)
        e = discord.Embed(title=f'**{prefix}thismonth (critter type) [hemisphere]**', colour=self.embed_colour)
        e.add_field(name='Shows all critters you can catch this month.',value=
            "**critter type**: The type of critter you want to catch (fish or bugs).\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}thismonth fish southern",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command()
    async def nextmonth(self, ctx):
        prefix = get_prefix(ctx)
        hemisphere = get_hemisphere(ctx)
        e = discord.Embed(title=f'**{prefix}nextmonth (critter type) [hemisphere]**', colour=self.embed_colour)
        e.add_field(name='Shows all critters you can catch next month.',value=
            "**critter type**: The type of critter you want to catch (fish or bugs).\n"
            "**hemisphere**: You can choose either the northern or southern hemisphere for this command.\n"
            f"**Example**: {prefix}nextmonth bugs northern",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command()
    @commands.check(is_owner)
    async def setprefix(self, ctx):
        prefix = get_prefix(ctx)
        hemisphere = get_hemisphere(ctx)
        e = discord.Embed(title=f'**{prefix}setprefix (new prefix)**', colour=self.embed_colour)
        e.add_field(name='Sets a custom prefix for this bot on your server.',value=
            "**new prefix**: The prefix you want to use for this bot on this server.\n"
            f"**Example**: {prefix}setprefix !",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @help.command()
    @commands.check(is_owner)
    async def sethemisphere(self, ctx):
        prefix = get_prefix(ctx)
        hemisphere = get_hemisphere(ctx)
        e = discord.Embed(title=f'**{prefix}sethemisphere (hemisphere)**', colour=self.embed_colour)
        e.add_field(name='Sets the default hemisphere for your server when running commands.',value=
            "**hemisphere**: The main hemisphere you want to be used on this server (has to be either 'northern' or 'southern').\n"
            f"**Example**: {prefix}sethemisphere northern",
        inline=False)
        e.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    
def setup(bot):
    bot.add_cog(Help(bot))