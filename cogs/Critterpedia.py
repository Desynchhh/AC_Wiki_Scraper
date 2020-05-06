import discord
from discord.ext import commands

from helpers.jsonreader import get_critter, get_monthly_critters
from helpers.serversettings import Serversettings

class Critterpedia(commands.Cog):
    def __init__(self, bot:discord.ext.commands.Bot):
        self.bot = bot
        self.default_error_msg = "I am sorry, but something went wrong. I am uncertain whether it was something you did, or something I did hoo.."
        self.valid_critter_types = ['fish', 'bugs']


    @commands.command(aliases=['f'])
    async def fish(self, ctx:discord.ext.commands.Context, *, name:str):
        """Searches for the given fish in the local JSON files.
        If the fish is found, send out a formatted message with it's data.
        Else, raise an error.

        :type ctx: discord.ext.commands.Context
        :type name: str
        :raises Exception: NoFishFound. The method could not find the given fish in the JSON file.
        """
        fish = get_critter('fish', name)
        if fish is None:
            raise Exception('NoFishFound', name)

        message = f"""
{fish['name']}
Selling price: {fish['nook_price']}
C.J. selling price: {fish['cj_price']}
Location: {fish['location']}
Shadow size: {fish['shadow_size']}
Active hours: {fish['active_hours']}
Active months (northern): {'All year' if len(fish['months_available']['northern']) == 12 else ', '.join(fish['months_available']['northern'])}
Active months (southern): {'All year' if len(fish['months_available']['southern']) == 12 else ', '.join(fish['months_available']['southern'])}
More details at {fish['details_link']}"""
        await ctx.send(message)

    @fish.error
    async def fish_error(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors caused by the 'fish' method. Sends out an informing message to the relevant discord channel.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Uh oh! It seems you forgot to enter the name of the fish you are looking for hoo')
        
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            if error.original.args[0] == 'NoFishFound':
                await ctx.send(f"I am sorry, I was unable to find a fish called {error.original.args[1]}. Are you certain you spelled it's name correctly?")

        else:
            await ctx.send(self.default_error_msg)


    @commands.command(aliases=['b'])
    async def bug(self, ctx:discord.ext.commands.Context, *, name:str):
        """Searches for the given bug in the local JSON files.
        If the bug is found, send out a formatted message with it's data.
        Else, raise an error.

        :type ctx: discord.ext.commands.Context
        :type name: str
        :raises Exception: NoBugFound. The method could not find the given bug in the JSON file.
        """        
        bug = get_critter('bugs', name)
        if bug is None:
            raise Exception('NoBugFound', name)

        message = f"""
{bug['name']}
Selling price: {bug['nook_price']}
Flick selling price: {bug['flick_price']}
Location: {bug['location']}
Active hours: {bug['active_hours']}
Active months (northern): {'All year' if len(bug['months_available']['northern']) == 12 else ', '.join(bug['months_available']['northern'])}
Active months (southern): {'All year' if len(bug['months_available']['southern']) == 12 else ', '.join(bug['months_available']['southern'])}
More details at {bug['details_link']}"""
        await ctx.send(message)

    @bug.error
    async def bug_error(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors for the 'bug' method. Sends out an informing message to the relevant discord channel.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Uh oh! It seems you forgot to enter the name of the bug you are looking for hoo')
        
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            if error.original.args[0] == 'NoBugFound':
                await ctx.send(f"I'm afraid' I was unable to find a bug called {error.original.args[1]}. Are you certain you spelled it's name correctly?")

        else:
            await ctx.send(self.default_error_msg)


    @commands.command(aliases=['pm', 'lastmonth', 'lm'])
    async def prevmonth(self, ctx:discord.ext.commands.Context, critter_type:str, hemisphere:str=None):
        """Gets all of the given critter type that were available last month, the month before, and the month after.

        :type ctx: discord.ext.commands.Context
        :type critter_type: str
        :type hemisphere: str, optional
        :raises Exception: WrongCritterType. The user supplied a type of critter that does not exist within the game.
        """
        if critter_type in self.valid_critter_types:
            if hemisphere is None:
                hemisphere = Serversettings().get_hemisphere(ctx.guild.id)
            else:
                hemisphere = self._verify_hemisphere(hemisphere)
            critters = get_monthly_critters(critter_type, hemisphere, -2)
            
            e = discord.Embed(title=f"{critter_type.capitalize()} for {critters['this_month']} in the {hemisphere} hemisphere", colour=0xF9D048)
            e.add_field(
                name=f'{critter_type.capitalize()} that were active since {critters["prev_month"]}', 
                value=", ".join([critter['name'] for critter in critters['recurring_critters']]), 
                inline=False
            )

            e.add_field(
                name=f'{critter_type.capitalize()} that were new to {critters["this_month"]}!',
                value=", ".join([critter['name'] for critter in critters['new_critters']]),
                inline=False
            )
            
            e.add_field(
                name=f'{critter_type.capitalize()} that left in {critters["next_month"]}',
                value=', '.join([critter['name'] for critter in critters['leaving_critters']]),
                inline=False
            )
            
            await ctx.send(embed=e)

        else:
            raise Exception('WrongCritterType')
    
    @prevmonth.error
    async def prevmont_error(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors for the 'prevmonth' method. Sends out an informing message to the relevant discord channel.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        self.handle_month_errors(ctx, error)


    @commands.command(aliases=['tm'])
    async def thismonth(self, ctx:discord.ext.commands.Context, critter_type:str, hemisphere:str=None):
        """Gets all of the given critter type that are available this month, the last month, and the next month.

        :type ctx: discord.ext.commands.Context
        :type critter_type: str
        :type hemisphere: str, optional
        :raises Exception: WrongCritterType. The user supplied a type of critter that does not exist within the game.
        """
        if critter_type in self.valid_critter_types:
            if hemisphere is None:
                hemisphere = Serversettings().get_hemisphere(ctx.guild.id)
            else:
                hemisphere = self._verify_hemisphere(hemisphere)
            critters = get_monthly_critters(critter_type, hemisphere)
            
            e = discord.Embed(title=f"{critter_type.capitalize()} for {critters['this_month']} in the {hemisphere} hemisphere", colour=0xF9D048)
            e.add_field(
                name=f'{critter_type.capitalize()} that have stayed since {critters["prev_month"]}', 
                value=", ".join([critter['name'] for critter in critters['recurring_critters']]), 
                inline=False
            )

            e.add_field(
                name=f'{critter_type.capitalize()} that are new for {critters["this_month"]}!',
                value=", ".join([critter['name'] for critter in critters['new_critters']]),
                inline=False
            )

            e.add_field(
                name=f'{critter_type.capitalize()} that will be leaving in {critters["next_month"]}',
                value=', '.join([critter['name'] for critter in critters['leaving_critters']]),
                inline=False
            )

            await ctx.send(embed=e)
        
        else:
            raise Exception('WrongCritterType')
    
    @thismonth.error
    async def thismonth_error(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors for the 'thismonth' method. Sends out an informing message to the relevant discord channel.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        await self.handle_month_errors(ctx, error)
    

    @commands.command(aliases=['nm'])
    async def nextmonth(self, ctx:discord.ext.commands.Context, critter_type:str, hemisphere:str=None):
        """Gets all of the given critter type that are available this month, next month, and the month after.

        :type ctx: discord.ext.commands.Context
        :type critter_type: str
        :type hemisphere: str, optional
        :raises Exception: WrongCritterType. The user supplied a type of critter that does not exist within the game.
        """
        if critter_type in self.valid_critter_types:
            if hemisphere is None:
                hemisphere = Serversettings().get_hemisphere(ctx.guild.id)
            else:
                hemisphere = self._verify_hemisphere(hemisphere)
            critters = get_monthly_critters(critter_type, hemisphere, 0)
            
            e = discord.Embed(title=f"{critter_type.capitalize()} for {critters['this_month']} in the {hemisphere} hemisphere", colour=0xF9D048)
            e.add_field(
                name=f'{critter_type.capitalize()} that will stay after {critters["prev_month"]}', 
                value=", ".join([critter['name'] for critter in critters['recurring_critters']]), 
                inline=False
            )

            e.add_field(
                name=f'{critter_type.capitalize()} that will be new for {critters["this_month"]}!',
                value=", ".join([critter['name'] for critter in critters['new_critters']]),
                inline=False
            )
            
            e.add_field(
                name=f'{critter_type.capitalize()} that will be leaving in {critters["next_month"]}',
                value=', '.join([critter['name'] for critter in critters['leaving_critters']]),
                inline=False
            )

            await ctx.send(embed=e)
        
        else:
            raise Exception('WrongCritterType')
 
    @nextmonth.error
    async def nextmonth_error(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors for the 'nextmonth' method. Sends out an informing message to the relevant discord channel.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        await self.handle_month_errors(ctx, error)


    async def handle_month_errors(self, ctx:discord.ext.commands.Context, error:discord.ext.commands.errors.DiscordException):
        """Handles errors for the 'prevmonth', 'thismonth', and 'nextmonth' methods. These methods are the same of nature, and cause the same errors.

        :type ctx: discord.ext.commands.Context
        :type error: discord.ext.commands.errors.DiscordException
        """
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Hoo! You have to tell me whether you want to view bugs or fish for that period!')
        
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            if error.original.args[0] == 'WrongCritterType':
                await ctx.send("I'm afraid I don't know what type of critter you are looking for. I only know about bugs and fish hoo..")

            elif error.original.args[0] == 'HemisphereDoesNotExist':
                await ctx.send(f"I'm afraid {error.original.args[1]} is not an existing hemisphere. You can only choose between northern and southern.")
        else:
            await ctx.send(self.default_error_msg)


    def _verify_hemisphere(self, hemisphere:str) -> str:
        """Verifies the given hemisphere is valid by looking through the serversettings JSON file.

        :type hemisphere: str
        :raises Exception: HemisphereDoesNotExist. The method could not find the given hemisphere in the serversettings JSON file.
        :rtype: str
        """
        valid_hemispheres = Serversettings().get_valid_hemispheres()
        if hemisphere in valid_hemispheres['northern'] or hemisphere in valid_hemispheres['southern']:
            for hs in valid_hemispheres:
                if hemisphere in hs:
                    hemisphere = hs
                    break
            return hemisphere
        else:
            raise Exception('HemisphereDoesNotExist', hemisphere)



def setup(bot:discord.ext.commands.Bot):
    bot.add_cog(Critterpedia(bot))